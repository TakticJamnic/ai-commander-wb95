import json
import random
from pathlib import Path

# Config
MAP_WIDTH = 10
MAP_HEIGHT = 10
OUTPUT_FILE = "generated/generated-map.json"

TERRAIN_TYPES = {
    "FOREST": {
        "move_cost": { "INF": 1, "ATV": 2 },
        "defence_bonus": 2
    },
    "CLEAR": {
        "move_cost": { "INF": 1, "ATV": 1 }
    }
}

ROAD_TYPES = {
    "ROAD": {
      "move_cost": { "INF": 0.5, "ATV": 0.33 }
    }
}

OBSTACLE_TYPES = {
    "STREAM": {
      "move_cost": { "INF": 2, "ATV": 4 },
      "defence_bonus": 1
    }
}

def format_hex_id(col, row):
    return f"{col:02}{row:02}"

def get_neighbors(col, row):
    # Flat-topped hex adjacency (even-q layout)
    offsets = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)] if col % 2 == 0 else \
              [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
    neighbors = []
    for dc, dr in offsets:
        nc, nr = col + dc, row + dr
        if 1 <= nc <= MAP_WIDTH and 1 <= nr <= MAP_HEIGHT:
            neighbors.append((nc, nr))
    return neighbors

def generate_roads(hex_ids):
    road_id = 0
    roads = {}

    def create_linear_road(start_col, start_row, direction, length, road_type_name):
        nonlocal road_id
        hex_list = []
        col, row = start_col, start_row
        for _ in range(length):
            if 1 <= col <= MAP_WIDTH and 1 <= row <= MAP_HEIGHT:
                hex_list.append(format_hex_id(col, row))
                col += direction[0]
                row += direction[1]
        if len(hex_list) >= 3:
            road_id += 1
            roads[f"road-{road_id}"] = {
                "name": f"{road_type_name.title()} {road_id}",
                "type": road_type_name,
                "hexes": hex_list
            }

    # Main horizontal roads
    for i in range(2):
        row = random.randint(2, MAP_HEIGHT - 2)
        road_type_name = random.choice(list(ROAD_TYPES.keys()))
        create_linear_road(1, row, (1, 0), MAP_WIDTH, road_type_name)

    # Main vertical roads
    for i in range(2):
        col = random.randint(2, MAP_WIDTH - 2)
        road_type_name = random.choice(list(ROAD_TYPES.keys()))
        create_linear_road(col, 1, (0, 1), MAP_HEIGHT, road_type_name)

    # Connectors
    for _ in range(20):  # 20 short connector roads
        h1 = random.choice(hex_ids)
        col, row = int(h1[:2]), int(h1[2:])
        neighbors = get_neighbors(col, row)
        if not neighbors:
            continue
        h2_col, h2_row = random.choice(neighbors)
        h2 = format_hex_id(h2_col, h2_row)
        if h1 != h2 and h1 < h2:
            road_type_name = random.choice(list(ROAD_TYPES.keys()))
            road_id += 1
            roads[f"road-{road_id}"] = {
                "name": f"Connector {road_id}",
                "type": road_type_name,
                "hexes": [h1, h2]
            }

    return roads

def generate():
    hexes = {}
    rivers = {}

    # Random terrain assignment
    hex_ids = []
    for col in range(1, MAP_WIDTH + 1):
        for row in range(1, MAP_HEIGHT + 1):
            hex_id = format_hex_id(col, row)
            hex_ids.append(hex_id)
            hexes[hex_id] = random.choice(list(TERRAIN_TYPES.keys()))

    roads = generate_roads(hex_ids)
    # River/stream segments
    river_id = 0
    for _ in range(int(MAP_WIDTH * MAP_HEIGHT * 0.05)):  # 5% river coverage
        h1 = random.choice(hex_ids)
        col, row = int(h1[:2]), int(h1[2:])
        neighbors = get_neighbors(col, row)
        if not neighbors:
            continue
        n_col, n_row = random.choice(neighbors)
        h2 = format_hex_id(n_col, n_row)
        if h1 < h2:
            river_id += 1
            rivers[f"river-{river_id}"] = {
                "name": f"River {river_id}",
                "type": random.choice(list(OBSTACLE_TYPES.keys())),
                "segments": [f"{h1}-{h2}"]
            }

    # Assemble map
    map_data = {
        "metadata": {
            "authors": ["AutoGen"],
            "name": "Random Map",
            "width": MAP_WIDTH,
            "height": MAP_HEIGHT
        },
        "terrain": TERRAIN_TYPES,
        "hexes": hexes,
        "roads": roads,
        "rivers": rivers
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(map_data, f, indent=2)

    print(f"✅ Map saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()