from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


K = 8
M = 1
X0 = 1.5 * np.pi
X_END = 3.0 * np.pi
STEPS = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5]


def exact_solution(x: np.ndarray | float) -> np.ndarray | float:
    return np.exp(-K * np.cos(M * x)) - K * np.cos(M * x) + 1


def rhs(x: float, y: float) -> float:
    return K * M * np.sin(M * x) * (y + K * np.cos(M * x))


def solve_euler(h: float) -> tuple[np.ndarray, np.ndarray]:
    n_steps = int(np.ceil((X_END - X0) / h))
    xs = np.empty(n_steps + 1)
    ys = np.empty(n_steps + 1)

    xs[0] = X0
    ys[0] = exact_solution(X0)

    for i in range(n_steps):
        step = min(h, X_END - xs[i])
        xs[i + 1] = xs[i] + step
        ys[i + 1] = ys[i] + step * rhs(xs[i], ys[i])

    return xs, ys


def solve_rk4(h: float) -> tuple[np.ndarray, np.ndarray]:
    n_steps = int(np.ceil((X_END - X0) / h))
    xs = np.empty(n_steps + 1)
    ys = np.empty(n_steps + 1)

    xs[0] = X0
    ys[0] = exact_solution(X0)

    for i in range(n_steps):
        step = min(h, X_END - xs[i])
        x = xs[i]
        y = ys[i]

        k1 = rhs(x, y)
        k2 = rhs(x + step / 2, y + step * k1 / 2)
        k3 = rhs(x + step / 2, y + step * k2 / 2)
        k4 = rhs(x + step, y + step * k3)

        xs[i + 1] = x + step
        ys[i + 1] = y + step * (k1 + 2 * k2 + 2 * k3 + k4) / 6

    return xs, ys


def max_error(xs: np.ndarray, ys: np.ndarray) -> float:
    return float(np.max(np.abs(exact_solution(xs) - ys)))


def decimate(xs: np.ndarray, ys: np.ndarray, max_points: int = 5000) -> tuple[np.ndarray, np.ndarray]:
    if len(xs) <= max_points:
        return xs, ys
    indices = np.linspace(0, len(xs) - 1, max_points, dtype=int)
    return xs[indices], ys[indices]


def plot_solution(h: float, euler: tuple[np.ndarray, np.ndarray], rk4: tuple[np.ndarray, np.ndarray], out_dir: Path) -> None:
    x_dense = np.linspace(X0, X_END, 2500)
    exact_y = exact_solution(x_dense)
    euler_x, euler_y = decimate(*euler)
    rk4_x, rk4_y = decimate(*rk4)

    fig, (ax_full, ax_zoom) = plt.subplots(2, 1, figsize=(8.5, 7.2), sharex=True)

    for ax in (ax_full, ax_zoom):
        ax.plot(x_dense, exact_y, color="black", linewidth=2.0, label="rozwiązanie dokładne")
        ax.plot(euler_x, euler_y, color="#d55e00", linewidth=1.25, label="metoda Eulera")
        ax.plot(rk4_x, rk4_y, color="#0072b2", linestyle="--", linewidth=1.35, label="Runge-Kutta 4")
        ax.grid(True, alpha=0.25)
        ax.set_ylabel("y")

    margin = 0.08 * (float(np.max(exact_y)) - float(np.min(exact_y)))
    ax_zoom.set_ylim(float(np.min(exact_y)) - margin, float(np.max(exact_y)) + margin)
    ax_full.set_title(f"Porównanie rozwiązań dla h = {h:g} (pełna skala)")
    ax_zoom.set_title("Zbliżenie na zakres rozwiązania dokładnego")
    ax_zoom.set_xlabel("x")
    ax_full.legend(loc="best")
    fig.tight_layout()
    plt.savefig(out_dir / f"rozwiazania_h_{h:.0e}.png", dpi=180)
    plt.close()


def plot_errors(errors: list[tuple[float, float, float]], out_dir: Path) -> None:
    h_values = np.array([row[0] for row in errors])
    euler_errors = np.array([row[1] for row in errors])
    rk4_errors = np.array([row[2] for row in errors])

    plt.figure(figsize=(8.2, 5.0))
    plt.loglog(h_values, euler_errors, "o-", label="metoda Eulera")
    plt.loglog(h_values, rk4_errors, "s-", label="Runge-Kutta 4")
    plt.gca().invert_xaxis()
    plt.xlabel("krok h")
    plt.ylabel(r"$E_{max}$")
    plt.title("Maksymalny błąd przybliżenia")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "bledy_maksymalne.png", dpi=180)
    plt.close()


def save_table(errors: list[tuple[float, float, float]], out_dir: Path) -> None:
    def latex_sci(value: float, digits: int = 5) -> str:
        mantissa, exponent = f"{value:.{digits}e}".split("e")
        return rf"{mantissa}\cdot 10^{{{int(exponent)}}}"

    step_labels = {
        1e-1: r"10^{-1}",
        1e-2: r"10^{-2}",
        1e-3: r"10^{-3}",
        1e-4: r"10^{-4}",
        1e-5: r"10^{-5}",
    }

    lines = [
        r"\begin{tabular}{rcc}",
        r"\toprule",
        r"$h$ & Metoda Eulera & Metoda Rungego-Kutty \\",
        r"\midrule",
    ]

    for h, euler_error, rk4_error in errors:
        lines.append(
            rf"${step_labels[h]}$ & ${latex_sci(euler_error)}$ & ${latex_sci(rk4_error)}$ \\"
        )

    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    (out_dir / "tabela_bledow.tex").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    errors: list[tuple[float, float, float]] = []

    for h in STEPS:
        euler = solve_euler(h)
        rk4 = solve_rk4(h)
        euler_error = max_error(*euler)
        rk4_error = max_error(*rk4)
        errors.append((h, euler_error, rk4_error))
        plot_solution(h, euler, rk4, out_dir)

    plot_errors(errors, out_dir)
    save_table(errors, out_dir)

    for h, euler_error, rk4_error in errors:
        print(f"h={h:.0e}; Euler={euler_error:.8e}; RK4={rk4_error:.8e}")


if __name__ == "__main__":
    main()
