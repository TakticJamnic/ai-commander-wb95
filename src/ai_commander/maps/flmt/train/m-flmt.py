import torch
import heapq
import json

class ManeuverabilityTensor:
    def __init__(self, movement_cost_graph, unit_type):
        self.graph = movement_cost_graph
        self.unit_type = unit_type
        # Lista wszystkich heksów w grafie
        self.hexes = sorted(self.graph[unit_type].keys())
        self.idx_map = {h: i for i, h in enumerate(self.hexes)}
        self.n = len(self.hexes)
        # Tworzymy adjacency matrix (cost matrix), inf tam gdzie brak krawędzi
        inf = float('inf')
        adj = torch.full((self.n, self.n), inf)
        for h_from, neighbors in self.graph[unit_type].items():
            i = self.idx_map[h_from]
            for h_to, cost in neighbors.items():
                j = self.idx_map[h_to]
                adj[i, j] = cost
        self.adj = adj

    def a_star(self, start, goal):
        start_i = self.idx_map[start]
        goal_i = self.idx_map[goal]

        open_set = []
        heapq.heappush(open_set, (0, start_i))
        came_from = {}
        g_score = torch.full((self.n,), float('inf'))
        g_score[start_i] = 0

        def heuristic(a, b):
            return 0  # brak pozycji, heurystyka zerowa

        while open_set:
            current_f, current = heapq.heappop(open_set)
            if current == goal_i:
                path = [current]
                costs = []
                while current in came_from:
                    prev = came_from[current]
                    costs.append((g_score[current] - g_score[prev]).item())
                    current = prev
                    path.append(current)
                path.reverse()
                costs.reverse()
                path_hex = [self.hexes[i] for i in path]
                return path_hex, costs

            neighbors = torch.where(self.adj[current] != float('inf'))[0].tolist()
            for neighbor in neighbors:
                move_cost = self.adj[current, neighbor].item()
                tentative_g_score = g_score[current] + move_cost
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal_i)
                    heapq.heappush(open_set, (f_score.item(), neighbor))

        return None, None

    def get_path(self, start, goal):
        return self.a_star(start, goal)

if __name__ == "__main__":
    with open("generated/movement-cost-graph.json") as f:
        movement_cost_graph_json = json.loads(f.read());
        print(ManeuverabilityTensor(movement_cost_graph_json, "ATV").get_path("0105", "0607"))