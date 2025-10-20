"""
Comprehensive Demo of UHH Scientific Visualization Tool

This script demonstrates all major features of the Unified Harmonic Helper.
Outputs are saved to /tmp for easy inspection.
"""

import numpy as np
import sys
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from uhh import HarmonicField, HarmonicVisualizer


def demo_2d_harmonic():
    """Demonstrate 2D harmonic field computation and visualization"""
    print("=" * 60)
    print("DEMO 1: 2D Harmonic Fields")
    print("=" * 60)
    
    hf = HarmonicField(dimensions=2)
    viz = HarmonicVisualizer(backend="matplotlib")
    
    # Create coordinate grid
    x = np.linspace(-np.pi, np.pi, 100)
    y = np.linspace(-np.pi, np.pi, 100)
    X, Y = np.meshgrid(x, y)
    
    # Example 1: Simple harmonic modes
    modes = [(1, 1), (2, 1), (1, 2)]
    amplitudes = [1.0, 0.5, 0.5]
    field = hf.compute_2d_harmonic(X, Y, modes, amplitudes)
    
    print(f"✓ Computed 2D harmonic field with modes: {modes}")
    print(f"  Field shape: {field.shape}")
    print(f"  Field range: [{field.min():.3f}, {field.max():.3f}]")
    print(f"  Total energy: {hf.compute_energy(field):.2f}")
    
    viz.plot_2d_field(field, X, Y,
                     title="2D Harmonic Field (Fourier Modes)",
                     cmap="RdBu_r",
                     show_contours=True,
                     save_path="/tmp/uhh_2d_harmonic.png")
    print(f"  Saved visualization to: /tmp/uhh_2d_harmonic.png")
    print()


def demo_wave_superposition():
    """Demonstrate wave superposition"""
    print("=" * 60)
    print("DEMO 2: Wave Superposition")
    print("=" * 60)
    
    hf = HarmonicField(dimensions=2)
    viz = HarmonicVisualizer(backend="matplotlib")
    
    x = np.linspace(-3*np.pi, 3*np.pi, 150)
    y = np.linspace(-3*np.pi, 3*np.pi, 150)
    X, Y = np.meshgrid(x, y)
    
    # Multiple wave sources with different frequencies
    sources = [
        (0, 0, 1.0, 1.0, 0),        # (x, y, amplitude, frequency, phase)
        (2, 2, 0.8, 1.2, 0),
        (-2, -2, 0.8, 0.8, 0)
    ]
    
    field = hf.compute_wave_superposition(X, Y, sources, time=0)
    
    print(f"✓ Computed wave superposition from {len(sources)} sources")
    print(f"  Field shape: {field.shape}")
    print(f"  Field range: [{field.min():.3f}, {field.max():.3f}]")
    
    viz.plot_2d_field(field, X, Y,
                     title="Wave Superposition from Multiple Sources",
                     cmap="twilight",
                     show_contours=False,
                     save_path="/tmp/uhh_wave_superposition.png")
    print(f"  Saved visualization to: /tmp/uhh_wave_superposition.png")
    print()


def demo_3d_surface():
    """Demonstrate 3D surface visualization"""
    print("=" * 60)
    print("DEMO 3: 3D Surface Visualization")
    print("=" * 60)
    
    hf = HarmonicField(dimensions=2)
    viz = HarmonicVisualizer(backend="matplotlib")
    
    x = np.linspace(-2*np.pi, 2*np.pi, 80)
    y = np.linspace(-2*np.pi, 2*np.pi, 80)
    X, Y = np.meshgrid(x, y)
    
    modes = [(1, 1), (2, 2)]
    field = hf.compute_2d_harmonic(X, Y, modes)
    
    print(f"✓ Creating 3D surface plot")
    print(f"  Field shape: {field.shape}")
    
    viz.plot_3d_surface(field, X, Y,
                       title="3D Harmonic Field Surface",
                       cmap="plasma",
                       save_path="/tmp/uhh_3d_surface.png")
    print(f"  Saved visualization to: /tmp/uhh_3d_surface.png")
    print()


def demo_gradient_field():
    """Demonstrate gradient and vector field visualization"""
    print("=" * 60)
    print("DEMO 4: Gradient and Vector Fields")
    print("=" * 60)
    
    hf = HarmonicField(dimensions=2)
    viz = HarmonicVisualizer(backend="matplotlib")
    
    x = np.linspace(-2*np.pi, 2*np.pi, 60)
    y = np.linspace(-2*np.pi, 2*np.pi, 60)
    X, Y = np.meshgrid(x, y)
    
    modes = [(1, 0), (0, 1), (1, 1)]
    field = hf.compute_2d_harmonic(X, Y, modes)
    
    # Compute gradient
    dx = x[1] - x[0]
    grad_y, grad_x = hf.compute_gradient(field, dx)
    
    print(f"✓ Computed gradient field")
    print(f"  Gradient X range: [{grad_x.min():.3f}, {grad_x.max():.3f}]")
    print(f"  Gradient Y range: [{grad_y.min():.3f}, {grad_y.max():.3f}]")
    
    viz.plot_vector_field(grad_x, grad_y, X, Y,
                         title="Gradient Field of Harmonic Function",
                         scale=0.3,
                         save_path="/tmp/uhh_gradient.png")
    print(f"  Saved visualization to: /tmp/uhh_gradient.png")
    
    # Compute Laplacian
    laplacian = hf.compute_laplacian(field, dx)
    
    print(f"✓ Computed Laplacian")
    print(f"  Laplacian range: [{laplacian.min():.3f}, {laplacian.max():.3f}]")
    
    viz.plot_2d_field(laplacian, X, Y,
                     title="Laplacian of Harmonic Field",
                     cmap="seismic",
                     show_contours=True,
                     save_path="/tmp/uhh_laplacian.png")
    print(f"  Saved visualization to: /tmp/uhh_laplacian.png")
    print()


def demo_spherical_harmonics():
    """Demonstrate 3D harmonic field using spherical harmonics"""
    print("=" * 60)
    print("DEMO 5: 3D Spherical Harmonics")
    print("=" * 60)
    
    hf = HarmonicField(dimensions=3)
    viz = HarmonicVisualizer(backend="matplotlib")
    
    # Create a 2D slice through 3D space (z=0 plane)
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    
    # Compute 3D harmonic field
    field_3d = hf.compute_3d_harmonic(X, Y, Z, l_max=3)
    
    print(f"✓ Computed 3D harmonic field (spherical harmonics, l_max=3)")
    print(f"  Field shape: {field_3d.shape}")
    print(f"  Field range: [{field_3d.min():.3f}, {field_3d.max():.3f}]")
    print(f"  Total energy: {hf.compute_energy(field_3d):.2f}")
    
    viz.plot_2d_field(field_3d, X, Y,
                     title="3D Harmonic Field (Spherical Harmonics) - Slice at z=0",
                     cmap="coolwarm",
                     show_contours=True,
                     save_path="/tmp/uhh_spherical_harmonics.png")
    print(f"  Saved visualization to: /tmp/uhh_spherical_harmonics.png")
    print()


def demo_boundary_conditions():
    """Demonstrate boundary conditions"""
    print("=" * 60)
    print("DEMO 6: Boundary Conditions")
    print("=" * 60)
    
    hf = HarmonicField(dimensions=2)
    viz = HarmonicVisualizer(backend="matplotlib")
    
    x = np.linspace(-np.pi, np.pi, 60)
    y = np.linspace(-np.pi, np.pi, 60)
    X, Y = np.meshgrid(x, y)
    
    modes = [(1, 1), (2, 2)]
    field = hf.compute_2d_harmonic(X, Y, modes)
    
    # Apply Dirichlet boundary condition
    field_bc = hf.apply_boundary_condition(field, "dirichlet", 0.0)
    
    print(f"✓ Applied Dirichlet boundary condition (value=0)")
    print(f"  Original field energy: {hf.compute_energy(field):.2f}")
    print(f"  Field with BC energy: {hf.compute_energy(field_bc):.2f}")
    
    viz.plot_2d_field(field_bc, X, Y,
                     title="Harmonic Field with Dirichlet BC",
                     cmap="viridis",
                     show_contours=True,
                     save_path="/tmp/uhh_boundary_conditions.png")
    print(f"  Saved visualization to: /tmp/uhh_boundary_conditions.png")
    print()


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 60)
    print("UHH - Unified Harmonic Helper")
    print("Scientific Visualization Tool Demonstration")
    print("=" * 60 + "\n")
    
    try:
        demo_2d_harmonic()
        demo_wave_superposition()
        demo_3d_surface()
        demo_gradient_field()
        demo_spherical_harmonics()
        demo_boundary_conditions()
        
        print("=" * 60)
        print("All demonstrations completed successfully!")
        print("=" * 60)
        print("\nGenerated files in /tmp/:")
        print("  - uhh_2d_harmonic.png")
        print("  - uhh_wave_superposition.png")
        print("  - uhh_3d_surface.png")
        print("  - uhh_gradient.png")
        print("  - uhh_laplacian.png")
        print("  - uhh_spherical_harmonics.png")
        print("  - uhh_boundary_conditions.png")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
