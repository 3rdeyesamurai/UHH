"""
Time Evolution of Harmonic Fields
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
    x = np.linspace(-3*np.pi, 3*np.pi, 100)
    y = np.linspace(-3*np.pi, 3*np.pi, 100)
    X, Y = np.meshgrid(x, y)
    
    # Define wave sources
    sources = [
        (0, 0, 1.0, 1.0, 0),
        (2, 2, 0.7, 1.2, 0),
        (-2, -2, 0.7, 0.8, 0)
    ]
    
    print("Computing time evolution of wave superposition...")
    
    # Generate frames for different time steps
    time_steps = np.linspace(0, 2*np.pi, 20)
    fields = []
    
    for t in time_steps:
        field = hf.compute_wave_superposition(X, Y, sources, time=t)
        fields.append(field)
    
    print(f"Generated {len(fields)} frames")
    
    # Display a few key frames
    for i, idx in enumerate([0, 5, 10, 15]):
        print(f"Displaying frame {idx}...")
        viz.plot_2d_field(fields[idx], X, Y,
                         title=f"Wave Evolution - t = {time_steps[idx]:.2f}",
                         cmap="twilight",
                         show_contours=False)
    
    print("\nTime evolution visualization complete!")
    print("Note: Full animation can be created using plot_animation_frames method")


if __name__ == "__main__":
    main()
