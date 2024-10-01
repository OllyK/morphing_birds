"""
morphing_birds: Run PCA on morphing bird wings and tail in flight.
"""
from __future__ import annotations

from .SkeletonDefinition import SkeletonDefinition
from .hawk_skeleton_definition import HawkSkeletonDefinition
# from .spider_skeleton_definition import SpiderSkeletonDefinition
from .Animal3D import Animal3D
from .Hawk3D import Hawk3D
# from .Spider3D import Spider3D
from .AnimalPlotter import plot, interactive_plot, plot_multiple
from .AnimalAnimate import animate, animate_compare
from .HawkDash import create_dash_app, plot_plotly

__all__ = ("__version__", "Animal3D", "Hawk3D", "SkeletonDefinition",
    "HawkSkeletonDefinition", "plot", "interactive_plot", "plot_multiple", "animate", "animate_compare", "create_dash_app", "plot_plotly")
__version__ = "0.1.0"
