from math import cosh, sinh

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

c = 299792458.  # m/s
g = 9.81  # m/s^2
planck_constant = 6.62607015e-34    # kg * m^2 /s
nu_caesium = 9192631770           # 1/s
year_seconds = 365.2425 * 24 * 3600
light_year_metres = year_seconds * c

# chart chrome (light surface)
_SURFACE = '#fcfcfb'
_INK = '#0b0b0b'
_MUTED = '#898781'
_GRID = '#e1e0d9'
_AXIS = '#c3c2b7'
_SERIES_TIME = '#2a78d6'  # categorical slot 1
_SERIES_DIST = '#eb6834'  # categorical slot 2

# sequential ramps for the 3-d surfaces: one hue each, light -> dark
_RAMP_TIME = LinearSegmentedColormap.from_list(
    'blue_seq', ['#cde2fb', '#86b6ef', '#3987e5', '#256abf', '#0d366b'])
_RAMP_DIST = LinearSegmentedColormap.from_list(
    'orange_seq', ['#fbe1d3', '#f4a780', '#eb6834', '#b94a1e', '#6d2a0f'])


def hyperbolic_motion(tau: float, a: float) -> tuple:
    """
    Idea: spaceship accelerating with a constant proper acceleration of a during a proper time of tau
    tau: a proper time in seconds
    a: acceleration in m/s^2
    returns elapsed time t (in seconds) and distance covered x (in metres) as seen on Earth
    """

    t = c / a * sinh(a / c * tau)
    x = c ** 2 / a * (cosh(a / c * tau) - 1)

    return t, x


def _decorate(ax, series_colour, ylabel, title):
    """Recessive grid and axes, muted labels; keeps the ink off the data."""
    ax.set_facecolor(_SURFACE)
    ax.grid(True, which='major', color=_GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color(_AXIS)
    ax.tick_params(colors=_MUTED, labelsize=9)
    ax.set_ylabel(ylabel, color=_MUTED, fontsize=10)
    ax.set_title(title, color=_INK, fontsize=11, loc='left', pad=8)
    return series_colour


def _annotate_end(ax, xs, ys, colour, unit):
    """Direct label on the last point instead of a legend box (one series per panel)."""
    ax.plot(xs[-1], ys[-1], marker='o', markersize=5, color=colour, zorder=3)
    ax.annotate(f' {ys[-1]:.3g} {unit}', (xs[-1], ys[-1]),
                color=colour, fontsize=9, va='center', ha='right',
                xytext=(-8, 10), textcoords='offset points')


def plot_hyperbolic_motion(lb: float, ub: float, a: float = g, n: int = 400):
    """
    Plot hyperbolic_motion(tau, a) for lb <= tau <= ub, both bounds given in years.

    Two panels sharing the proper-time axis (elapsed time and distance are different
    measures, so they never share one y-scale):
      - Earth elapsed time t, in years
      - distance covered x, in light years
    The dashed grey line in each panel is the non-relativistic reference (t = tau, x = c * tau).
    Returns the figure.
    """
    if ub <= lb:
        raise ValueError(f'need lb < ub, got lb={lb}, ub={ub}')
    if lb < 0:
        raise ValueError(f'need lb >= 0, got lb={lb}')

    step = (ub - lb) / (n - 1)
    taus = [lb + i * step for i in range(n)]
    results = [hyperbolic_motion(tau * year_seconds, a) for tau in taus]
    ts = [t / year_seconds for t, _ in results]
    xs = [x / light_year_metres for _, x in results]

    fig, (ax_t, ax_x) = plt.subplots(2, 1, sharex=True, figsize=(8, 7.5),
                                     facecolor=_SURFACE, constrained_layout=True)
    fig.suptitle(f'Spaceship at constant proper acceleration a = {a:g} m/s²',
                 color=_INK, fontsize=13, x=0.02, ha='left')

    for ax, ys, colour, ylabel, title, unit, reference in (
            (ax_t, ts, _SERIES_TIME, 'elapsed time t (years)',
             'Time on Earth', 'yr', 't = τ  (no dilation)'),
            (ax_x, xs, _SERIES_DIST, 'distance x (light years)',
             'Distance covered', 'ly', 'x = c·τ')):
        _decorate(ax, colour, ylabel, title)
        ax.plot(taus, taus, color=_MUTED, linewidth=1.2, linestyle='--', zorder=1)
        ax.plot(taus, ys, color=colour, linewidth=2, zorder=2)
        _annotate_end(ax, taus, ys, colour, unit)
        ax.annotate(reference, (taus[-1], taus[-1]), color=_MUTED, fontsize=9,
                    ha='right', va='top', xytext=(-4, -8), textcoords='offset points',
                    bbox=dict(facecolor=_SURFACE, edgecolor='none', pad=1.5))
        if lb > 0 and ys[-1] / max(ys[0], 1e-12) > 100:
            ax.set_yscale('log')

    ax_x.set_xlabel('proper time τ on board (years)', color=_MUTED, fontsize=10)

    plt.show()
    return fig


def _decorate3d(ax, zlabel, title):
    """Same recessive chrome as the 2-d panels, applied to the three panes."""
    ax.set_facecolor(_SURFACE)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1, 1, 1, 0))
        axis.line.set_color(_AXIS)
        axis._axinfo['grid'].update(color=_GRID, linewidth=0.8)
    ax.tick_params(colors=_MUTED, labelsize=8)
    ax.set_xlabel('proper time τ (years)', color=_MUTED, fontsize=9, labelpad=6)
    ax.set_ylabel('acceleration a (g)', color=_MUTED, fontsize=9, labelpad=6)
    ax.set_zlabel(zlabel, color=_MUTED, fontsize=9, labelpad=8)
    ax.set_title(title, color=_INK, fontsize=11, loc='left', pad=0)


def plot_hyperbolic_motion_3d(lb_tau: float, ub_tau: float,
                              lb_a: float, ub_a: float,
                              n_tau: int = 60, n_a: int = 60):
    """
    Surface plot of hyperbolic_motion(tau, a) over the rectangle
    lb_tau <= tau <= ub_tau (years) and lb_a <= a <= ub_a (multiples of g).

    Two surfaces, one per output — elapsed time and distance are different measures,
    so they get their own panel and their own z-scale:
      - left:  Earth elapsed time t, in years
      - right: distance covered x, in light years
    Height and colour both carry magnitude (one hue per panel, light -> dark).
    Either panel switches to a log10 z-axis when its values span more than two
    decades, which they quickly do.
    Returns the figure.
    """
    if ub_tau <= lb_tau:
        raise ValueError(f'need lb_tau < ub_tau, got {lb_tau}, {ub_tau}')
    if ub_a <= lb_a:
        raise ValueError(f'need lb_a < ub_a, got {lb_a}, {ub_a}')
    if lb_tau < 0:
        raise ValueError(f'need lb_tau >= 0, got {lb_tau}')
    if lb_a <= 0:
        raise ValueError(f'need lb_a > 0 (a = 0 is not accelerated motion), got {lb_a}')

    taus = np.linspace(lb_tau, ub_tau, n_tau)  # years
    accs = np.linspace(lb_a, ub_a, n_a)  # multiples of g

    # rows are a, columns are tau
    tau_grid, a_grid = np.meshgrid(taus, accs)
    grid = [[hyperbolic_motion(tau * year_seconds, a * g) for tau in taus] for a in accs]
    t_grid = np.array([[t for t, _ in row] for row in grid]) / year_seconds
    x_grid = np.array([[x for _, x in row] for row in grid]) / light_year_metres

    fig = plt.figure(figsize=(13, 6), facecolor=_SURFACE, constrained_layout=True)
    fig.suptitle('Spaceship at constant proper acceleration: '
                 'Earth time and distance over (τ, a)',
                 color=_INK, fontsize=13, x=0.02, ha='left')

    for k, (zs, ramp, zlabel, title, unit) in enumerate((
            (t_grid, _RAMP_TIME, 'elapsed time t (years)', 'Time on Earth', 'yr'),
            (x_grid, _RAMP_DIST, 'distance x (light years)', 'Distance covered', 'ly'))):
        lo, hi = zs.min(), zs.max()
        if lo > 0 and hi / lo > 100:
            zs = np.log10(zs)
            zlabel = f'log₁₀ {zlabel}'
            unit = f'log₁₀ {unit}'

        ax = fig.add_subplot(1, 2, k + 1, projection='3d', facecolor=_SURFACE)
        surface = ax.plot_surface(tau_grid, a_grid, zs, cmap=ramp,
                                  linewidth=0.2, edgecolor=_SURFACE,
                                  rstride=2, cstride=2, antialiased=True)
        _decorate3d(ax, zlabel, title)
        ax.view_init(elev=24, azim=-60)

        # horizontal bar underneath: a vertical one would sit on the z-axis label
        bar = fig.colorbar(surface, ax=ax, orientation='horizontal',
                           shrink=0.6, aspect=30, pad=0.02)
        bar.outline.set_visible(False)
        bar.ax.tick_params(colors=_MUTED, labelsize=8)
        bar.set_label(unit, color=_MUTED, fontsize=9)

    plt.show()
    return fig


def kilogram():
    aa = 6.09110229711386655
    bb = 8.9875517873681764e40
    
    kg1 = bb / aa
    
    M_CS = planck_constant * nu_caesium / c ** 2 
    # kg = 1.4755214e40 * planck_constant * nu_caesium / c ** 2 
    
    kg = 1/M_CS
    return M_CS, kg

if __name__ == '__main__':
    
    print(kilogram())

    tau = 10 * year_seconds
    v = g * tau
    print(v)
    
    t, x = hyperbolic_motion(tau, g/10)
    print(t / year_seconds, x / light_year_metres)

    # plot_hyperbolic_motion(1, 20)

    # plot_hyperbolic_motion_3d(1, 20, 0.1, 2.)
