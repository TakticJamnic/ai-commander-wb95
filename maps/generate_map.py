import json
import random

TERRAINS = {
    "CLEAR": {"move_cost": 1, "defense_bonus": 0},
    "FOREST": {"move_cost": 2, "defense_bonus": 1},
    "SWAMP": {"move_cost": 3, "defense_bonus": 0},
    "URBAN": {"move_cost": 2, "defense_bonus": 2},
    "HILL": {"move_cost": 2, "defense_bonus": 2},
    "WATER": {"move_cost": 99, "defense_bonus": 0},
}

def generate_map(width=10, height=10, seed=42):
    random.seed(seed)
    map_data = {
        "width": width,
        "height": height,
        "hexes": {}
    }

    for row in range(height):
        for col in range(width):
            hex_id = f"{col:02d}{row:02d}"
            terrain = random.choice(list(TERRAINS.keys()))
            map_data["hexes"][hex_id] = {
                "terrain": terrain,
                "move_cost": TERRAINS[terrain]["move_cost"],
                "defense_bonus": TERRAINS[terrain]["defense_bonus"]
            }

    return map_data

if __name__ == "__main__":
    map_data = generate_map(width=10, height=10)
    with open("maps/random_map_10x10.json", "w", encoding="utf-8") as f:
        json.dump(map_data, f, indent=2)
    print("✅ Map saved to maps/random_map_10x10.json")