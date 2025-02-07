import numpy as np
import matplotlib.pyplot as plt

# Define the zeros and poles
zeros = [0.5 + 0.5j]
poles = [0.5 - 0.5j]

# Set up the plot
plt.figure(figsize=(8, 8))
ax = plt.subplot(111)

# Plot the unit circle
theta = np.linspace(0, 2 * np.pi, 100)
unit_circle = np.exp(1j * theta)
plt.plot(unit_circle.real, unit_circle.imag, 'k--', label='Unit Circle')

# Plot zeros
for zero in zeros:
    plt.plot(zero.real, zero.imag, 'ro', label='Zero' if zero == zeros[0] else "")
    
# Plot poles
for pole in poles:
    plt.plot(pole.real, pole.imag, 'bx', label='Pole' if pole == poles[0] else "")

# Set limits and labels
plt.xlim(-1, 2)
plt.ylim(-2, 2)
plt.axhline(0, color='grey', lw=0.5)
plt.axvline(0, color='grey', lw=0.5)
plt.grid()
plt.title('Zeros and Poles in the Z-Plane')
plt.xlabel('Real Part')
plt.ylabel('Imaginary Part')
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()