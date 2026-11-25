"""Tests for M01 ThermalZone: analytic solution, numerical accuracy, stability, energy balance."""

import numpy as np
import pytest

from energy_training.simulation import thermal_zone as tz
from energy_training.simulation.inputs import piecewise_constant
from energy_training.simulation.integrators import euler_amplification, explicit_euler
from energy_training.utilities import celsius_to_kelvin

P = tz.ThermalZoneParams()  # C = 1e7 J/K, UA = 200 W/K -> tau = 5e4 s
T_AMB = float(celsius_to_kelvin(0.0))
T0 = float(celsius_to_kelvin(10.0))
Q = 4000.0  # W -> T_ss = 20 degC
H = 3600.0


def test_time_constant_and_steady_state():
    assert tz.time_constant(P) == pytest.approx(5.0e4)
    assert tz.steady_state(Q, T_AMB, P) == pytest.approx(T_AMB + 20.0)


def test_rhs_zero_at_equilibrium():
    assert tz.rhs(0.0, tz.steady_state(Q, T_AMB, P), Q, T_AMB, P) == pytest.approx(0.0, abs=1e-15)


def test_analytic_properties():
    tau = tz.time_constant(P)
    T_ss = tz.steady_state(Q, T_AMB, P)
    assert tz.analytic_step(0.0, T0, Q, T_AMB, P) == pytest.approx(T0)
    # after one time constant 63.2 % of the step is completed
    frac = (tz.analytic_step(tau, T0, Q, T_AMB, P) - T0) / (T_ss - T0)
    assert frac == pytest.approx(1 - np.exp(-1))


def test_solve_ivp_matches_analytic():
    t = np.linspace(0, 72 * H, 301)
    res = tz.simulate((0, 72 * H), T0, Q, T_AMB, P, t_eval=t)
    exact = tz.analytic_step(t, T0, Q, T_AMB, P)
    assert np.max(np.abs(res.T - exact)) < 1e-6


def test_state_space_consistent_with_rhs():
    A, B, C, D = tz.state_space(P)
    for T in (T0, T_AMB + 5.0):
        x_dot = A @ [T] + B @ [Q, T_AMB]
        assert x_dot[0] == pytest.approx(tz.rhs(0.0, T, Q, T_AMB, P))
    assert C.shape == (1, 1) and D.shape == (1, 2)
    # eigenvalue of A is -1/tau
    assert np.linalg.eigvals(A)[0] == pytest.approx(-1 / tz.time_constant(P))


def test_euler_first_order_convergence():
    def f(t, y):
        return np.array([tz.rhs(t, y[0], Q, T_AMB, P)])

    errors = []
    for h in (2 * H, 1 * H, 0.5 * H):
        t, y = explicit_euler(f, (0, 24 * H), T0, h)
        errors.append(abs(y[-1, 0] - tz.analytic_step(t[-1], T0, Q, T_AMB, P)))
    ratios = np.array(errors[:-1]) / np.array(errors[1:])
    assert np.all((ratios > 1.8) & (ratios < 2.2)), ratios  # error ~ h


@pytest.mark.parametrize(
    ("h_over_tau", "behaviour"),
    [(0.5, "monotone"), (1.5, "oscillating"), (2.5, "diverging")],
)
def test_euler_stability_regimes(h_over_tau, behaviour):
    tau = tz.time_constant(P)

    def f(t, y):
        return np.array([tz.rhs(t, y[0], Q, T_AMB, P)])

    t, y = explicit_euler(f, (0, 20 * tau), T0, h_over_tau * tau)
    dev = y[:, 0] - tz.steady_state(Q, T_AMB, P)
    g = euler_amplification(h_over_tau * tau, tau)
    np.testing.assert_allclose(dev[1:5] / dev[:4], g)  # deviation multiplied by g each step
    if behaviour == "monotone":
        assert np.all(np.diff(np.abs(dev)) < 0) and np.all(dev < 0)
    elif behaviour == "oscillating":
        assert np.all(np.sign(dev[1:6]) != np.sign(dev[:5])) and abs(dev[-1]) < abs(dev[0])
    else:
        n_steps = len(t) - 1
        assert abs(dev[-1]) == pytest.approx(abs(g) ** n_steps * abs(dev[0]))
        assert abs(dev[-1]) > 10 * abs(dev[0])


def test_piecewise_numeric_matches_analytic_and_conserves_energy():
    times = [0.0, 6 * H, 22 * H, 30 * H]
    q_vals = [4000.0, 0.0, 4000.0, 1000.0]
    q = piecewise_constant(times, q_vals)
    t = np.linspace(0, 48 * H, 48 * 60 + 1)  # 1-min grid: breakpoints are sample points
    res = tz.simulate((0, 48 * H), T0, q, T_AMB, P, t_eval=t)
    exact = tz.analytic_piecewise(t, T0, times, q_vals, [T_AMB] * 4, P)
    assert np.max(np.abs(res.T - exact)) < 3e-6  # ~ rtol * T = 1e-8 * 280 K
    # Energy: the trapezoid rule smears each input jump over one output sample (dt = 60 s),
    # so the integral of Q is off by sum(Q_after - Q_before) * dt / 2 — computed explicitly here.
    eb = tz.energy_balance(res, P)
    dt = t[1] - t[0]
    jumps = np.diff(q_vals)  # Q_after - Q_before at 6 h, 22 h, 30 h
    supplied_exact = 4000 * 6 * H + 4000 * 8 * H + 1000 * 18 * H
    assert eb["supplied"] == pytest.approx(supplied_exact + jumps.sum() * dt / 2, rel=1e-9)
    assert eb["residual"] == pytest.approx(jumps.sum() * dt / 2 * -1, rel=1e-3)


@pytest.mark.parametrize(("rtol", "atol", "bound"), [(1e-3, 1e-6, 1e-2), (1e-8, 1e-8, 3e-6)])
def test_input_jumps_not_seen_by_previous_segment(rtol, atol, bound):
    """Regression (review finding M1): RK stages at the segment end must use the held input."""
    times, q_vals = [0.0, 6 * H, 22 * H, 30 * H], [4000.0, 0.0, 4000.0, 1000.0]
    t = np.linspace(0, 48 * H, 48 * 60 + 1)
    res = tz.simulate(
        (0, 48 * H), T0, piecewise_constant(times, q_vals), T_AMB, P, t_eval=t, rtol=rtol, atol=atol
    )
    exact = tz.analytic_piecewise(t, T0, times, q_vals, [T_AMB] * 4, P)
    assert np.max(np.abs(res.T - exact)) < bound


def test_simulate_rejects_t_eval_outside_span():
    with pytest.raises(ValueError):
        tz.simulate((0, 10 * H), T0, Q, T_AMB, P, t_eval=np.array([0, 5 * H, 20 * H]))


def test_piecewise_constant_signal():
    s = piecewise_constant([0.0, 10.0], [1.0, 2.0])
    assert s(-5) == 1.0 and s(0) == 1.0 and s(9.99) == 1.0 and s(10) == 2.0 and s(1e9) == 2.0
    assert s.breakpoints == (10.0,)
    with pytest.raises(ValueError):
        piecewise_constant([0.0, 0.0], [1.0, 2.0])


def test_invalid_parameters():
    with pytest.raises(ValueError):
        tz.ThermalZoneParams(C=-1.0)
