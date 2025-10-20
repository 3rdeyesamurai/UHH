"""
Gradient and Vector Field Visualization Example
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from uhh import HarmonicField, HarmonicVisualizer


def main():
    # Initialize
    hf = HarmonicField(dimensions=2)
    viz = HarmonicVisualizer(backend="matplotlib")
    
    # Create coordinate grid
    x = np.linspace(-2*np.pi, 2*np.pi, 80)
    y = np.linspace(-2*np.pi, 2*np.pi, 80)
    X, Y = np.meshgrid(x, y)
    
    # Create a harmonic field
    modes = [(1, 0), (0, 1), (1, 1)]
    amplitudes = [1.0, 1.0, 0.5]
    field = hf.compute_2d_harmonic(X, Y, modes, amplitudes)
    
    print("Computing gradient field...")
    # Compute gradient
    dx = x[1] - x[0]
    grad_y, grad_x = hf.compute_gradient(field, dx)
    
    # Visualize the gradient as a vector field
    print("Visualizing gradient vector field...")
    viz.plot_vector_field(grad_x, grad_y, X, Y,
                         title="Gradient Field of Harmonic Function",
                         scale=0.5)
    
    # Compute and visualize Laplacian
    print("Computing and visualizing Laplacian...")
    laplacian = hf.compute_laplacian(field, dx)
    
    viz.plot_2d_field(laplacian, X, Y,
                     title="Laplacian of Harmonic Field",
                     cmap="seismic",
                     show_contours=True)
    
    print("\nGradient visualization complete!")


if __name__ == "__main__":
    main()
