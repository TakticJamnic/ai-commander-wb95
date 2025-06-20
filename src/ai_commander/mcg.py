import json
import os

class MovementCostGraphBuilder:
    def __init__(self, map_data):
        self.map_data = map_data
        self.terrain_defs = map_data["terrain"]
        self.hex_terrain = map_data["hexes"]
        self.width = map_data["metadata"]["width"]
        self.height = map_data["metadata"]["height"]
        self.roads = map_data.get("roads", {})
        self.rivers = map_data.get("rivers", {})

    @staticmethod
    def parse_hex_id(hex_id):
        col = int(hex_id[:2])
        row = int(hex_id[2:])
        return col, row

    @staticmethod
    def to_hex_id(col, row):
        return f"{col:02d}{row:02d}"

    def get_adjacent_hexes(self, col, row):
        if col % 2 == 1:
            directions = [(+1, 0), (+1, -1), (0, -1), (-1, -1), (-1, 0), (0, +1)]
        else:
            directions = [(+1, +1), (+1, 0), (0, -1), (-1, 0), (-1, +1), (0, +1)]

        neighbors = []
        for dc, dr in directions:
            nc, nr = col + dc, row + dr
            if 1 <= nc <= self.width and 1 <= nr <= self.height:
                neighbors.append((nc, nr))
        return neighbors

    def build_graph(self):
        unit_types = {
            unit for terrain in self.terrain_defs.values()
            for unit in terrain.get("move_cost", {}).keys()
        }

        # Buduj mapę kosztów dróg
        road_costs = {unit: {} for unit in unit_types}
        for road in self.roads.values():
            road_type = road["type"]
            hexes = road["hexes"]
            for i in range(len(hexes) - 1):
                h1, h2 = hexes[i], hexes[i + 1]
                for unit in unit_types:
                    road_move_cost = self.terrain_defs.get(road_type, {}).get("move_cost", {}).get(unit)
                    if road_move_cost is None:
                        continue
                    road_costs[unit].setdefault(h1, {})[h2] = road_move_cost
                    road_costs[unit].setdefault(h2, {})[h1] = road_move_cost

        # Krawędzie rzek
        river_edges = {
            (h1, h2)
            for river in self.rivers.values()
            for segment in river.get("segments", [])
            for h1, h2 in [segment.split("-"), segment.split("-")[::-1]]
        }

        graph = {unit: {} for unit in unit_types}

        for hex_id, terrain in self.hex_terrain.items():
            col, row = self.parse_hex_id(hex_id)
            for n_col, n_row in self.get_adjacent_hexes(col, row):
                neighbor_id = self.to_hex_id(n_col, n_row)
                if neighbor_id not in self.hex_terrain:
                    continue

                river_block = (hex_id, neighbor_id) in river_edges

                for unit in unit_types:
                    has_road = hex_id in road_costs[unit] and neighbor_id in road_costs[unit][hex_id]
                    if river_block and not has_road:
                        continue

                    if has_road:
                        cost = road_costs[unit][hex_id][neighbor_id]
                    else:
                        cost_from = self.terrain_defs[terrain].get("move_cost", {}).get(unit)
                        cost_to = self.terrain_defs[self.hex_terrain[neighbor_id]].get("move_cost", {}).get(unit)
                        if cost_to is None or cost_from is None:
                            continue
                        cost = cost_to

                    graph[unit].setdefault(hex_id, {})[neighbor_id] = cost
        return graph

    def save_graph(self, output_base):
        graph = self.build_graph()
        output_file = os.path.join(output_base, "mcg.json")
        with open(output_file, "w") as f:
            json.dump(graph, f, indent=2)
            print(f"✅ MCG graph saved to ➡️ {output_file}")
            return graph    
        

    @classmethod
    def from_file(cls, map_file):
        with open(map_file) as f:
            map_data = json.load(f)
        return cls(map_data)

