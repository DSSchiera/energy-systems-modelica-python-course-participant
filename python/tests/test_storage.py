"""Tests for M03 storage tank: series-tank solution, conservation, losses, flow reversal."""

import numpy as np
import pytest

from energy_training.simulation import storage as st
from energy_training.simulation.inputs import piecewise_constant

H = 3600.0
T_HOT, T_COLD, T_ENV = 333.15, 303.15, 293.15


@pytest.mark.parametrize("N", [1, 4, 10])
def test_charging_matches_series_tank_solution(N):
    p = st.StorageParams(N=N, UA_loss=0.0)
    m = 0.1
    t = np.linspace(0, 2 * st.residence_time(m, p), 241)
    res = st.simulate((0, t[-1]), T_COLD, m, T_HOT, T_ENV, p, t_eval=t)
    for k in (1, N):
        exact = st.analytic_series_step(t, k, T_COLD, T_HOT, m, p)
        assert np.max(np.abs(res.T[:, k - 1] - exact)) < 1e-5  # 3e-8 relative at rtol 1e-8


def test_mean_residence_time_independent_of_N():
    """Simulated outlet after an inlet step: int (1 - F) dt = rho V / m_flow for any N."""
    m = 0.1
    for N in (1, 5, 20):
        p = st.StorageParams(N=N, UA_loss=0.0)
        tau = st.residence_time(m, p)
        t = np.linspace(0, 12 * tau, 2401)
        res = st.simulate((0, t[-1]), T_COLD, m, T_HOT, T_ENV, p, t_eval=t)
        F = (res.T_out - T_COLD) / (T_HOT - T_COLD)  # 0 -> 1
        assert np.trapezoid(1 - F, t) == pytest.approx(tau, rel=1e-3)


def test_conduction_conserves_energy_and_mixes():
    p = st.StorageParams(N=6, UA_loss=0.0, G=5.0)
    T0 = np.linspace(T_HOT, T_COLD, 6)
    # slowest mixing mode: tau = C_node / (2 G (1 - cos(pi/N))) ~ 43 h; run ~23 tau
    res = st.simulate((0, 1000 * H), T0, 0.0, T_HOT, T_ENV, p, t_eval=np.linspace(0, 1000 * H, 81))
    np.testing.assert_allclose(res.T.sum(axis=1), T0.sum(), rtol=1e-12)
    np.testing.assert_allclose(res.T[-1], T0.mean(), atol=1e-3)


def test_standby_losses_decay_exponentially():
    p = st.StorageParams()
    t = np.linspace(0, 200 * H, 101)
    res = st.simulate((0, t[-1]), T_HOT, 0.0, T_HOT, T_ENV, p, t_eval=t)
    exact = T_ENV + (T_HOT - T_ENV) * np.exp(-t / st.loss_time_constant(p))
    assert np.max(np.abs(res.T - exact[:, None])) < 1e-6


def test_discharge_mirrors_charge():
    """Upward flow from the bottom is the charging problem with the node order reversed."""
    p = st.StorageParams(N=8, G=1.0)
    t = np.linspace(0, 3 * H, 61)
    T0 = np.linspace(T_HOT, T_COLD, 8)
    down = st.simulate((0, 3 * H), T0[::-1], 0.08, T_HOT, T_ENV, p, t_eval=t)
    up = st.simulate((0, 3 * H), T0, -0.08, T_HOT, T_ENV, p, t_eval=t)
    np.testing.assert_allclose(up.T, down.T[:, ::-1], atol=1e-6)
    np.testing.assert_allclose(up.T_out, up.T[:, 0])


def test_energy_balance_with_charge_and_discharge():
    p = st.StorageParams(N=10, G=2.0)
    m = piecewise_constant([0.0, 2 * H, 3 * H, 5 * H], [0.1, 0.0, -0.06, 0.0])
    T_in = piecewise_constant([0.0, 3 * H], [T_HOT, T_COLD])
    t = np.linspace(0, 8 * H, 8 * 120 + 1)  # 30-s grid, jumps on grid points
    res = st.simulate((0, 8 * H), T_COLD, m, T_in, T_ENV, p, t_eval=t)
    eb = st.energy_balance(res, p)
    throughput = abs(eb["advected"]) + abs(eb["lost"]) + abs(eb["stored"])
    # 4 jumps of the advected power, each smeared over one 30-s sample by the trapezoid rule
    adv = np.abs(res.m_flow) * p.cp * (res.T_in - res.T_out)
    smear = np.abs(np.diff(adv)).max() * 30.0 / 2 * 4
    assert abs(eb["residual"]) <= smear + 1e-6 * throughput


def test_energy_balance_criterion_with_continuous_power():
    """Course validation criterion: |residual| / throughput < 1e-4.

    The flow reverses smoothly; the inlet temperature switches only when the flow is zero, so the
    advected power has no jumps and the trapezoid rule is accurate."""
    p = st.StorageParams(N=10, G=2.0)
    period = 4 * H

    def m(t):
        return 0.08 * np.sin(2 * np.pi * t / period)

    def T_in(t):
        return T_HOT if m(t) >= 0 else T_COLD

    t = np.linspace(0, 8 * H, 8 * 360 + 1)  # 10-s grid
    res = st.simulate(
        (0, 8 * H),
        T_COLD,
        m,
        T_in,
        T_ENV,
        p,
        t_eval=t,
        breakpoints=[period / 2 * k for k in range(1, 4)],
    )
    eb = st.energy_balance(res, p)
    throughput = abs(eb["advected"]) + abs(eb["lost"]) + abs(eb["stored"])
    assert abs(eb["residual"]) / throughput < 1e-4


def test_input_validation():
    with pytest.raises(ValueError):
        st.StorageParams(N=0)
    with pytest.raises(ValueError):
        st.simulate((0, 10.0), [T_HOT, T_COLD], 0.0, T_HOT, T_ENV, st.StorageParams(N=3))


def test_loose_tolerance_breaks_maximum_principle():
    """Documented pitfall (common errors): at SciPy's default tolerances a node can exceed T_in."""
    p = st.StorageParams(N=50)
    t = np.linspace(0, 2 * H, 241)
    loose = st.simulate((0, 2 * H), T_COLD, 0.1, T_HOT, T_ENV, p, t_eval=t, rtol=1e-3, atol=1e-6)
    tight = st.simulate((0, 2 * H), T_COLD, 0.1, T_HOT, T_ENV, p, t_eval=t)
    assert loose.T.max() > T_HOT + 0.1
    assert tight.T.max() <= T_HOT + 1e-6


def test_degenerate_arguments():
    p = st.StorageParams()
    with pytest.raises(ValueError):
        st.residence_time(0.0, p)
    with pytest.raises(ValueError):
        st.loss_time_constant(st.StorageParams(UA_loss=0.0))
