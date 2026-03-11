import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal, getcontext
import os

# Set precision for accurate reference values (100 significant digits)
getcontext().prec = 100

def get_true_val(x_str):
    """Calculate reference value: sqrt(x^2 + 1) - 1 with high precision."""
    x = Decimal(x_str)
    val = (x**2 + 1).sqrt() - 1
    return float(val)

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'data_small.csv')

df = pd.read_csv(file_path)
df['true_val'] = df['x'].apply(lambda x: get_true_val(str(x)))

# Plot 1: Relative error for f(x) across all data types
plt.figure(figsize=(12, 7))

for t, label, color, marker in [('float', 'float (32-bit)', 'red', 'o'), 
                                ('double', 'double (64-bit)', 'green', 's'), 
                                ('long_double', 'long double (80-bit)', 'blue', '^')]:
    f_col = f'f_{t}'
    err = np.abs(df[f_col] - df['true_val']) / df['true_val']
    # Set zero values to 1.0 for logarithmic scale visualization
    err[df[f_col] == 0] = 1.0
    plt.plot(df['x'], err, label=f'Error f(x) {label}', color=color, marker=marker, linestyle='-', markersize=5)

plt.xscale('log')
plt.yscale('log')
plt.gca().invert_xaxis()
plt.grid(True, which="both", ls="--", alpha=0.4)

plt.title('Relative Error of Formula $f(x) = \sqrt{x^2 + 1} - 1$ for Different Data Types', fontsize=14)
plt.xlabel('Argument $x$ (logarithmic scale)', fontsize=12)
plt.ylabel('Relative Error (1.0 = 100% error)', fontsize=12)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('wykres_bledow_3typy.png', dpi=300)

# Plot 2: Decay of computed values for f(x) and comparison with stable g(x)
plt.figure(figsize=(12, 7))

plt.plot(df['x'], df['true_val'], 'k--', linewidth=2, label='Reference value (ideal)', zorder=1)

plt.plot(df['x'], df['f_float'], 'r-o', label='$f(x)$ float', markersize=4)
plt.plot(df['x'], df['f_double'], 'g-s', label='$f(x)$ double', markersize=4)
plt.plot(df['x'], df['f_long_double'], 'b-^', label='$f(x)$ long double', markersize=4)

plt.plot(df['x'], df['g_float'], color='orange', linestyle=':', linewidth=2, label='$g(x)$ float (stable)')

plt.xscale('log')
plt.yscale('log')
plt.gca().invert_xaxis()
plt.grid(True, which="both", ls="--", alpha=0.4)

plt.title('Decay of Values Computed by $f(x)$ with Decreasing $x$', fontsize=14)
plt.xlabel('Argument $x$ (logarithmic scale)', fontsize=12)
plt.ylabel('Computed value (log)', fontsize=12)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('wykres_zaniku_wartosci.png', dpi=300)

print("Generated plots: 'wykres_bledow_3typy.png' and 'wykres_zaniku_wartosci.png'")
plt.show()