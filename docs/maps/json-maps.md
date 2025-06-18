# 🗂️ JSON Map Format

🔙 [Back to Documentation](../docs.md) / [← Maps Overview](maps.md)

---

The **AI Commander** uses a structured and extensible **JSON-based map format** to define the battlefield. Each map encodes essential gameplay elements such as terrain, movement rules per unit type, obstacles like rivers, and connections via road networks.

---

## 📦 Supported Sections

| Section     | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `metadata`  | General information like map name, authorship, width and height            |
| `terrain`   | Definitions of terrain types and their movement costs / defense bonuses    |
| `hexes`     | Hex grid layout with terrain assignments                                   |
| `roads`     | Road segments connecting hexes with road type and name                     |
| `rivers`    | Water obstacles placed between hexes, impacting movement and strategy      |

---

## 🧾 Example: Map JSON Format

```json
{
  "metadata": {
    "authors": ["XYZ"],
    "name": "Sample Map",
    "width": 2,
    "height": 2
  },
  "terrain": {
    "FOREST": {
      "move_cost": { "INF": 1, "ATV": 2 },
      "defence_bonus": 2
    },
    "CLEAR": {
      "move_cost": { "INF": 1, "ATV": 1 }
    },
    "ROAD": {
      "move_cost": { "INF": 0.5, "ATV": 0.33 }
    },
    "STREAM": {
      "move_cost": { "INF": 2, "ATV": 4 },
      "defence_bonus": 1
    }
  },
  "hexes": {
    "0101": "FOREST",
    "0201": "CLEAR",
    "0102": "CLEAR",
    "0202": "CLEAR"
  },
  "roads": {
    "road-572": {
      "name": "Route 572",
      "type": "ROAD",
      "hexes": ["0101", "0201", "0202"]
    }
  },
  "rivers": {
    "osil": {
      "name": "Osil River",
      "type": "STREAM",
      "segments": ["0101-0201", "0201-0202"]
    }
  }
}
```

## 🧠 Notes

* Hex IDs follow a columnrow pattern, using two-digit numbers: e.g., "0101" means column 01, row 01.

* move_cost is defined per unit type: "INF", "ATV", etc.

* segments in rivers define obstacles between hexes, not on hexes.

* You can extend terrain, roads, and rivers types freely in your own scenarios.

📘 More in:

Creating Custom Maps

Visualizing Maps