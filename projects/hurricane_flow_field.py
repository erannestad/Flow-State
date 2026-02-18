#!/usr/bin/env python3
"""
Hurricane Flow Field Generator
Creates a fluid dynamic flow field visualization of hurricane motion
and outputs it as an SVG with arrows showing flow direction.
"""

import math
import numpy as np
from typing import Tuple


class HurricaneFlowField:
    """Generates a hurricane-like flow field using fluid dynamics principles."""
    
    def __init__(self, width: int = 800, height: int = 600, 
                 center_x: float = None, center_y: float = None,
                 max_wind_speed: float = 50.0, eye_radius: float = 30.0):
        """
        Initialize the flow field.
        
        Args:
            width: SVG canvas width
            height: SVG canvas height
            center_x: X coordinate of hurricane eye (default: center)
            center_y: Y coordinate of hurricane eye (default: center)
            max_wind_speed: Maximum wind speed at outer edge
            eye_radius: Radius of the calm eye region
        """
        self.width = width
        self.height = height
        self.center_x = center_x if center_x is not None else width / 2
        self.center_y = center_y if center_y is not None else height / 2
        self.max_wind_speed = max_wind_speed
        self.eye_radius = eye_radius
        
    def velocity_field(self, x: float, y: float) -> Tuple[float, float]:
        """
        Calculate velocity vector at point (x, y) using Rankine vortex model.
        
        The Rankine vortex combines:
        - Solid body rotation inside the eye
        - Potential flow (inverse radius) outside the eye
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Tuple of (vx, vy) velocity components
        """
        # Distance from center
        dx = x - self.center_x
        dy = y - self.center_y
        r = math.sqrt(dx*dx + dy*dy)
        
        # Avoid division by zero at center
        if r < 0.1:
            return (0.0, 0.0)
        
        # Calculate angular velocity
        if r < self.eye_radius:
            # Inside eye: solid body rotation
            omega = self.max_wind_speed / self.eye_radius
        else:
            # Outside eye: potential flow (conservation of angular momentum)
            omega = (self.max_wind_speed * self.eye_radius) / (r * r)
        
        # Convert to Cartesian velocity components
        # Tangential velocity (perpendicular to radius)
        vx = -omega * dy / r
        vy = omega * dx / r
        
        # Add slight inward radial component for spiral effect
        radial_factor = 0.1 * (1.0 - self.eye_radius / max(r, self.eye_radius))
        vx += radial_factor * (-dx / r) * self.max_wind_speed * 0.1
        vy += radial_factor * (-dy / r) * self.max_wind_speed * 0.1
        
        return (vx, vy)
    
    def generate_grid(self, spacing: int = 30) -> list:
        """
        Generate a grid of points for flow visualization.
        
        Args:
            spacing: Distance between grid points
            
        Returns:
            List of (x, y) tuples
        """
        points = []
        for x in range(spacing, self.width, spacing):
            for y in range(spacing, self.height, spacing):
                points.append((x, y))
        return points
    
    def arrow_path(self, x: float, y: float, vx: float, vy: float, 
                   scale: float = 1.0, arrow_length: float = 20.0) -> str:
        """
        Generate SVG path for an arrow showing flow direction.
        
        Args:
            x: Starting X coordinate
            y: Starting Y coordinate
            vx: X component of velocity
            vy: Y component of velocity
            scale: Scale factor for arrow size
            arrow_length: Base length of arrow
            
        Returns:
            SVG path string
        """
        # Normalize velocity vector
        speed = math.sqrt(vx*vx + vy*vy)
        if speed < 0.01:
            return ""  # Skip very slow flows
        
        # Scale arrow length by speed
        length = arrow_length * scale * min(speed / self.max_wind_speed, 1.0)
        
        # Normalize direction
        vx_norm = vx / speed
        vy_norm = vy / speed
        
        # Arrow tip
        tip_x = x + vx_norm * length
        tip_y = y + vy_norm * length
        
        # Arrow head dimensions
        head_length = length * 0.3
        head_width = length * 0.15
        
        # Perpendicular vector for arrow head
        perp_x = -vy_norm
        perp_y = vx_norm
        
        # Arrow head points
        head_base_x = tip_x - vx_norm * head_length
        head_base_y = tip_y - vy_norm * head_length
        
        left_x = head_base_x + perp_x * head_width
        left_y = head_base_y + perp_y * head_width
        
        right_x = head_base_x - perp_x * head_width
        right_y = head_base_y - perp_y * head_width
        
        # Create path
        path = f"M {x:.2f},{y:.2f} L {tip_x:.2f},{tip_y:.2f} "
        path += f"M {left_x:.2f},{left_y:.2f} L {tip_x:.2f},{tip_y:.2f} "
        path += f"L {right_x:.2f},{right_y:.2f}"
        
        return path
    
    def generate_svg(self, spacing: int = 30, arrow_scale: float = 1.0,
                     stroke_width: float = 1.5, stroke_color: str = "#0066cc") -> str:
        """
        Generate complete SVG representation of the flow field.
        
        Args:
            spacing: Grid spacing for arrows
            arrow_scale: Scale factor for arrow sizes
            stroke_width: Width of arrow strokes
            stroke_color: Color of arrows
            
        Returns:
            Complete SVG string
        """
        # SVG header
        svg = f'''<svg width="{self.width}" height="{self.height}" 
xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .flow-arrow {{
        stroke: {stroke_color};
        stroke-width: {stroke_width};
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
      }}
      .eye {{
        fill: rgba(200, 200, 200, 0.3);
        stroke: rgba(100, 100, 100, 0.5);
        stroke-width: 2;
      }}
    </style>
  </defs>
  
  <!-- Background -->
  <rect width="{self.width}" height="{self.height}" fill="#f8f9fa"/>
  
  <!-- Hurricane eye -->
  <circle cx="{self.center_x:.2f}" cy="{self.center_y:.2f}" 
          r="{self.eye_radius:.2f}" class="eye"/>
  
  <!-- Flow field arrows -->
  <g class="flow-field">
'''
        
        # Generate arrows for each grid point
        grid_points = self.generate_grid(spacing)
        for x, y in grid_points:
            vx, vy = self.velocity_field(x, y)
            arrow_path = self.arrow_path(x, y, vx, vy, arrow_scale)
            if arrow_path:
                svg += f'    <path d="{arrow_path}" class="flow-arrow"/>\n'
        
        # Close SVG
        svg += '''  </g>
</svg>'''
        
        return svg
    
    def save_svg(self, filename: str = "hurricane_flow_field.svg", **kwargs):
        """
        Generate and save SVG to file.
        
        Args:
            filename: Output filename
            **kwargs: Additional arguments passed to generate_svg()
        """
        svg_content = self.generate_svg(**kwargs)
        with open(filename, 'w') as f:
            f.write(svg_content)
        print(f"Flow field saved to {filename}")


def main():
    """Main function to generate hurricane flow field visualization."""
    
    # Create flow field with custom parameters
    flow_field = HurricaneFlowField(
        width=800,
        height=600,
        center_x=400,  # Center of canvas
        center_y=300,
        max_wind_speed=60.0,  # Maximum wind speed
        eye_radius=40.0  # Radius of calm eye
    )
    
    # Generate and save SVG
    flow_field.save_svg(
        filename="hurricane_flow_field.svg",
        spacing=25,  # Grid spacing (smaller = more arrows)
        arrow_scale=1.2,  # Arrow size multiplier
        stroke_width=1.5,
        stroke_color="#0066cc"  # Blue color for flow arrows
    )
    
    print("\nHurricane flow field visualization complete!")
    print("Parameters:")
    print(f"  Canvas size: {flow_field.width}x{flow_field.height}")
    print(f"  Eye center: ({flow_field.center_x}, {flow_field.center_y})")
    print(f"  Eye radius: {flow_field.eye_radius}")
    print(f"  Max wind speed: {flow_field.max_wind_speed}")


if __name__ == "__main__":
    main()
