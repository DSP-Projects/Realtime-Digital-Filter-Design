import numpy as np
class CodeGenerator:
    def __init__(self, z_plane_instance):
        b, a= z_plane_instance.compute_filter_coefficients()
        self.b=b #numerator coefficients
        self.a=a #denominator coefficients

    def generate_c_code(self):
        b = self.b  # Numerator coefficients
        a = self.a  # Denominator coefficients
        N = len(b) - 1  # Order of numerator
        M = len(a) - 1  # Order of denominator

        # Convert coefficients to formatted C-style strings
        b_str = ", ".join(f"{coef:.6f}" for coef in b)
        a_str = ", ".join(f"{coef:.6f}" for coef in a)

        c_code = f"""#include <stdio.h>

        #define N {N}  // Order of the numerator
        #define M {M}  // Order of the denominator

        // Filter coefficients
        double b[N+1] = {{ {b_str} }};  // Numerator coefficients
        double a[M+1] = {{ {a_str} }};  // Denominator coefficients

        // State buffer for Direct Form II
        double w[M+1] = {{0}};  

        // Direct Form II Transposed implementation
        double filter(double input) {{
            double output;

            // Compute the new state
            double w_new = input;
            for (int i = 1; i <= M; i++) {{
                w_new -= a[i] * w[i-1];
            }}

            // Compute the output
            output = b[0] * w_new;
            for (int i = 1; i <= N; i++) {{
                output += b[i] * w[i-1];
            }}

            // Shift delay buffer
            for (int i = M; i > 0; i--) {{
                w[i] = w[i-1];
            }}
            w[0] = w_new;

            return output;
        }}
            """

        # Save to a file
        with open("filter.c", "w") as file:
            file.write(c_code)

        print("C code for the filter has been generated and saved as 'filter.c'.")
