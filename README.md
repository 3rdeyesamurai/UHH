# UHH - Unified Harmonic Helper

A comprehensive scientific visualization tool for the Unified Harmonic Field Framework. This package provides powerful tools for computing and visualizing harmonic fields in 2D and 3D, including Fourier modes, spherical harmonics, wave superposition, and field analysis.

## Features

- **2D Harmonic Fields**: Compute harmonic fields using Fourier series with customizable modes and amplitudes
- **3D Harmonic Fields**: Generate 3D harmonic fields using spherical harmonics
- **Wave Superposition**: Simulate and visualize wave interference from multiple sources
- **Field Analysis**: Compute gradients, Laplacians, and energy of harmonic fields
- **Advanced Visualization**: 
  - 2D heatmaps with contours
  - 3D surface plots
  - Vector field visualization
  - Time evolution animations
- **Dual Backend Support**: Choose between matplotlib (static) or plotly (interactive) visualization
- **Boundary Conditions**: Apply Dirichlet and Neumann boundary conditions

## Installation

### From source:

```bash
git clone https://github.com/3rdeyesamurai/UHH.git
cd UHH
pip install -e .
```

### Dependencies:

```bash
pip install -r requirements.txt
```

Required packages:
- numpy >= 1.21.0
- matplotlib >= 3.5.0
- scipy >= 1.7.0
- plotly >= 5.0.0
- pandas >= 1.3.0

## Quick Start

### Basic 2D Harmonic Field

```python
import numpy as np
from uhh import HarmonicField, HarmonicVisualizer

# Initialize
hf = HarmonicField(dimensions=2)
viz = HarmonicVisualizer(backend="matplotlib")

# Create coordinate grid
x = np.linspace(-np.pi, np.pi, 100)
y = np.linspace(-np.pi, np.pi, 100)
X, Y = np.meshgrid(x, y)

# Define harmonic modes and compute field
modes = [(1, 1), (2, 1), (1, 2)]
amplitudes = [1.0, 0.5, 0.5]
field = hf.compute_2d_harmonic(X, Y, modes, amplitudes)

# Visualize
viz.plot_2d_field(field, X, Y, title="2D Harmonic Field")
```

### Wave Superposition

```python
# Define wave sources (x, y, amplitude, frequency, phase)
sources = [
    (0, 0, 1.0, 2.0, 0),
    (1, 1, 0.8, 1.5, np.pi/4),
]

# Compute wave field at time t=0
field = hf.compute_wave_superposition(X, Y, sources, time=0)

# Visualize
viz.plot_2d_field(field, X, Y, title="Wave Superposition")
```

### 3D Harmonic Field

```python
# Create 3D field using spherical harmonics
hf_3d = HarmonicField(dimensions=3)

# Create coordinate grid
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)

# Compute field
field_3d = hf_3d.compute_3d_harmonic(X, Y, Z, l_max=3)

# Visualize as 3D surface
viz.plot_3d_surface(field_3d, X, Y, title="3D Harmonic Field")
```

### Gradient and Vector Fields

```python
# Compute gradient
dx = x[1] - x[0]
grad_y, grad_x = hf.compute_gradient(field, dx)

# Visualize gradient as vector field
viz.plot_vector_field(grad_x, grad_y, X, Y, title="Gradient Field")

# Compute Laplacian
laplacian = hf.compute_laplacian(field, dx)
viz.plot_2d_field(laplacian, X, Y, title="Laplacian")
```

## Examples

The `examples/` directory contains comprehensive examples:

- `basic_2d_visualization.py`: Basic 2D harmonic field visualization
- `gradient_visualization.py`: Gradient and Laplacian computation
- `3d_harmonic_field.py`: 3D spherical harmonic visualization
- `time_evolution.py`: Time evolution of wave fields

Run examples:

```bash
cd examples
python basic_2d_visualization.py
```

## API Reference

### HarmonicField

The `HarmonicField` class provides methods for computing harmonic fields:

**Methods:**
- `compute_2d_harmonic(x, y, modes, amplitudes)`: Compute 2D harmonic field using Fourier series
- `compute_3d_harmonic(x, y, z, l_max)`: Compute 3D harmonic field using spherical harmonics
- `compute_wave_superposition(x, y, sources, time)`: Compute wave superposition from multiple sources
- `compute_gradient(field, dx)`: Compute gradient of a field
- `compute_laplacian(field, dx)`: Compute Laplacian of a field
- `compute_energy(field)`: Compute total energy of the field
- `apply_boundary_condition(field, boundary_type, boundary_value)`: Apply boundary conditions

### HarmonicVisualizer

The `HarmonicVisualizer` class provides visualization methods:

**Methods:**
- `plot_2d_field(field, x, y, ...)`: Plot 2D harmonic field with heatmap
- `plot_3d_surface(field, x, y, ...)`: Plot field as 3D surface
- `plot_vector_field(u, v, x, y, ...)`: Plot vector field (e.g., gradient)
- `plot_animation_frames(fields, ...)`: Create animation of field evolution

**Parameters:**
- `backend`: Choose "matplotlib" for static plots or "plotly" for interactive plots
- `cmap`: Colormap name (e.g., "viridis", "plasma", "RdBu_r")
- `show_contours`: Whether to overlay contour lines
- `save_path`: Path to save the figure

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run individual test files:

```bash
python -m unittest tests.test_harmonic_field
python -m unittest tests.test_visualizer
```

## Applications

The Unified Harmonic Field Framework is useful for:

- **Physics**: Electromagnetic fields, quantum mechanics, wave phenomena
- **Engineering**: Signal processing, acoustics, vibration analysis
- **Mathematics**: Differential equations, harmonic analysis
- **Computer Graphics**: Procedural generation, texture synthesis
- **Data Science**: Feature extraction, pattern recognition

## Mathematical Background

Harmonic fields are solutions to Laplace's equation (∇²φ = 0) and can be represented using various basis functions:

- **Fourier Series (2D)**: φ(x,y) = Σ A_mn cos(mx) cos(ny)
- **Spherical Harmonics (3D)**: φ(r,θ,φ) = Σ R_l(r) Y_lm(θ,φ)
- **Wave Superposition**: φ(x,y,t) = Σ A_i cos(k_i·r - ωt + φ_i)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Authors

- 3rdeyesamurai

## Acknowledgments

Built with NumPy, SciPy, Matplotlib, and Plotly.
