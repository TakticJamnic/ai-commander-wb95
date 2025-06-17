import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# Terrain color mapping
TERRAIN_COLORS = {
    "CLEAR": "#a4d3a2",
    "FOREST": "#228b22",
    "SWAMP": "#556b2f",
    "URBAN": "#c0c0c0",
    "HILL": "#bdb76b",
    "WATER": "#1e90ff",
}

def axial_to_pixel(col, row, size):
    """Flat-topped hex: oblicz pozycję XY"""
    width = math.sqrt(3) * size
    height = 2 * size
    x = width * (col + 0.5 * (row % 2))
    y = height * 3/4 * row
    return x, -y

def draw_hex(ax, x, y, size, color, label=None):
    """Narysuj pojedynczy heks"""
    hexagon = patches.RegularPolygon(
        (x, y),
        numVertices=6,
        radius=size,
        orientation=0,  # flat top
        facecolor=color,
        edgecolor="black",
        linewidth=0.5
    )
    ax.add_patch(hexagon)
    if label:
        ax.text(x, y, label, ha="center", va="center", fontsize=6, color="black")

def visualize_map(json_path, size=1.0):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    width = data["width"]
    height = data["height"]
    hexes = data["hexes"]

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_aspect("equal")
    ax.axis("off")

    all_x = []
    all_y = []

    for hex_id, hex_data in hexes.items():
        col = int(hex_id[:2])
        row = int(hex_id[2:])
        terrain = hex_data["terrain"]
        color = TERRAIN_COLORS.get(terrain, "#ffffff")

        x, y = axial_to_pixel(col, row, size)
        all_x.append(x)
        all_y.append(y)
        draw_hex(ax, x, y, size, color, label=hex_id)

    margin = size * 2
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize_map("maps/random_map_10x10.json", size=1.0)