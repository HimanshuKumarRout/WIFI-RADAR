import os
import sys
import tkinter as tk
import math

# If running this module directly, add the project root to sys.path so the Radar package can be imported.
if __package__ is None and __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from Radar.scanner import WiFiScanner

WIDTH, HEIGHT = 800, 600
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
RADAR_RADIUS = 280
FPS = 60

class RadarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Radar Tracker")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg='black')
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black', highlightthickness=0)
        self.canvas.pack()
        
        self.scanner = WiFiScanner()
        self.scanner.start_scanning(interval=3)
        
        self.sweep_angle = 0.0
        self.sweep_speed = 1.5
        
        self.visible_points = {}
        
        # Start update loop
        self.update_radar()
        
    def polar_to_cartesian(self, radius, angle_deg):
        angle_rad = math.radians(angle_deg)
        # Angle 0 is North, 90 is East
        x = radius * math.sin(angle_rad)
        y = -radius * math.cos(angle_rad)
        return int(CENTER_X + x), int(CENTER_Y + y)
        
    def get_color(self, r, g, b, alpha_pct):
        # alpha_pct is 0.0 to 1.0. We just scale RGB down for fake alpha on a black bg
        r2 = int(r * alpha_pct)
        g2 = int(g * alpha_pct)
        b2 = int(b * alpha_pct)
        return f"#{r2:02x}{g2:02x}{b2:02x}"
        
    def update_radar(self):
        self.canvas.delete("all")
        
        # Draw background
        for r in range(50, RADAR_RADIUS + 1, 50):
            self.canvas.create_oval(CENTER_X - r, CENTER_Y - r, CENTER_X + r, CENTER_Y + r, outline='#002800', width=1)
        self.canvas.create_line(CENTER_X, CENTER_Y - RADAR_RADIUS, CENTER_X, CENTER_Y + RADAR_RADIUS, fill='#002800', width=1)
        self.canvas.create_line(CENTER_X - RADAR_RADIUS, CENTER_Y, CENTER_X + RADAR_RADIUS, CENTER_Y, fill='#002800', width=1)
        
        # Title text
        self.canvas.create_text(20, 20, anchor=tk.NW, text="WIFI RADAR TRACKER", fill='#00FF00', font=('Courier', 16, 'bold'))
        
        # Update sweep angle
        self.sweep_angle = (self.sweep_angle + self.sweep_speed) % 360
        prev_angle = (self.sweep_angle - self.sweep_speed) % 360
        
        current_networks = self.scanner.get_networks()
        self.canvas.create_text(20, 50, anchor=tk.NW, text=f"NETWORKS IN RANGE: {len(current_networks)}", fill='#00FF00', font=('Courier', 12))
        
        for net in current_networks:
            na = net["angle"]
            passed = False
            if self.sweep_speed > 0:
                if prev_angle <= self.sweep_angle:
                    passed = prev_angle <= na <= self.sweep_angle
                else:
                    passed = na >= prev_angle or na <= self.sweep_angle
                    
            if passed:
                pos = self.polar_to_cartesian(net["distance"], na)
                self.visible_points[net["bssid"]] = {
                    "network": net,
                    "alpha": 100, # Max alpha 100 frames to fade
                    "pos": pos
                }
                
        # Draw sweep line trail
        trail_length = 60
        for i in range(1, trail_length):
            a = (self.sweep_angle - i) % 360
            end_pos = self.polar_to_cartesian(RADAR_RADIUS, a)
            
            fade_pct = (1 - i/trail_length) * 0.4
            color = self.get_color(0, 255, 0, fade_pct)
            w = max(1, 3 - int(i/20))
            self.canvas.create_line(CENTER_X, CENTER_Y, end_pos[0], end_pos[1], fill=color, width=w)
            
        # Draw main sweep line
        end_pos = self.polar_to_cartesian(RADAR_RADIUS, self.sweep_angle)
        self.canvas.create_line(CENTER_X, CENTER_Y, end_pos[0], end_pos[1], fill='#64FF64', width=2)
        
        # Draw points
        to_remove = []
        for bssid, data in self.visible_points.items():
            alpha = data["alpha"]
            pos = data["pos"]
            net = data["network"]
            
            if alpha > 0:
                alpha_pct = alpha / 100.0
                pulse = 3 + math.sin(alpha / 5.0) * 3
                
                color = self.get_color(0, 255, 0, alpha_pct)
                bright_color = self.get_color(100, 255, 100, alpha_pct)
                
                # glowing dot
                self.canvas.create_oval(pos[0] - pulse - 2, pos[1] - pulse - 2, pos[0] + pulse + 2, pos[1] + pulse + 2, outline=color, width=2)
                self.canvas.create_oval(pos[0] - 2, pos[1] - 2, pos[0] + 2, pos[1] + 2, fill=bright_color, outline=bright_color)
                
                # text
                if alpha > 20: # don't draw text when almost faded
                    ssid_text = net['ssid'] if net['ssid'] else "<Hidden>"
                    self.canvas.create_text(pos[0] + 12, pos[1] - 10, anchor=tk.NW, text=f"{ssid_text} ({net['signal']}%)", fill=bright_color, font=('Courier', 10))
                    
            data["alpha"] -= 1.0
            if data["alpha"] <= 0:
                to_remove.append(bssid)
                
        for b in to_remove:
            del self.visible_points[b]
            
        # Schedule next frame
        self.root.after(1000 // FPS, self.update_radar)
        
    def on_closing(self):
        self.scanner.stop_scanning()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RadarApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
