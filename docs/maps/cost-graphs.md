# 📉 Cost Graphs

🔙 [Back to Documentation](../docs.md) / [← Maps](maps.md)

---

When `cost_graph.py` is fed with a valid `map.json`, it generates two unidirectional graphs representing terrain and obstacle costs for units navigating the battlefield:

- 🔄 **Movement Cost Graph (MCG)** – movement effort between hexes by unit type  
- 🛡️ **Defense Cost Graph (DCG)** – terrain-based defensive advantages on hex-to-hex transitions

---

## 🔄 Movement Cost Graph (MCG)

The MCG defines movement effort required for various unit types to travel between adjacent hexes. Each unit type (e.g., `INF`, `ATV`) has its own cost mapping.

---

### 📄 Example MCG JSON

```json
{
  "INF": {
    "0101": {
      "0102": 0.5,
      "0201": 1
    },
    "0201": {
      "0101": 0.5,
      "0102": 1,
      "0202": 0.5
    },
    "0102": {
      "0101": 1,
      "0202": 1
    },
    "0202": {
      "0102": 1,
      "0201": 0.5
    }
  },
  "ATV": {
    "0101": {
      "0102": 0.33,
      "0201": 1
    },
    "0201": {
      "0101": 0.33,
      "0102": 1,
      "0202": 0.33
    },
    "0102": {
      "0101": 2,
      "0202": 1
    },
    "0202": {
      "0102": 1,
      "0201": 0.33
    }
  }
}

```

## 🛡️ Defence Cost Graph (DCG)
The DCG describes how terrain influences defensive positioning. Currently, a placeholder unit type "CLE" (for "clean" or generic use) is used. Future updates will support advanced unit-type modifiers, such as bonuses in forests or cities.

---
## 📄 Example DCG JSON

``` json
{
  "CLE": {
    "0101": {
      "0102": 1,
      "0201": 0
    },
    "0201": {
      "0101": 1,
      "0102": 0,
      "0202": 1
    },
    "0102": {
      "0101": 0,
      "0202": 0
    },
    "0202": {
      "0102": 0,
      "0201": 1
    }
  }
}
```

## 🧠 Notes

* All connections are directional — costs may differ depending on direction.
* Hex IDs use "columnrow" format, e.g., "0101".
* Values represent cost (MCG) or bonus (DCG); lower is better for MCG, higher is better for DCG.

📘 More in:

* Terrain Rules
* Map Format
* Tensor Generation