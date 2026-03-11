# Lab 1 – Numeryczna Stabilność Algorytmów

Analiza wpływu precyzji zmiennoprzecinkowej na błędy obliczeń numerycznych dla funkcji $f(x) = \sqrt{x^2 + 1} - 1$.

## Kompilacja i Uruchomienie

### 1. Skompilować program C++ (g++)

```bash
g++ -std=c++17 -o main.exe main.cpp
```

### 2. Uruchomić program (generuje CSV)

```bash
./main.exe
```

Tworzy pliki:

- `data_small.csv` – analiza dla małych x (x = 8⁻ᵏ)
- `data_big.csv` – analiza dla dużych x

### 3. Wygenerować wykresy (Python)

Zainstaluj zależności:

```bash
pip install pandas matplotlib numpy
```

Uruchom skrypt:

```bash
python plots.py
```

## Wymagania

- Python 3.8+
- Biblioteki: `pandas`, `matplotlib`, `numpy`
- Kompilator C++ (g++)
