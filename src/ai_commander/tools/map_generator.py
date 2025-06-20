import json
import os
import random
from pathlib import Path
from ai_commander.tools.name_generator import generate_readable_name

class RandomMapGenerator:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.terrain_types = {
            "FOREST": {
                "move_cost": {"INF": 1, "ATV": 2},
                "defence_bonus": 2
            },
            "CLEAR": {
                "move_cost": {"INF": 1, "ATV": 1}
            }
        }
        self.road_types = {
            "ROAD": {
                "move_cost": {"INF": 0.5, "ATV": 0.1}
            }
        }
        self.obstacle_types = {
            "STREAM": {
                "move_cost": {"INF": 2, "ATV": 4},
                "defence_bonus": 1
            }
        }

    def format_hex_id(self, col, row):
        return f"{col:02}{row:02}"

    def get_neighbors(self, col, row):
        if col % 2 == 0:
            offsets = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
        else:
            offsets = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]

        neighbors = []
        for dc, dr in offsets:
            nc, nr = col + dc, row + dr
            if 1 <= nc <= self.width and 1 <= nr <= self.height:
                neighbors.append((nc, nr))
        return neighbors

    def generate_roads(self, hex_ids):
        road_id = 0
        roads = {}

        def create_linear_road(start_col, start_row, direction, length, road_type_name):
            nonlocal road_id
            hex_list = []
            col, row = start_col, start_row
            for _ in range(length):
                if 1 <= col <= self.width and 1 <= row <= self.height:
                    hex_list.append(self.format_hex_id(col, row))
                    col += direction[0]
                    row += direction[1]
            if len(hex_list) >= 3:
                road_id += 1
                roads[f"road-{road_id}"] = {
                    "name": f"{road_type_name.title()} {road_id}",
                    "type": road_type_name,
                    "hexes": hex_list
                }

        for _ in range(2):
            row = random.randint(2, self.height - 2)
            road_type = random.choice(list(self.road_types.keys()))
            create_linear_road(1, row, (1, 0), self.width, road_type)

        for _ in range(2):
            col = random.randint(2, self.width - 2)
            road_type = random.choice(list(self.road_types.keys()))
            create_linear_road(col, 1, (0, 1), self.height, road_type)

        for _ in range(20):
            h1 = random.choice(hex_ids)
            col, row = int(h1[:2]), int(h1[2:])
            neighbors = self.get_neighbors(col, row)
            if not neighbors:
                continue
            n_col, n_row = random.choice(neighbors)
            h2 = self.format_hex_id(n_col, n_row)
            if h1 != h2 and h1 < h2:
                road_type = random.choice(list(self.road_types.keys()))
                road_id += 1
                roads[f"road-{road_id}"] = {
                    "name": f"Connector {road_id}",
                    "type": road_type,
                    "hexes": [h1, h2]
                }

        return roads

    def generate(self, output_base="tests/generated"):
        run_id = generate_readable_name()
        output_dir = os.path.join(output_base, run_id)
        output_file = os.path.join(output_dir, "map.json")

        os.makedirs(output_dir, exist_ok=True)

        hexes = {}
        hex_ids = []

        for col in range(1, self.width + 1):
            for row in range(1, self.height + 1):
                hex_id = self.format_hex_id(col, row)
                hex_ids.append(hex_id)
                hexes[hex_id] = random.choice(list(self.terrain_types.keys()))

        roads = self.generate_roads(hex_ids)

        rivers = {}
        river_id = 0
        for _ in range(int(self.width * self.height * 0.05)):
            h1 = random.choice(hex_ids)
            col, row = int(h1[:2]), int(h1[2:])
            neighbors = self.get_neighbors(col, row)
            if not neighbors:
                continue
            n_col, n_row = random.choice(neighbors)
            h2 = self.format_hex_id(n_col, n_row)
            if h1 < h2:
                river_id += 1
                rivers[f"river-{river_id}"] = {
                    "name": f"River {river_id}",
                    "type": random.choice(list(self.obstacle_types.keys())),
                    "segments": [f"{h1}-{h2}"]
                }

        terrain_defs = {
            **self.terrain_types,
            **self.road_types,
            **self.obstacle_types
        }

        map_data = {
            "metadata": {
                "authors": ["AutoGen"],
                "name": run_id,
                "width": self.width,
                "height": self.height
            },
            "terrain": terrain_defs,
            "hexes": hexes,
            "roads": roads,
            "rivers": rivers
        }

        with open(output_file, "w") as f:
            json.dump(map_data, f, indent=2)

        print(f"✅ Map saved to ➡️ {output_file}")
        return run_id, map_data
