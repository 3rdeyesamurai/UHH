"""
Harmonic Field computation module for the Unified Harmonic Field Framework.
This module provides tools for computing and analyzing harmonic fields.
"""

import numpy as np
from scipy.special import sph_harm
from typing import Tuple, Optional, Callable


class HarmonicField:
    """
    A class for computing and manipulating harmonic fields.
    
    Harmonic fields are solutions to Laplace's equation and can be represented
    using spherical harmonics, Fourier series, or other harmonic basis functions.
    """
    
    def __init__(self, dimensions: int = 2):
        """
        Initialize the HarmonicField.
        
        Args:
            dimensions: Number of spatial dimensions (2 or 3)
        """
        self.dimensions = dimensions
        
    def compute_2d_harmonic(
        self,
        x: np.ndarray,
        y: np.ndarray,
        modes: list,
        amplitudes: Optional[list] = None
    ) -> np.ndarray:
        """
        Compute 2D harmonic field using Fourier series.
        
        Args:
            x: X-coordinate grid
            y: Y-coordinate grid
            modes: List of (m, n) mode tuples
            amplitudes: Amplitudes for each mode (default: all 1.0)
            
        Returns:
            2D array of field values
        """
        if amplitudes is None:
            amplitudes = [1.0] * len(modes)
            
        field = np.zeros_like(x, dtype=float)
        for (m, n), amp in zip(modes, amplitudes):
            field += amp * np.cos(m * x) * np.cos(n * y)
            
        return field
    
    def compute_3d_harmonic(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        l_max: int = 3
    ) -> np.ndarray:
        """
        Compute 3D harmonic field using spherical harmonics.
        
        Args:
            x, y, z: Coordinate grids in Cartesian coordinates
            l_max: Maximum degree of spherical harmonics
            
        Returns:
            3D array of field values
        """
        # Convert to spherical coordinates
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arccos(np.clip(z / (r + 1e-10), -1, 1))
        phi = np.arctan2(y, x)
        
        field = np.zeros_like(x, dtype=complex)
        
        for l in range(l_max + 1):
            for m in range(-l, l + 1):
                Y_lm = sph_harm(m, l, phi, theta)
                # Combine with radial function
                R_l = r**l / (1 + r**(2*l + 1))
                field += Y_lm * R_l
                
        return np.real(field)
    
    def compute_wave_superposition(
        self,
        x: np.ndarray,
        y: np.ndarray,
        sources: list,
        time: float = 0.0
    ) -> np.ndarray:
        """
        Compute superposition of harmonic waves from multiple sources.
        
        Args:
            x, y: Coordinate grids
            sources: List of (x0, y0, amplitude, frequency, phase) tuples
            time: Time parameter for wave evolution
            
        Returns:
            2D array of field values
        """
        field = np.zeros_like(x)
        
        for x0, y0, amp, freq, phase in sources:
            r = np.sqrt((x - x0)**2 + (y - y0)**2)
            field += amp * np.cos(freq * r - 2 * np.pi * freq * time + phase)
            
        return field
    
    def compute_gradient(self, field: np.ndarray, dx: float = 1.0) -> Tuple[np.ndarray, ...]:
        """
        Compute gradient of a field.
        
        Args:
            field: Input field array
            dx: Grid spacing
            
        Returns:
            Tuple of gradient components
        """
        return tuple(np.gradient(field, dx))
    
    def compute_laplacian(self, field: np.ndarray, dx: float = 1.0) -> np.ndarray:
        """
        Compute Laplacian of a field.
        
        Args:
            field: Input field array
            dx: Grid spacing
            
        Returns:
            Laplacian of the field
        """
        laplacian = np.zeros_like(field)
        gradients = self.compute_gradient(field, dx)
        
        for i, grad in enumerate(gradients):
            laplacian += np.gradient(grad, dx, axis=i)
            
        return laplacian
    
    def compute_energy(self, field: np.ndarray) -> float:
        """
        Compute total energy of the harmonic field.
        
        Args:
            field: Input field array
            
        Returns:
            Total energy (sum of squared field values)
        """
        return np.sum(field**2)
    
    def apply_boundary_condition(
        self,
        field: np.ndarray,
        boundary_type: str = "dirichlet",
        boundary_value: float = 0.0
    ) -> np.ndarray:
        """
        Apply boundary conditions to the field.
        
        Args:
            field: Input field array
            boundary_type: Type of boundary condition ("dirichlet" or "neumann")
            boundary_value: Value at the boundary
            
        Returns:
            Field with boundary conditions applied
        """
        result = field.copy()
        
        if boundary_type.lower() == "dirichlet":
            # Set boundary values
            if field.ndim == 2:
                result[0, :] = boundary_value
                result[-1, :] = boundary_value
                result[:, 0] = boundary_value
                result[:, -1] = boundary_value
            elif field.ndim == 3:
                result[0, :, :] = boundary_value
                result[-1, :, :] = boundary_value
                result[:, 0, :] = boundary_value
                result[:, -1, :] = boundary_value
                result[:, :, 0] = boundary_value
                result[:, :, -1] = boundary_value
                
        return result
