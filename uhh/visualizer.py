"""
Visualization module for harmonic fields.
Provides 2D and 3D plotting capabilities with multiple backends.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from typing import Optional, Tuple, Union


class HarmonicVisualizer:
    """
    A class for visualizing harmonic fields in 2D and 3D.
    Supports both static (matplotlib) and interactive (plotly) visualizations.
    """
    
    def __init__(self, backend: str = "matplotlib"):
        """
        Initialize the visualizer.
        
        Args:
            backend: Plotting backend ("matplotlib" or "plotly")
        """
        self.backend = backend.lower()
        if self.backend not in ["matplotlib", "plotly"]:
            raise ValueError("Backend must be 'matplotlib' or 'plotly'")
    
    def plot_2d_field(
        self,
        field: np.ndarray,
        x: Optional[np.ndarray] = None,
        y: Optional[np.ndarray] = None,
        title: str = "Harmonic Field",
        cmap: str = "viridis",
        show_contours: bool = True,
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot a 2D harmonic field.
        
        Args:
            field: 2D array of field values
            x: X-coordinate array (optional)
            y: Y-coordinate array (optional)
            title: Plot title
            cmap: Colormap name
            show_contours: Whether to show contour lines
            save_path: Path to save the figure (optional)
        """
        if self.backend == "matplotlib":
            self._plot_2d_matplotlib(field, x, y, title, cmap, show_contours, save_path)
        else:
            self._plot_2d_plotly(field, x, y, title, cmap, show_contours, save_path)
    
    def _plot_2d_matplotlib(
        self,
        field: np.ndarray,
        x: Optional[np.ndarray],
        y: Optional[np.ndarray],
        title: str,
        cmap: str,
        show_contours: bool,
        save_path: Optional[str]
    ) -> None:
        """Create 2D plot using matplotlib."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if x is None or y is None:
            im = ax.imshow(field, cmap=cmap, origin='lower', aspect='auto')
        else:
            im = ax.pcolormesh(x, y, field, cmap=cmap, shading='auto')
            
        if show_contours:
            if x is None or y is None:
                ax.contour(field, colors='white', alpha=0.3, linewidths=0.5)
            else:
                ax.contour(x, y, field, colors='white', alpha=0.3, linewidths=0.5)
        
        plt.colorbar(im, ax=ax, label='Field Value')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def _plot_2d_plotly(
        self,
        field: np.ndarray,
        x: Optional[np.ndarray],
        y: Optional[np.ndarray],
        title: str,
        cmap: str,
        show_contours: bool,
        save_path: Optional[str]
    ) -> None:
        """Create 2D plot using plotly."""
        fig = go.Figure()
        
        if x is None:
            x = np.arange(field.shape[1])
        if y is None:
            y = np.arange(field.shape[0])
        
        fig.add_trace(go.Heatmap(
            z=field,
            x=x[0] if x.ndim > 1 else x,
            y=y[:, 0] if y.ndim > 1 else y,
            colorscale=cmap,
            colorbar=dict(title="Field Value")
        ))
        
        if show_contours:
            fig.add_trace(go.Contour(
                z=field,
                x=x[0] if x.ndim > 1 else x,
                y=y[:, 0] if y.ndim > 1 else y,
                showscale=False,
                contours=dict(coloring='none'),
                line=dict(color='white', width=1)
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="X",
            yaxis_title="Y",
            width=800,
            height=700
        )
        
        if save_path:
            fig.write_html(save_path)
        fig.show()
    
    def plot_3d_surface(
        self,
        field: np.ndarray,
        x: Optional[np.ndarray] = None,
        y: Optional[np.ndarray] = None,
        title: str = "3D Harmonic Field",
        cmap: str = "viridis",
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot a 2D field as a 3D surface.
        
        Args:
            field: 2D array of field values
            x: X-coordinate array (optional)
            y: Y-coordinate array (optional)
            title: Plot title
            cmap: Colormap name
            save_path: Path to save the figure (optional)
        """
        if self.backend == "matplotlib":
            self._plot_3d_surface_matplotlib(field, x, y, title, cmap, save_path)
        else:
            self._plot_3d_surface_plotly(field, x, y, title, cmap, save_path)
    
    def _plot_3d_surface_matplotlib(
        self,
        field: np.ndarray,
        x: Optional[np.ndarray],
        y: Optional[np.ndarray],
        title: str,
        cmap: str,
        save_path: Optional[str]
    ) -> None:
        """Create 3D surface plot using matplotlib."""
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        if x is None or y is None:
            x = np.arange(field.shape[1])
            y = np.arange(field.shape[0])
            x, y = np.meshgrid(x, y)
        
        surf = ax.plot_surface(x, y, field, cmap=cmap, alpha=0.9,
                              linewidth=0, antialiased=True)
        
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Field Value')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_zlabel('Field Value', fontsize=12)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def _plot_3d_surface_plotly(
        self,
        field: np.ndarray,
        x: Optional[np.ndarray],
        y: Optional[np.ndarray],
        title: str,
        cmap: str,
        save_path: Optional[str]
    ) -> None:
        """Create 3D surface plot using plotly."""
        if x is None:
            x = np.arange(field.shape[1])
        if y is None:
            y = np.arange(field.shape[0])
        
        fig = go.Figure(data=[go.Surface(
            z=field,
            x=x[0] if x.ndim > 1 else x,
            y=y[:, 0] if y.ndim > 1 else y,
            colorscale=cmap,
            colorbar=dict(title="Field Value")
        )])
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Field Value"
            ),
            width=900,
            height=700
        )
        
        if save_path:
            fig.write_html(save_path)
        fig.show()
    
    def plot_vector_field(
        self,
        u: np.ndarray,
        v: np.ndarray,
        x: Optional[np.ndarray] = None,
        y: Optional[np.ndarray] = None,
        title: str = "Vector Field",
        scale: float = 1.0,
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot a 2D vector field (e.g., gradient field).
        
        Args:
            u: X-component of vectors
            v: Y-component of vectors
            x: X-coordinate array (optional)
            y: Y-coordinate array (optional)
            title: Plot title
            scale: Arrow scaling factor
            save_path: Path to save the figure (optional)
        """
        if self.backend == "matplotlib":
            self._plot_vector_field_matplotlib(u, v, x, y, title, scale, save_path)
        else:
            self._plot_vector_field_plotly(u, v, x, y, title, scale, save_path)
    
    def _plot_vector_field_matplotlib(
        self,
        u: np.ndarray,
        v: np.ndarray,
        x: Optional[np.ndarray],
        y: Optional[np.ndarray],
        title: str,
        scale: float,
        save_path: Optional[str]
    ) -> None:
        """Create vector field plot using matplotlib."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if x is None or y is None:
            x = np.arange(u.shape[1])
            y = np.arange(u.shape[0])
            x, y = np.meshgrid(x, y)
        
        # Subsample for clarity
        step = max(1, min(u.shape) // 20)
        
        magnitude = np.sqrt(u**2 + v**2)
        im = ax.contourf(x, y, magnitude, levels=20, cmap='viridis', alpha=0.6)
        
        ax.quiver(x[::step, ::step], y[::step, ::step],
                 u[::step, ::step], v[::step, ::step],
                 magnitude[::step, ::step], cmap='plasma',
                 scale=scale * 50, scale_units='xy')
        
        plt.colorbar(im, ax=ax, label='Magnitude')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_aspect('equal')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def _plot_vector_field_plotly(
        self,
        u: np.ndarray,
        v: np.ndarray,
        x: Optional[np.ndarray],
        y: Optional[np.ndarray],
        title: str,
        scale: float,
        save_path: Optional[str]
    ) -> None:
        """Create vector field plot using plotly."""
        if x is None:
            x = np.arange(u.shape[1])
        if y is None:
            y = np.arange(u.shape[0])
        
        if x.ndim == 1:
            x, y = np.meshgrid(x, y)
        
        # Subsample for clarity
        step = max(1, min(u.shape) // 20)
        
        magnitude = np.sqrt(u**2 + v**2)
        
        fig = go.Figure()
        
        # Add magnitude as background
        fig.add_trace(go.Heatmap(
            z=magnitude,
            x=x[0],
            y=y[:, 0],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Magnitude")
        ))
        
        # Note: Plotly doesn't have native quiver, so we use cone plot or skip vectors
        # For simplicity in this implementation, we focus on magnitude
        
        fig.update_layout(
            title=title,
            xaxis_title="X",
            yaxis_title="Y",
            width=800,
            height=700
        )
        
        if save_path:
            fig.write_html(save_path)
        fig.show()
    
    def plot_animation_frames(
        self,
        fields: list,
        x: Optional[np.ndarray] = None,
        y: Optional[np.ndarray] = None,
        title: str = "Harmonic Field Evolution",
        cmap: str = "viridis",
        interval: int = 100,
        save_path: Optional[str] = None
    ) -> None:
        """
        Create an animation of field evolution.
        
        Args:
            fields: List of 2D field arrays at different time steps
            x: X-coordinate array (optional)
            y: Y-coordinate array (optional)
            title: Plot title
            cmap: Colormap name
            interval: Time between frames in milliseconds
            save_path: Path to save the animation (optional)
        """
        if self.backend == "matplotlib":
            from matplotlib.animation import FuncAnimation
            
            fig, ax = plt.subplots(figsize=(10, 8))
            
            if x is None or y is None:
                vmin = min(f.min() for f in fields)
                vmax = max(f.max() for f in fields)
                im = ax.imshow(fields[0], cmap=cmap, origin='lower',
                             vmin=vmin, vmax=vmax, aspect='auto')
            else:
                vmin = min(f.min() for f in fields)
                vmax = max(f.max() for f in fields)
                im = ax.pcolormesh(x, y, fields[0], cmap=cmap,
                                  vmin=vmin, vmax=vmax, shading='auto')
            
            plt.colorbar(im, ax=ax, label='Field Value')
            ax.set_title(f"{title} - Frame 0", fontsize=14, fontweight='bold')
            ax.set_xlabel('X', fontsize=12)
            ax.set_ylabel('Y', fontsize=12)
            
            def update(frame):
                if x is None or y is None:
                    im.set_array(fields[frame])
                else:
                    im.set_array(fields[frame].ravel())
                ax.set_title(f"{title} - Frame {frame}", fontsize=14, fontweight='bold')
                return [im]
            
            anim = FuncAnimation(fig, update, frames=len(fields),
                               interval=interval, blit=True)
            
            if save_path:
                anim.save(save_path, writer='pillow', fps=1000//interval)
            plt.show()
        else:
            print("Animation with plotly backend not implemented in this version")
