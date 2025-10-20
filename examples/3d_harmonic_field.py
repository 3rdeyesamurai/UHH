"""
3D Harmonic Field Visualization using Spherical Harmonics
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from uhh import HarmonicField, HarmonicVisualizer


def main():
    # Initialize
    hf = HarmonicField(dimensions=3)
    viz = HarmonicVisualizer(backend="matplotlib")
    
    print("Computing 3D harmonic field using spherical harmonics...")
    
    # Create a 2D slice through 3D space (z=0 plane)
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    
    # Compute 3D harmonic field
    field_3d = hf.compute_3d_harmonic(X, Y, Z, l_max=3)
    
    # Visualize the slice
    print("Visualizing 2D slice at z=0...")
    viz.plot_2d_field(field_3d, X, Y,
                     title="3D Harmonic Field (Spherical Harmonics) - Slice at z=0",
                     cmap="coolwarm",
                     show_contours=True)
    
    # Create a 3D surface plot
    print("Creating 3D surface visualization...")
    viz.plot_3d_surface(field_3d, X, Y,
                       title="3D Harmonic Field Surface",
                       cmap="viridis")
    
    # Compute energy
    energy = hf.compute_energy(field_3d)
    print(f"\nTotal field energy: {energy:.4f}")
    
    print("\n3D harmonic field visualization complete!")


if __name__ == "__main__":
    main()
