# UHH Usage Guide

This guide provides detailed examples and usage patterns for the Unified Harmonic Helper.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Computing Harmonic Fields](#computing-harmonic-fields)
4. [Visualization](#visualization)
5. [Advanced Features](#advanced-features)
6. [Common Use Cases](#common-use-cases)

## Installation

### Requirements

- Python 3.7 or higher
- NumPy 1.21.0 or higher
- Matplotlib 3.5.0 or higher
- SciPy 1.7.0 or higher
- Plotly 5.0.0 or higher

### Install from source

```bash
git clone https://github.com/3rdeyesamurai/UHH.git
cd UHH
pip install -e .
```

### Install dependencies only

```bash
pip install -r requirements.txt
```

## Basic Usage

### Import the library

```python
import numpy as np
from uhh import HarmonicField, HarmonicVisualizer
```

### Create a simple harmonic field

```python
# Initialize
hf = HarmonicField(dimensions=2)
viz = HarmonicVisualizer(backend="matplotlib")

# Create coordinate grid
x = np.linspace(-np.pi, np.pi, 100)
y = np.linspace(-np.pi, np.pi, 100)
X, Y = np.meshgrid(x, y)

# Define modes and compute field
modes = [(1, 1), (2, 1)]
field = hf.compute_2d_harmonic(X, Y, modes)

# Visualize
viz.plot_2d_field(field, X, Y, title="My Harmonic Field")
```

## Computing Harmonic Fields

### 2D Harmonic Fields (Fourier Series)

2D harmonic fields are computed using Fourier series:

```python
hf = HarmonicField(dimensions=2)

# Define modes (m, n) and amplitudes
modes = [(1, 0), (0, 1), (1, 1), (2, 2)]
amplitudes = [1.0, 1.0, 0.7, 0.3]

field = hf.compute_2d_harmonic(X, Y, modes, amplitudes)
```

Each mode (m, n) contributes: `A * cos(m*x) * cos(n*y)`

### 3D Harmonic Fields (Spherical Harmonics)

3D fields use spherical harmonics up to degree `l_max`:

```python
hf = HarmonicField(dimensions=3)

# Create 3D coordinate grid
x = np.linspace(-2, 2, 50)
y = np.linspace(-2, 2, 50)
z = np.linspace(-2, 2, 50)
X, Y, Z = np.meshgrid(x, y, z)

# Compute field (l_max controls complexity)
field_3d = hf.compute_3d_harmonic(X, Y, Z, l_max=3)
```

### Wave Superposition

Simulate interference from multiple wave sources:

```python
# Define sources: (x_pos, y_pos, amplitude, frequency, phase)
sources = [
    (0, 0, 1.0, 2.0, 0),           # Center source
    (2, 2, 0.8, 1.5, np.pi/4),     # Top-right source
    (-2, -2, 0.8, 1.8, -np.pi/4),  # Bottom-left source
]

# Compute at different time steps
for t in np.linspace(0, 2*np.pi, 10):
    field = hf.compute_wave_superposition(X, Y, sources, time=t)
    # Process or visualize field
```

## Visualization

### 2D Heatmaps

```python
viz = HarmonicVisualizer(backend="matplotlib")

viz.plot_2d_field(
    field, X, Y,
    title="My Field",
    cmap="viridis",        # Color map
    show_contours=True,    # Overlay contour lines
    save_path="output.png" # Save to file
)
```

### 3D Surface Plots

```python
viz.plot_3d_surface(
    field, X, Y,
    title="3D Surface",
    cmap="plasma",
    save_path="surface.png"
)
```

### Vector Fields

Visualize gradients or other vector quantities:

```python
# Compute gradient
dx = x[1] - x[0]
grad_y, grad_x = hf.compute_gradient(field, dx)

# Plot as vector field
viz.plot_vector_field(
    grad_x, grad_y, X, Y,
    title="Gradient Field",
    scale=0.5,  # Arrow scaling
    save_path="gradient.png"
)
```

### Interactive Plots with Plotly

```python
viz = HarmonicVisualizer(backend="plotly")

# Creates interactive HTML plot
viz.plot_2d_field(
    field, X, Y,
    title="Interactive Field",
    save_path="interactive.html"
)
```

## Advanced Features

### Gradient and Laplacian

```python
# Compute gradient
dx = x[1] - x[0]
grad_y, grad_x = hf.compute_gradient(field, dx)

# Compute Laplacian (∇²φ)
laplacian = hf.compute_laplacian(field, dx)

# For harmonic fields, Laplacian should be close to zero
print(f"Max Laplacian: {np.max(np.abs(laplacian))}")
```

### Energy Calculation

```python
energy = hf.compute_energy(field)
print(f"Total field energy: {energy}")
```

### Boundary Conditions

Apply Dirichlet (fixed value) boundary conditions:

```python
field_bc = hf.apply_boundary_condition(
    field,
    boundary_type="dirichlet",
    boundary_value=0.0
)
```

### Time Evolution Animations

```python
# Generate frames
time_steps = np.linspace(0, 2*np.pi, 30)
fields = []

for t in time_steps:
    field = hf.compute_wave_superposition(X, Y, sources, time=t)
    fields.append(field)

# Create animation
viz.plot_animation_frames(
    fields, X, Y,
    title="Wave Evolution",
    interval=100,  # ms between frames
    save_path="animation.gif"
)
```

## Common Use Cases

### 1. Electromagnetic Field Simulation

```python
# Define charge locations and strengths
charges = [
    (0, 0, 1.0, 1.0, 0),      # Positive charge
    (1, 0, -0.8, 1.0, np.pi)  # Negative charge
]

field = hf.compute_wave_superposition(X, Y, charges, time=0)
viz.plot_2d_field(field, X, Y, title="Electric Field", cmap="RdBu_r")
```

### 2. Acoustic Wave Propagation

```python
# Sound sources with different frequencies
speakers = [
    (-1, 0, 1.0, 440, 0),   # 440 Hz (A note)
    (1, 0, 1.0, 554, 0),    # 554 Hz (C# note)
]

field = hf.compute_wave_superposition(X, Y, speakers, time=0)
viz.plot_2d_field(field, X, Y, title="Acoustic Field", cmap="viridis")
```

### 3. Quantum Mechanics Wavefunctions

```python
# Spherical harmonics for atomic orbitals
hf_3d = HarmonicField(dimensions=3)

# Create 2D slice (z=0)
field_orbital = hf_3d.compute_3d_harmonic(X, Y, Z, l_max=2)

viz.plot_2d_field(field_orbital, X, Y,
                 title="Atomic Orbital (l=2)",
                 cmap="coolwarm")
```

### 4. Heat Distribution Analysis

```python
# Initial heat distribution
modes = [(1, 1), (2, 1), (1, 2)]
field = hf.compute_2d_harmonic(X, Y, modes)

# Apply boundary conditions (cold walls)
field = hf.apply_boundary_condition(field, "dirichlet", 0.0)

# Visualize with contours
viz.plot_2d_field(field, X, Y,
                 title="Heat Distribution",
                 cmap="hot",
                 show_contours=True)
```

### 5. Signal Processing

```python
# Frequency decomposition
frequencies = [1, 2, 3, 5, 8]  # Harmonics
modes = [(f, 0) for f in frequencies]
amplitudes = [1/f for f in frequencies]  # Decreasing amplitude

field = hf.compute_2d_harmonic(X, Y, modes, amplitudes)
viz.plot_2d_field(field, X, Y, title="Frequency Spectrum")
```

## Tips and Best Practices

### Grid Resolution

- Use 50-100 points per dimension for quick visualization
- Use 200-500 points for publication-quality figures
- Higher resolution = more memory and computation time

```python
# Quick preview
x = np.linspace(-np.pi, np.pi, 50)

# High quality
x = np.linspace(-np.pi, np.pi, 200)
```

### Colormap Selection

- **Sequential**: `viridis`, `plasma`, `inferno` - for magnitude data
- **Diverging**: `RdBu_r`, `coolwarm`, `seismic` - for signed data
- **Cyclic**: `twilight`, `hsv` - for periodic data (phases)

### Performance Optimization

```python
# Use smaller grids for iteration
x_small = np.linspace(-np.pi, np.pi, 30)

# Then use full resolution for final output
x_full = np.linspace(-np.pi, np.pi, 200)
```

### Saving Outputs

```python
# Matplotlib: PNG, PDF, SVG
viz.plot_2d_field(field, save_path="output.png")
viz.plot_2d_field(field, save_path="output.pdf")

# Plotly: HTML (interactive)
viz_plotly = HarmonicVisualizer(backend="plotly")
viz_plotly.plot_2d_field(field, save_path="interactive.html")
```

## Troubleshooting

### Import Errors

If you get import errors, ensure all dependencies are installed:

```bash
pip install numpy matplotlib scipy plotly pandas
```

### Memory Issues

For large grids, reduce resolution or process in chunks:

```python
# Instead of 500x500
# Use 200x200 or split into smaller regions
```

### Visualization Not Showing

If plots don't appear:

```python
import matplotlib.pyplot as plt

# Add this after visualization calls
plt.show()

# Or save to file
viz.plot_2d_field(field, save_path="output.png")
```

## Further Reading

- See `examples/` directory for complete working examples
- Run `python examples/demo.py` for comprehensive demonstration
- Check API documentation in `README.md`
- Review test cases in `tests/` for usage patterns

## Getting Help

- GitHub Issues: https://github.com/3rdeyesamurai/UHH/issues
- Review examples in `examples/` directory
- Check test cases in `tests/` for more patterns
