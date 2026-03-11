#include <iostream>
#include <iomanip>
#include <cmath>
#include <fstream>
#include <limits>

int main() {
    // Open output files for small and large argument ranges
    std::ofstream file_small("data_small.csv");
    std::ofstream file_large("data_big.csv");

    // Set scientific notation with maximum precision for long double
    int max_digits = std::numeric_limits<long double>::max_digits10;
    file_small << std::scientific << std::setprecision(max_digits);
    file_large << std::scientific << std::setprecision(max_digits);

    // Write CSV headers
    file_small << "k,x,f_float,g_float,f_double,g_double,f_long_double,g_long_double\n";
    file_large << "potega_10,x,f_float,g_float,f_double,g_double,f_long_double,g_long_double\n";

    // Part 1: Analyze loss of significant digits with small arguments (x = 8^-k)
    // Direct subtraction loss vs algebraically stable reformulation
    long double x_small = 1.0L;
    for (int k = 1; k <= 20; ++k) {
        x_small /= 8.0L;

        float x_f = static_cast<float>(x_small);
        double x_d = static_cast<double>(x_small);
        long double x_ld = x_small;

        // Compute f(x) = sqrt(x^2 + 1) - 1 (unstable for small x)
        float f_float = std::sqrt(x_f * x_f + 1.0f) - 1.0f;
        float g_float = (x_f * x_f) / (std::sqrt(x_f * x_f + 1.0f) + 1.0f);

        // Same computation using double precision
        double f_double = std::sqrt(x_d * x_d + 1.0) - 1.0;
        double g_double = (x_d * x_d) / (std::sqrt(x_d * x_d + 1.0) + 1.0);

        // Same computation using long double precision
        long double f_long_double = std::sqrt(x_ld * x_ld + 1.0L) - 1.0L;
        long double g_long_double = (x_ld * x_ld) / (std::sqrt(x_ld * x_ld + 1.0L) + 1.0L);

        file_small << k << "," << x_ld << ","
                   << f_float << "," << g_float << ","
                   << f_double << "," << g_double << ","
                   << f_long_double << "," << g_long_double << "\n";
    }

    // Part 2: Analyze overflow behavior with large arguments approaching max_double (~10^308)
    for (int potega = 10; potega <= 310; potega += 20) {
        long double x_large = std::pow(10.0L, potega);

        float x_f = static_cast<float>(x_large);
        double x_d = static_cast<double>(x_large);
        long double x_ld = x_large;

        float f_float = std::sqrt(x_f * x_f + 1.0f) - 1.0f;
        float g_float = (x_f * x_f) / (std::sqrt(x_f * x_f + 1.0f) + 1.0f);

        double f_double = std::sqrt(x_d * x_d + 1.0) - 1.0;
        double g_double = (x_d * x_d) / (std::sqrt(x_d * x_d + 1.0) + 1.0);

        long double f_long_double = std::sqrt(x_ld * x_ld + 1.0L) - 1.0L;
        long double g_long_double = (x_ld * x_ld) / (std::sqrt(x_ld * x_ld + 1.0L) + 1.0L);

        file_large << potega << "," << x_ld << ","
                   << f_float << "," << g_float << ","
                   << f_double << "," << g_double << ","
                   << f_long_double << "," << g_long_double << "\n";
    }

    std::cout << "Computation complete. Generated 'data_small.csv' and 'data_big.csv'." << std::endl;
    return 0;
}