import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

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
    "ROAD": {"color": "white", "linewidth": 2, "linestyle": "-", "stroke_width": 3}
}

RIVER_STYLE = {"color": "blue", "linewidth": 2.5, "linestyle": "-"}

HEX_SIZE = 1.0  # Radius of hex
HEX_WIDTH = 2 * HEX_SIZE
HEX_HEIGHT = math.sqrt(3) * HEX_SIZE  # wysokość heksa flat-top

# === HELPER FUNCTIONS ===

# def hex_to_pixel_flat(col, row):
#     x = HEX_WIDTH * (col - 1) + (HEX_WIDTH / 2 if row % 2 == 0 else 0)
#     y = HEX_HEIGHT * (row - 1)
#     return (x, y)

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

    # Oblicz pozycję punktu po środku wspólnej krawędzi
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    # Wygeneruj małą linię prostopadłą do łączącej dwa środki
    perp_angle = angle + math.pi / 2
    dx_edge = (HEX_SIZE * 0.4) * math.cos(perp_angle)
    dy_edge = (HEX_SIZE * 0.4) * math.sin(perp_angle)

    return (mx - dx_edge, my - dy_edge), (mx + dx_edge, my + dy_edge)

def draw_river_between(ax, h1, h2, style, map_height):
    (x1, y1), (x2, y2) = get_edge_coords(h1, h2, map_height)
    ax.plot([x1, x2], [y1, y2], **style)

# === MAIN VISUALIZATION ===

def visualise_map(json_path):
    with open(json_path) as f:
        data = json.load(f)

    map_height = data["metadata"]["height"]
    terrain_map = data["hexes"]
    terrain_defs = data.get("terrain", {})
    roads = data.get("roads", {})
    rivers = data.get("rivers", {})

    fig, ax = plt.subplots(figsize=(14, 12))
    ax.set_aspect('equal')
    ax.axis('off')

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

    # Draw rivers between hexes (as edge barriers)
    for river in rivers.values():
        for segment in river.get("segments", []):
            h1, h2 = segment.split("-")
            draw_river_between(ax, h1, h2, RIVER_STYLE, map_height)

    plt.tight_layout()
    plt.show()

# === ENTRY POINT ===

if __name__ == "__main__":
    json_file = "generated/generated-map.json"  # Change if needed
    visualise_map(json_file)
