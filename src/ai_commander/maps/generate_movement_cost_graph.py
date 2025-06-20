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
    roads = map_data.get("roads", {})
    rivers = map_data.get("rivers", {})

    unit_types = set()
    for terrain in terrain_defs.values():
        unit_types.update(terrain.get("move_cost", {}).keys())

    # Budujemy mapę kosztów ruchu po drogach (dwukierunkowe)
    road_costs = {unit: {} for unit in unit_types}
    for road in roads.values():
        road_type = road["type"]
        hexes = road["hexes"]
        for i in range(len(hexes) - 1):
            h1, h2 = hexes[i], hexes[i + 1]
            for unit in unit_types:
                road_move_cost = terrain_defs.get(road_type, {}).get("move_cost", {}).get(unit)
                if road_move_cost is None:
                    continue
                if h1 not in road_costs[unit]:
                    road_costs[unit][h1] = {}
                if h2 not in road_costs[unit]:
                    road_costs[unit][h2] = {}
                road_costs[unit][h1][h2] = road_move_cost
                road_costs[unit][h2][h1] = road_move_cost  # dwukierunkowe

    # Budujemy zbiór krawędzi rzek — pary heksów które łączą rzeki (niezależnie od kierunku)
    river_edges = set()
    for river in rivers.values():
        for segment in river.get("segments", []):
            h1, h2 = segment.split("-")
            river_edges.add((h1, h2))
            river_edges.add((h2, h1))

    graph = {unit: {} for unit in unit_types}

    for hex_id, terrain in hex_terrain.items():
        col, row = parse_hex_id(hex_id)
        for n_col, n_row in get_adjacent_hexes_flat_top(col, row, width, height):
            neighbor_id = to_hex_id(n_col, n_row)
            if neighbor_id not in hex_terrain:
                continue

            # Sprawdzamy, czy jest rzeka między tymi heksami
            river_block = ((hex_id, neighbor_id) in river_edges)

            for unit in unit_types:
                # Jeśli jest rzeka i nie ma drogi na tym odcinku, ruch niemożliwy
                has_road = (hex_id in road_costs[unit] and neighbor_id in road_costs[unit][hex_id])
                if river_block and not has_road:
                    continue

                if has_road:
                    cost = road_costs[unit][hex_id][neighbor_id]
                else:
                    cost_from = terrain_defs[terrain].get("move_cost", {}).get(unit)
                    cost_to = terrain_defs[hex_terrain[neighbor_id]].get("move_cost", {}).get(unit)
                    if cost_to is None or cost_from is None:
                        continue
                    cost = cost_to  # koszt wejścia na sąsiada

                if hex_id not in graph[unit]:
                    graph[unit][hex_id] = {}
                graph[unit][hex_id][neighbor_id] = cost

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