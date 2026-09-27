import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SIR on a network

    The model presented in `sir-from-scratch`, but on a NetworkX network.

    For SIR, I used EoN (Epidemics on Networks, [GitHub](https://epidemicsonnetworks.readthedocs.io/en/latest/))
    """)
    return


@app.cell
def _():
    import EoN
    import marimo as mo
    import matplotlib.pyplot as plt
    import networkx as nx

    return EoN, mo, nx, plt


@app.cell
def _(mo):
    population_size_slider = mo.ui.slider(
        start=1000,
        stop=100_000,
        step=1000,
        value=1000,
        label="Population Size"
    )

    edge_probability_slider = mo.ui.slider(
        start=0,
        stop=1,
        step=0.01,
        value=0.01,
        label="Edge Creation Probability"
    )

    tau_slider = mo.ui.slider(
        start=0.1,
        stop=1.0,
        step=0.01,
        value=0.5,
        label="Infection Rate (tau)"
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
        value=5,
        label="Initial Infected Individuals"
    )

    mo.vstack([population_size_slider, edge_probability_slider, tau_slider, gamma_slider, initial_infected_slider])
    return (
        edge_probability_slider,
        gamma_slider,
        initial_infected_slider,
        population_size_slider,
        tau_slider,
    )


@app.cell
def _(
    edge_probability_slider,
    gamma_slider,
    initial_infected_slider,
    population_size_slider,
    tau_slider,
):
    population_size = population_size_slider.value
    edge_probability = edge_probability_slider.value
    tau = tau_slider.value
    gamma = gamma_slider.value
    initial_infected = initial_infected_slider.value
    return edge_probability, gamma, initial_infected, population_size, tau


@app.cell
def _(edge_probability, nx, population_size):
    epidemic_network = nx.fast_gnp_random_graph(population_size, edge_probability)
    return (epidemic_network,)


@app.cell
def _(EoN, epidemic_network, gamma, initial_infected, tau):
    t, S, I, R = EoN.fast_SIR(epidemic_network, tau=tau, gamma=gamma, initial_infecteds=initial_infected)
    return I, R, S, t


@app.cell
def _(I, R, S, plt, population_size, t):
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, facecolor="#dddddd", axisbelow=True)
    ax.plot(t, S / 1000, "b", alpha=0.5, lw=2, label="Susceptible")
    ax.plot(t, I / 1000, "r", alpha=0.5, lw=2, label="Infected")
    ax.plot(t, R / 1000, "g", alpha=0.5, lw=2, label="Recovered with immunity")
    ax.set_xlabel("Time")
    ax.set_ylabel("Number (1000s)")
    ax.set_ylim(0, 1.2 * population_size / 1000)
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
