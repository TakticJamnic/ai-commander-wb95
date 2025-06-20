import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
import matplotlib.widgets as widgets
from pathlib import Path
import matplotlib
matplotlib.use('TkAgg')  # lub 'Qt5Agg', zależnie co masz zainstalowane

TOKEN_COLOR = "red"
OUTPUT_PATHS_FILE = Path("generated/paths.jsonl")

# === CONFIGURATION ===
TERRAIN_COLORS = {
    "FOREST": "#228B22",   # green
    "CLEAR": "#FFFFCC",    # light yellow
    "HILL": "#DEB887",     # tan
    "WATER": "#87CEFA",    # light blue
    "URBAN": "#A9A9A9",    # gray
}

ROAD_STYLES = {
    "LOCAL": {"color": "black", "linewidth": 1, "linestyle": ":"},
    "REGIONAL": {"color": "black", "linewidth": 1.5, "linestyle": "-"},
    "HIGHWAY": {"color": "black", "linewidth": 2, "linestyle": "--"},
    "ROAD": {"color": "white", "linewidth": 2, "linestyle": "-"}
}

RIVER_STYLE = {"color": "blue", "linewidth": 2.5, "linestyle": "-"}

HEX_SIZE = 1.0
HEX_WIDTH = 2 * HEX_SIZE
HEX_HEIGHT = math.sqrt(3) * HEX_SIZE

# === HELPER FUNCTIONS ===
def hex_to_pixel_flat(col, row, map_height):
    x = HEX_WIDTH * (col - 1) * 0.75
    y = HEX_HEIGHT * (map_height - row) + (HEX_HEIGHT / 2 if col % 2 == 1 else 0)
    return (x, y)

def hex_to_pixel(col, row):
    x = HEX_WIDTH * (3/4) * (col - 1)
    y = HEX_HEIGHT * (row - 1) + (HEX_HEIGHT / 2 if col % 2 == 0 else 0)
    return (x, y)

def draw_flat_top_hex(ax, x, y, color):
    angles_deg = np.arange(0, 360, 60)
    points = [
        (x + HEX_SIZE * np.cos(np.radians(a)),
         y + HEX_SIZE * np.sin(np.radians(a)))
        for a in angles_deg
    ]
    hex_patch = patches.Polygon(points, closed=True, edgecolor='black', facecolor=color)
    ax.add_patch(hex_patch)

def parse_hex_id(hex_id):
    col = int(hex_id[:2])
    row = int(hex_id[2:])
    return col, row

def get_hex_center(hex_id, map_height):
    col, row = parse_hex_id(hex_id)
    return hex_to_pixel_flat(col, row, map_height)

def draw_line_between(ax, h1, h2, style, map_height):
    x1, y1 = get_hex_center(h1, map_height)
    x2, y2 = get_hex_center(h2, map_height)
    draw_stroked_line(ax, x1, y1, x2, y2, style)
    ax.plot([x1, x2], [y1, y2], **style)

def draw_stroked_line(ax, x1, y1, x2, y2, line_style, stroke_width=3):
    # Stroke line (underneath)
    ax.plot([x1, x2], [y1, y2], 
            color=line_style.get("stroke_color", "black"), 
            linewidth=line_style.get("linewidth", 2) + line_style.get("stroke_width", 1), 
            solid_capstyle='round', 
            zorder=1)

    # Foreground line
    ax.plot([x1, x2], [y1, y2], 
            color=line_style.get("color", "white"),
            linewidth=line_style.get("linewidth", 2),
            linestyle=line_style.get("linestyle", "-"),
            solid_capstyle='round',
            zorder=2)    

def get_edge_coords(h1, h2, map_height):
    x1, y1 = get_hex_center(h1, map_height)
    x2, y2 = get_hex_center(h2, map_height)
    dx = x2 - x1
    dy = y2 - y1
    angle = math.atan2(dy, dx)
    angle_deg = math.degrees(angle)

    edge_offset = HEX_SIZE * 0.5

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    perp_angle = angle + math.pi / 2
    dx_edge = (HEX_SIZE * 0.4) * math.cos(perp_angle)
    dy_edge = (HEX_SIZE * 0.4) * math.sin(perp_angle)

    return (mx - dx_edge, my - dy_edge), (mx + dx_edge, my + dy_edge)

def draw_river_between(ax, h1, h2, style, map_height):
    (x1, y1), (x2, y2) = get_edge_coords(h1, h2, map_height)
    ax.plot([x1, x2], [y1, y2], **style)

# === MAIN VISUALIZATION ===

def visualise_map(json_path):
    from matplotlib.widgets import Button

    with open(json_path) as f:
        data = json.load(f)

    map_height = data["metadata"]["height"]
    terrain_map = data["hexes"]
    roads = data.get("roads", {})
    rivers = data.get("rivers", {})

    fig, ax = plt.subplots(figsize=(14, 12))
    plt.subplots_adjust(bottom=0.15)  # zostaw miejsce na przyciski
    ax.set_aspect('equal')
    ax.axis('off')

    state = InteractionState()

    # Draw hexes
    for hex_id, terrain_type in terrain_map.items():
        col, row = parse_hex_id(hex_id)
        x, y = hex_to_pixel_flat(col, row, map_height)
        color = TERRAIN_COLORS.get(terrain_type, "#DDDDDD")
        draw_flat_top_hex(ax, x, y, color)
        ax.text(x, y, hex_id, ha='center', va='center', fontsize=8)

    # Draw roads
    for road in roads.values():
        hexes = road["hexes"]
        style = ROAD_STYLES.get(road["type"], ROAD_STYLES["ROAD"])
        for i in range(len(hexes) - 1):
            draw_line_between(ax, hexes[i], hexes[i + 1], style, map_height)

    # Draw rivers
    for river in rivers.values():
        for segment in river.get("segments", []):
            h1, h2 = segment.split("-")
            draw_river_between(ax, h1, h2, RIVER_STYLE, map_height)

    # === BUTTONS ===
    btn_ax_start = plt.axes([0.7, 0.01, 0.1, 0.05])
    btn_ax_stop = plt.axes([0.81, 0.01, 0.1, 0.05])
    btn_start = Button(btn_ax_start, "Start")
    btn_stop = Button(btn_ax_stop, "Stop")

    def on_start(event):
        print("▶️ Start recording path")
        state.reset()
        state.tracking = True

    def on_stop(event):
        print("⏹️ Stop recording")
        if state.tracking and len(state.current_path) > 1:
            OUTPUT_PATHS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with OUTPUT_PATHS_FILE.open("a") as f:
                f.write(json.dumps(state.current_path) + "\n")
            print(f"✅ Saved path: {state.current_path}")
        else:
            print("⚠️ No path to save.")
        state.reset()
        fig.canvas.draw()

    btn_start.on_clicked(on_start)
    btn_stop.on_clicked(on_stop)

    def on_click(event):
        if not state.tracking or event.inaxes != ax:
            return

        min_dist = float('inf')
        nearest_hex = None

        for hex_id in terrain_map:
            xh, yh = get_hex_center(hex_id, map_height)
            dist = (event.xdata - xh) ** 2 + (event.ydata - yh) ** 2
            if dist < min_dist:
                min_dist = dist
                nearest_hex = hex_id

        if nearest_hex:
            if len(state.current_path) == 0 or state.current_path[-1] != nearest_hex:
                state.current_path.append(nearest_hex)
                x, y = get_hex_center(nearest_hex, map_height)
                if state.token_plot:
                    state.token_plot.set_data([x], [y])
                else:
                    state.token_plot, = ax.plot(x, y, 'o', color=TOKEN_COLOR, markersize=12)
                fig.canvas.draw()
                print(f"📍 Moved to {nearest_hex}")

    fig.canvas.mpl_connect("button_press_event", on_click)
    plt.show()

def on_click(event, ax, data, map_height, state):
    if not state.tracking or event.inaxes != ax:
        return

    min_dist = float('inf')
    nearest_hex = None

    for hex_id in data["hexes"]:
        xh, yh = get_hex_center(hex_id, map_height)
        dist = (event.xdata - xh) ** 2 + (event.ydata - yh) ** 2
        if dist < min_dist:
            min_dist = dist
            nearest_hex = hex_id

    if nearest_hex:
        if len(state.current_path) == 0 or nearest_hex != state.current_path[-1]:
            state.current_path.append(nearest_hex)
            x, y = get_hex_center(nearest_hex, map_height)
            if state.token_plot:
                state.token_plot.set_data([x], [y])
            else:
                state.token_plot, = ax.plot(x, y, 'o', color=TOKEN_COLOR, markersize=12)
            plt.draw()

def setup_buttons(fig, ax, state):
    ax_start = plt.axes([0.8, 0.025, 0.1, 0.04])
    ax_stop = plt.axes([0.65, 0.025, 0.1, 0.04])
    btn_start = widgets.Button(ax_start, 'Start')
    btn_stop = widgets.Button(ax_stop, 'Stop')

    def on_start(event):
        print("⏺️ Tracking started.")
        state.reset()
        state.tracking = True

    def on_stop(event):
        if state.tracking and len(state.current_path) >= 2:
            with OUTPUT_PATHS_FILE.open("a") as f:
                f.write(json.dumps(state.current_path) + "\n")
            print(f"✅ Path saved: {state.current_path}")
        else:
            print("⚠️ Nothing to save.")
        state.reset()
        plt.draw()

    btn_start.on_clicked(on_start)
    btn_stop.on_clicked(on_stop)

class InteractionState:
    def __init__(self):
        self.current_path = []
        self.tracking = False
        self.token_plot = None

    def reset(self):
        self.current_path = []
        self.tracking = False
        if self.token_plot:
            self.token_plot.remove()
            self.token_plot = None

# === ENTRY POINT ===
if __name__ == "__main__":
    json_file = "generated/generated-map.json"
    visualise_map(json_file)
