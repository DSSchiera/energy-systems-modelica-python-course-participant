"""Tests for M02 ZoneRC: state space, modes, closed-form solution, energy balance."""

import numpy as np
import pytest
from scipy.linalg import expm

from energy_training.simulation import thermal_zone as tz
from energy_training.simulation import zone_rc as zr
from energy_training.simulation.inputs import piecewise_constant

P = zr.ZoneRCParams()
H = 3600.0
T_AMB = 273.15
X0 = np.array([288.15, 283.15])


def test_state_space_matches_rhs():
    A, B, Cy, D = zr.state_space(P)
    rng = np.random.default_rng(0)
    for _ in range(5):
        x = 273.15 + 30 * rng.random(2)
        u = np.array([5000 * rng.random(), 263.15 + 20 * rng.random()])
        np.testing.assert_allclose(A @ x + B @ u, zr.rhs(0.0, x, u[0], u[1], P), rtol=1e-12)
    assert Cy.shape == (1, 2) and D.shape == (1, 2)


def test_time_constants_match_source():
    """Bacher & Madsen (2011), Table 3, TiTeTh: tau2 = 0.668 h, tau3 = 18.4 h. Dropping their
    heater node (tau1 = 0.129 h) leaves the two slower modes almost unchanged."""
    tau = zr.time_constants(P) / H
    assert tau[0] == pytest.approx(0.668, rel=0.01)
    assert tau[1] == pytest.approx(18.4, rel=0.01)
    lam = np.linalg.eigvals(zr.state_space(P)[0])
    assert np.all(np.abs(lam.imag) == 0) and np.all(lam.real < 0)


def test_steady_state_and_lumped_equivalent():
    Q = 4000.0
    Tz, Te = zr.steady_state(Q, T_AMB, P)
    A, B, *_ = zr.state_space(P)
    np.testing.assert_allclose(A @ [Tz, Te] + B @ [Q, T_AMB], 0.0, atol=1e-12)
    C, UA = zr.lumped_equivalent(P)
    assert C == pytest.approx(P.C_z + P.C_e)
    # same equilibrium as M01 with the series conductance
    assert Tz == pytest.approx(tz.steady_state(Q, T_AMB, tz.ThermalZoneParams(C=C, UA=UA)))


@pytest.mark.parametrize("Q", [0.0, 4000.0])
def test_simulation_matches_closed_form(Q):
    """x(t) = e^{At} x0 + A^{-1}(e^{At} - I) B u for constant inputs."""
    A, B, *_ = zr.state_space(P)
    u = np.array([Q, T_AMB])
    t = np.linspace(0, 72 * H, 145)
    res = zr.simulate((0, 72 * H), X0, Q, T_AMB, P, t_eval=t)
    for k, tk in enumerate(t):
        E = expm(A * tk)
        x = E @ X0 + np.linalg.solve(A, (E - np.eye(2)) @ B @ u)
        # 1e-5 K absolute = 3e-8 relative, far inside the 1e-5 criterion at rtol = 1e-8
        assert np.max(np.abs([res.T_z[k], res.T_e[k]] - x)) < 1e-5


def test_energy_balance_closes_with_schedule():
    times = [0.0, 6 * H, 22 * H, 30 * H, 46 * H]
    q = piecewise_constant(times, [4000.0, 1000.0, 4000.0, 1000.0, 4000.0])
    t = np.linspace(0, 48 * H, 48 * 60 + 1)  # 1-min grid: jumps fall on grid points
    res = zr.simulate(
        (0, 48 * H), X0, q, lambda s: T_AMB + 3 * np.sin(2 * np.pi * s / 86400), P, t_eval=t
    )
    eb = zr.energy_balance(res, P)
    # trapezoid smears each jump over one sample: |error| <= sum |dQ| dt / 2
    jumps = 4 * 3000.0 * 60.0 / 2
    assert abs(eb["residual"]) <= jumps + 1e-4 * eb["supplied"]


def test_invalid_parameters():
    with pytest.raises(ValueError):
        zr.ZoneRCParams(R_ze=0.0)
