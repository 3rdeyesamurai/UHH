"""
Basic 2D Harmonic Field Visualization Example
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from uhh import HarmonicField, HarmonicVisualizer


def main():
    # Initialize harmonic field and visualizer
    hf = HarmonicField(dimensions=2)
    viz = HarmonicVisualizer(backend="matplotlib")
    
    # Create coordinate grid
    x = np.linspace(-np.pi, np.pi, 100)
    y = np.linspace(-np.pi, np.pi, 100)
    X, Y = np.meshgrid(x, y)
    
    # Example 1: Simple harmonic modes
    print("Example 1: Simple Harmonic Modes")
    modes = [(1, 1), (2, 1), (1, 2)]
    amplitudes = [1.0, 0.5, 0.5]
    field = hf.compute_2d_harmonic(X, Y, modes, amplitudes)
    
    viz.plot_2d_field(field, X, Y, 
                     title="2D Harmonic Field (Fourier Modes)",
                     cmap="RdBu_r",
                     show_contours=True)
    
    # Example 2: Wave superposition
    print("Example 2: Wave Superposition from Multiple Sources")
    sources = [
        (0, 0, 1.0, 2.0, 0),        # (x, y, amplitude, frequency, phase)
        (1, 1, 0.8, 1.5, np.pi/4),
        (-1, -1, 0.8, 1.5, -np.pi/4)
    ]
    field_waves = hf.compute_wave_superposition(X, Y, sources, time=0)
    
    viz.plot_2d_field(field_waves, X, Y,
                     title="Wave Superposition",
                     cmap="viridis",
                     show_contours=True)
    
    # Example 3: 3D Surface plot
    print("Example 3: 3D Surface Visualization")
    viz.plot_3d_surface(field, X, Y,
                       title="3D Harmonic Field Surface",
                       cmap="plasma")
    
    print("\nVisualization complete!")


if __name__ == "__main__":
    main()
