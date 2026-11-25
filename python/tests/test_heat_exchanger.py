"""Tests for the effectiveness-NTU functions against directly solved temperature profiles."""

import pytest
from scipy.integrate import solve_ivp

from energy_training.simulation import heat_exchanger as hx

CASES = [(2000.0, 4000.0, 1500.0), (3000.0, 3000.0, 6000.0), (5000.0, 1200.0, 900.0)]


def _parallel(UA, C_h, C_c, Th, Tc):
    def f(x, y):
        d = y[0] - y[1]
        return [-UA / C_h * d, UA / C_c * d]

    sol = solve_ivp(f, (0, 1), [Th, Tc], rtol=1e-11, atol=1e-11)
    return C_h * (Th - sol.y[0, -1])


def _counterflow(UA, C_h, C_c, Th, Tc):
    """Shooting: hot enters at x = 0, cold enters at x = 1 and flows towards x = 0.

    The profiles are linear in the unknown cold outlet T_c(0), so two integrations fix it."""

    def f(x, y):
        d = y[0] - y[1]
        return [-UA / C_h * d, -UA / C_c * d]

    def end(Tc0):
        sol = solve_ivp(f, (0, 1), [Th, Tc0], rtol=1e-12, atol=1e-12)
        return sol.y[:, -1]

    a, b = end(Tc), end(Th)  # two trial cold-outlet temperatures
    s = (Tc - a[1]) / (b[1] - a[1])  # interpolate so that T_c(1) = Tc
    Th_out = a[0] + s * (b[0] - a[0])
    return C_h * (Th - Th_out)


@pytest.mark.parametrize("UA,C_h,C_c", CASES)
@pytest.mark.parametrize(
    "arrangement,direct", [("parallel", _parallel), ("counterflow", _counterflow)]
)
def test_effectiveness_matches_profiles(UA, C_h, C_c, arrangement, direct):
    Q = hx.heat_flow(UA, C_h, C_c, 343.15, 303.15, arrangement)
    assert Q == pytest.approx(direct(UA, C_h, C_c, 343.15, 303.15), rel=1e-6)


def test_limits():
    assert hx.effectiveness(50.0, 0.5, "counterflow") == pytest.approx(1.0, abs=1e-9)
    assert hx.effectiveness(50.0, 0.5, "parallel") == pytest.approx(1 / 1.5, abs=1e-9)
    assert hx.effectiveness(0.0, 0.3) == 0.0
    # C_r -> 1 is continuous for counterflow
    assert hx.effectiveness(2.0, 1.0 - 1e-9) == pytest.approx(hx.effectiveness(2.0, 1.0), rel=1e-6)
    with pytest.raises(ValueError):
        hx.effectiveness(1.0, 1.5)
