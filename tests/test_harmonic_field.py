"""
Unit tests for HarmonicField class
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from uhh import HarmonicField


class TestHarmonicField(unittest.TestCase):
    """Test cases for HarmonicField class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.hf_2d = HarmonicField(dimensions=2)
        self.hf_3d = HarmonicField(dimensions=3)
        
    def test_initialization(self):
        """Test HarmonicField initialization"""
        self.assertEqual(self.hf_2d.dimensions, 2)
        self.assertEqual(self.hf_3d.dimensions, 3)
        
    def test_compute_2d_harmonic_basic(self):
        """Test basic 2D harmonic computation"""
        x = np.linspace(0, 2*np.pi, 50)
        y = np.linspace(0, 2*np.pi, 50)
        X, Y = np.meshgrid(x, y)
        
        modes = [(1, 1)]
        field = self.hf_2d.compute_2d_harmonic(X, Y, modes)
        
        # Check output shape
        self.assertEqual(field.shape, X.shape)
        
        # Check that values are bounded for cosine
        self.assertTrue(np.all(field >= -1.1))
        self.assertTrue(np.all(field <= 1.1))
        
    def test_compute_2d_harmonic_with_amplitudes(self):
        """Test 2D harmonic with custom amplitudes"""
        x = np.linspace(0, 2*np.pi, 50)
        y = np.linspace(0, 2*np.pi, 50)
        X, Y = np.meshgrid(x, y)
        
        modes = [(1, 0), (0, 1)]
        amplitudes = [2.0, 3.0]
        field = self.hf_2d.compute_2d_harmonic(X, Y, modes, amplitudes)
        
        # Field should be bounded by sum of amplitudes
        self.assertTrue(np.all(np.abs(field) <= sum(amplitudes) + 0.1))
        
    def test_compute_3d_harmonic(self):
        """Test 3D harmonic computation using spherical harmonics"""
        x = np.linspace(-1, 1, 20)
        y = np.linspace(-1, 1, 20)
        z = np.zeros((20, 20))
        X, Y = np.meshgrid(x, y)
        Z = z
        
        field = self.hf_3d.compute_3d_harmonic(X, Y, Z, l_max=2)
        
        # Check output shape
        self.assertEqual(field.shape, X.shape)
        
        # Check that field is real-valued
        self.assertTrue(np.all(np.isreal(field)))
        
    def test_compute_wave_superposition(self):
        """Test wave superposition"""
        x = np.linspace(-5, 5, 30)
        y = np.linspace(-5, 5, 30)
        X, Y = np.meshgrid(x, y)
        
        sources = [(0, 0, 1.0, 1.0, 0)]
        field = self.hf_2d.compute_wave_superposition(X, Y, sources, time=0)
        
        # Check output shape
        self.assertEqual(field.shape, X.shape)
        
        # At the source location, check expected behavior
        # (approximate center of grid)
        center_idx = field.shape[0] // 2
        self.assertAlmostEqual(field[center_idx, center_idx], 1.0, places=1)
        
    def test_compute_gradient(self):
        """Test gradient computation"""
        field = np.array([[1, 2, 3],
                         [4, 5, 6],
                         [7, 8, 9]], dtype=float)
        
        gradients = self.hf_2d.compute_gradient(field, dx=1.0)
        
        # Should return tuple of gradients
        self.assertIsInstance(gradients, tuple)
        self.assertEqual(len(gradients), 2)
        
        # Check gradient shapes
        for grad in gradients:
            self.assertEqual(grad.shape, field.shape)
            
    def test_compute_laplacian(self):
        """Test Laplacian computation"""
        # Create a simple field
        x = np.linspace(-2, 2, 30)
        y = np.linspace(-2, 2, 30)
        X, Y = np.meshgrid(x, y)
        field = np.sin(X) * np.sin(Y)
        
        dx = x[1] - x[0]
        laplacian = self.hf_2d.compute_laplacian(field, dx)
        
        # Check output shape
        self.assertEqual(laplacian.shape, field.shape)
        
        # For sin(x)*sin(y), Laplacian should be approximately -2*sin(x)*sin(y)
        # (within numerical errors)
        expected = -2 * field
        # Check correlation rather than exact values due to numerical derivatives
        correlation = np.corrcoef(laplacian.flatten(), expected.flatten())[0, 1]
        self.assertGreater(correlation, 0.95)
        
    def test_compute_energy(self):
        """Test energy computation"""
        field = np.array([[1, 2], [3, 4]], dtype=float)
        energy = self.hf_2d.compute_energy(field)
        
        # Energy should be sum of squares
        expected_energy = 1 + 4 + 9 + 16
        self.assertEqual(energy, expected_energy)
        
    def test_apply_boundary_condition_2d(self):
        """Test applying boundary conditions in 2D"""
        field = np.ones((5, 5))
        
        # Apply Dirichlet boundary condition
        result = self.hf_2d.apply_boundary_condition(field, "dirichlet", 0.0)
        
        # Check boundaries are zero
        self.assertTrue(np.all(result[0, :] == 0))
        self.assertTrue(np.all(result[-1, :] == 0))
        self.assertTrue(np.all(result[:, 0] == 0))
        self.assertTrue(np.all(result[:, -1] == 0))
        
        # Check interior is unchanged
        self.assertTrue(np.all(result[1:-1, 1:-1] == 1))
        
    def test_wave_superposition_multiple_sources(self):
        """Test wave superposition with multiple sources"""
        x = np.linspace(-5, 5, 40)
        y = np.linspace(-5, 5, 40)
        X, Y = np.meshgrid(x, y)
        
        sources = [
            (0, 0, 1.0, 1.0, 0),
            (2, 2, 0.5, 1.0, 0)
        ]
        
        field = self.hf_2d.compute_wave_superposition(X, Y, sources, time=0)
        
        # Check output shape
        self.assertEqual(field.shape, X.shape)
        
        # Field should be bounded
        self.assertTrue(np.all(np.abs(field) <= 2.0))
        

class TestHarmonicFieldEdgeCases(unittest.TestCase):
    """Test edge cases for HarmonicField"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.hf = HarmonicField(dimensions=2)
        
    def test_empty_modes(self):
        """Test with empty mode list"""
        x = np.linspace(0, 1, 10)
        y = np.linspace(0, 1, 10)
        X, Y = np.meshgrid(x, y)
        
        field = self.hf.compute_2d_harmonic(X, Y, [])
        
        # Should return zero field
        self.assertTrue(np.all(field == 0))
        
    def test_single_point(self):
        """Test with single point"""
        X = np.array([[0]])
        Y = np.array([[0]])
        
        modes = [(1, 1)]
        field = self.hf.compute_2d_harmonic(X, Y, modes)
        
        # Should work without error
        self.assertEqual(field.shape, (1, 1))


if __name__ == '__main__':
    unittest.main()
