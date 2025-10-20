"""
Unit tests for HarmonicVisualizer class
"""

import unittest
import numpy as np
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from uhh import HarmonicVisualizer


class TestHarmonicVisualizer(unittest.TestCase):
    """Test cases for HarmonicVisualizer class"""
    
    def test_initialization_matplotlib(self):
        """Test initializing with matplotlib backend"""
        viz = HarmonicVisualizer(backend="matplotlib")
        self.assertEqual(viz.backend, "matplotlib")
        
    def test_initialization_plotly(self):
        """Test initializing with plotly backend"""
        viz = HarmonicVisualizer(backend="plotly")
        self.assertEqual(viz.backend, "plotly")
        
    def test_initialization_invalid_backend(self):
        """Test that invalid backend raises error"""
        with self.assertRaises(ValueError):
            HarmonicVisualizer(backend="invalid")
            
    def test_initialization_case_insensitive(self):
        """Test that backend is case insensitive"""
        viz = HarmonicVisualizer(backend="MATPLOTLIB")
        self.assertEqual(viz.backend, "matplotlib")
        
    @patch('matplotlib.pyplot.show')
    def test_plot_2d_field_matplotlib(self, mock_show):
        """Test 2D field plotting with matplotlib"""
        viz = HarmonicVisualizer(backend="matplotlib")
        field = np.random.rand(10, 10)
        
        # Should not raise an error
        viz.plot_2d_field(field, title="Test Field")
        
        # Verify show was called
        mock_show.assert_called_once()
        
    @patch('matplotlib.pyplot.show')
    def test_plot_2d_field_with_coordinates(self, mock_show):
        """Test 2D field plotting with explicit coordinates"""
        viz = HarmonicVisualizer(backend="matplotlib")
        x = np.linspace(0, 1, 10)
        y = np.linspace(0, 1, 10)
        X, Y = np.meshgrid(x, y)
        field = np.random.rand(10, 10)
        
        viz.plot_2d_field(field, X, Y, title="Test Field with Coords")
        mock_show.assert_called_once()
        
    @patch('matplotlib.pyplot.show')
    def test_plot_3d_surface_matplotlib(self, mock_show):
        """Test 3D surface plotting with matplotlib"""
        viz = HarmonicVisualizer(backend="matplotlib")
        field = np.random.rand(10, 10)
        
        viz.plot_3d_surface(field, title="Test 3D Surface")
        mock_show.assert_called_once()
        
    @patch('matplotlib.pyplot.show')
    def test_plot_vector_field_matplotlib(self, mock_show):
        """Test vector field plotting with matplotlib"""
        viz = HarmonicVisualizer(backend="matplotlib")
        u = np.random.rand(10, 10)
        v = np.random.rand(10, 10)
        
        viz.plot_vector_field(u, v, title="Test Vector Field")
        mock_show.assert_called_once()


class TestVisualizerEdgeCases(unittest.TestCase):
    """Test edge cases for HarmonicVisualizer"""
    
    @patch('matplotlib.pyplot.show')
    def test_small_field(self, mock_show):
        """Test with very small field"""
        viz = HarmonicVisualizer(backend="matplotlib")
        field = np.array([[1, 2], [3, 4]])
        
        # Should work without error
        viz.plot_2d_field(field)
        mock_show.assert_called_once()
        
    @patch('matplotlib.pyplot.show')
    def test_zero_field(self, mock_show):
        """Test with all-zero field"""
        viz = HarmonicVisualizer(backend="matplotlib")
        field = np.zeros((10, 10))
        
        # Should work without error
        viz.plot_2d_field(field)
        mock_show.assert_called_once()


if __name__ == '__main__':
    unittest.main()
