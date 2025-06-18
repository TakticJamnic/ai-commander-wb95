import json
import os

# Directions for hex neighbors in flat-top layout
HEX_DIRECTIONS = [
    (+1, 0), (+1, -1), (0, -1),
    (-1, 0), (-1, +1), (0, +1)
]

def parse_hex_id(hex_id):
    col = int(hex_id[:2])
    row = int(hex_id[2:])
    return col, row

def to_hex_id(col, row):
    return f"{col:02d}{row:02d}"

def get_adjacent_hexes_flat_top(col, row, width, height):
    # Flat-top hex layout: even-q offset
    if col % 2 == 1:  # even column
        directions = [
            (+1, 0), (+1, -1), (0, -1),
            (-1, -1), (-1, 0), (0, +1)
        ]
    else:  # odd column
        directions = [
            (+1, +1), (+1, 0), (0, -1),
            (-1, 0), (-1, +1), (0, +1)
        ]

    neighbors = []
    for dc, dr in directions:
        nc, nr = col + dc, row + dr
        if 1 <= nc <= width and 1 <= nr <= height:
            neighbors.append((nc, nr))
    return neighbors

def build_movement_cost_graph(map_data):
    terrain_defs = map_data["terrain"]
    hex_terrain = map_data["hexes"]
    width = map_data["metadata"]["width"]
    height = map_data["metadata"]["height"]

    unit_types = set()
    for terrain in terrain_defs.values():
        unit_types.update(terrain.get("move_cost", {}).keys())

    graph = {unit: {} for unit in unit_types}

    for hex_id, terrain in hex_terrain.items():
        col, row = parse_hex_id(hex_id)
        for n_col, n_row in get_adjacent_hexes_flat_top(col, row, width, height):
            neighbor_id = to_hex_id(n_col, n_row)
            if neighbor_id not in hex_terrain:
                continue

            neighbor_terrain = hex_terrain[neighbor_id]

            for unit in unit_types:
                cost_from = terrain_defs[terrain].get("move_cost", {}).get(unit)
                cost_to = terrain_defs[neighbor_terrain].get("move_cost", {}).get(unit)
                if cost_to is None:
                    continue  # can't enter neighbor
                if cost_from is None:
                    continue  # can't exit this hex

                if hex_id not in graph[unit]:
                    graph[unit][hex_id] = {}
                graph[unit][hex_id][neighbor_id] = cost_to

    return graph

def main():
    with open("generated/generated-map.json") as f:
        map_data = json.load(f)

    movement_graph = build_movement_cost_graph(map_data)

    os.makedirs("generated", exist_ok=True)
    with open("generated/movement-cost-graph.json", "w") as f:
        json.dump(movement_graph, f, indent=2)

if __name__ == "__main__":
    main()