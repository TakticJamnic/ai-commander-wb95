import json
import random
from pathlib import Path
from collections import deque

class PathGenerator:
    def __init__(self, graph_path: str, unit_type: str):
        with open(graph_path) as f:
            self.graph = json.load(f)[unit_type]
        self.unit_type = unit_type

    def find_path(self, start, goal, noise=0.3):
        """Non optimal path with random noise in decision making"""
        visited = set()
        queue = deque()
        queue.append((start, [start]))

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path

            neighbors = list(self.graph.get(current, {}).items())
            if not neighbors:
                continue

            random.shuffle(neighbors)
            if random.random() < noise:
                neighbors = neighbors[:max(1, len(neighbors) // 2)]

            for neighbor, _ in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def generate_paths(self, pairs, output_py_file):
        collected_paths = []

        for start, end in pairs:
            path = self.find_path(start, end)
            if path:
                collected_paths.append(path)

        with open(output_py_file, "a") as f:
            for path in collected_paths:
                f.write(f"{path}\n")
            return collected_paths

    def format_hex_id(self, col, row):
        return f"{col:02}{row:02}"

    def generate_hex_ids(self, width=10, height=10):
        return [self.format_hex_id(col, row) for col in range(1, width + 1) for row in range(1, height + 1)]

    def generate_unique_pairs(self, count=10_000):
        pairs = set()
        elements = ["01","02","03","04","05","06","07","08","09","10"]
        while len(pairs) < count:
            start = random.choice(elements) + random.choice(elements)
            end = random.choice(elements) + random.choice(elements)
            if start != end:
                pairs.add((start, end))
        return list(pairs)

