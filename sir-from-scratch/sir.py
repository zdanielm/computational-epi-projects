import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The SIR Model

    This model divides the (fixed) population of *N* individuals into three "compartments" which may vary as a function of time, *t*:

    - *S(t)*: susceptible, but not yet infected

    - *I(t)*: infectious individuals

    - *R(t)*: those who have recovered and now have immunity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The SIR model describes the change in the population of these compartments in terms of parameters $\\beta$ and $\\gamma$.

    - $\\beta$ describes the *effective contact rate*: an infected individual comes into contact with $\\beta N$ other individuals per unit time (of which the fraction that are susceptible to contracting is $S/N$).

    - $\\gamma$ is the *mean recovery rate*: that is, $1/\\gamma$ is the mean period of time during which an infected individual can pass the disease on.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The differential equations describing the SIR model were first derived by Kermack and McKendrick \[Proc. R. Soc. A, **115**, 772 (1927)\]:

    $$
    \begin{aligned}
    \frac{dS}{dt} &= -\beta \frac{SI}{N}, \\
    \frac{dI}{dt} &= \beta \frac{SI}{N} - \gamma I, \\
    \frac{dR}{dt} &= \gamma I.
    \end{aligned}
    $$

    The following Python notebook integrates these equations for a disease characterised by parameters $\\beta = 0.2$ and $1/\\gamma = 10,\\mathrm{days}$ in a population of $N = 1000$ (perhaps flu in a school).

    The model starts with a single infected individual on day 0:

    $$
    I(0) = 1.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Disclaimer: Adopted from [Learning Scientific Programming with Python (2nd edition) - Chapter 8: SciPy/Examples/E8.29: The SIR epidemic model](https://scipython.com/books/book2/chapter-8-scipy/examples/the-sir-epidemic-model/) and made interactive using [marimo notebooks](https://marimo.io/)*
    """)
    return


@app.cell
def _():
    import marimo as mo #Interactive elements
    import matplotlib.pyplot as plt # Plotting
    import numpy as np # Numerical computing
    from scipy.integrate import odeint # Integrate ODEs

    return mo, np, odeint, plt


@app.cell
def _(mo):
    population_size_slider = mo.ui.slider(
        start=1000,
        stop=100_000,
        step=1000,
        value=1000,
        label="Population Size"
    )

    beta_slider = mo.ui.slider(
        start=0.1,
        stop=1.0,
        step=0.01,
        value=0.2,
        label="Infection Rate (beta)"
    )

    gamma_slider = mo.ui.slider(
        start=0.1,
        stop=1.0,
        step=0.01,
        value=0.1,
        label="Recovery Rate (gamma)"
    )

    initial_infected_slider = mo.ui.slider(
        start=1,
        stop=100,
        step=1,
        value=1,
        label="Initial Infected Individuals"
    )

    initial_recovered_slider = mo.ui.slider(
        start=0,
        stop=100,
        step=1,
        value=0,
        label="Initial Recovered Individuals"
    )

    mo.vstack([population_size_slider, beta_slider, gamma_slider, initial_infected_slider, initial_recovered_slider])
    return (
        beta_slider,
        gamma_slider,
        initial_infected_slider,
        initial_recovered_slider,
        population_size_slider,
    )


@app.cell
def _(
    beta_slider,
    gamma_slider,
    initial_infected_slider,
    initial_recovered_slider,
    population_size_slider,
):
    population_size = population_size_slider.value
    beta = beta_slider.value
    gamma = gamma_slider.value
    initial_infected = initial_infected_slider.value
    initial_recovered = initial_recovered_slider.value
    return beta, gamma, initial_infected, initial_recovered, population_size


@app.cell
def _(initial_infected, initial_recovered, population_size):
    initial_susceptible = population_size - initial_infected - initial_recovered
    return (initial_susceptible,)


@app.cell
def _(np):
    # A grid of time points (in days)
    t = np.linspace(0, 160, 160)
    return (t,)


@app.function
# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


@app.cell
def _(initial_infected, initial_recovered, initial_susceptible):
    # Initial conditions vector
    initial_conditions = initial_susceptible, initial_infected, initial_recovered
    return (initial_conditions,)


@app.cell
def _(beta, gamma, initial_conditions, odeint, population_size, t):
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, initial_conditions, t, args=(population_size, beta, gamma))
    return (ret,)


@app.cell
def _(ret):
    S, I, R = ret.T
    return I, R, S


@app.cell
def _(I, R, S, plt, t):
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, facecolor="#dddddd", axisbelow=True)
    ax.plot(t, S / 1000, "b", alpha=0.5, lw=2, label="Susceptible")
    ax.plot(t, I / 1000, "r", alpha=0.5, lw=2, label="Infected")
    ax.plot(t, R / 1000, "g", alpha=0.5, lw=2, label="Recovered with immunity")
    ax.set_xlabel("Time /days")
    ax.set_ylabel("Number (1000s)")
    ax.set_ylim(0, 1.2)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(which="major", c="w", lw=2, ls="-")
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ("top", "right", "bottom", "left"):
        ax.spines[spine].set_visible(False)
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
