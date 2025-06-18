# 🧭 Map Processing Overview

🔙 [Back to Documentation](../docs.md)

---

The **AI Commander** processes structured **JSON Map** files to build internal **Cost Graphs**, which are then transformed into a series of hierarchical **Map Tensors**. These tensors represent various strategic layers of the battlefield and drive AI decision-making.

---

## 🧮 Map Tensor Pipeline

### 📦 1. JSON Map Input

The starting point of the map pipeline. The JSON map contains complete terrain, topology, and metadata.

🔗 See [JSON Maps](json-maps.md) for full structure and examples.

---

### 🧠 2. Cost Graph Construction

From the raw map input, AI Commander builds **two directional graphs** representing movement and defense values between neighboring hexes:

- 🧭 **Movement Cost Graph (MCG)**  
- 🛡️ **Defense Cost Graph (DCG)**  

These graphs take into account terrain types, road networks, and river obstacles.

🔗 More in [Cost Graphs](cost-graphs.md)

---

### 🧱 3. First Layer Map Tensors (FLMT)

These tensors are directly derived from the cost graphs and encode essential battlefield features:

| Tensor | Description |
|--------|-------------|
| 🔄 **M-FLMT** | Maneuverability Tensor — how easily units can traverse the terrain |
| 🛡️ **DP-FLMT** | Defensive Positions Tensor — terrain defensibility and cover |
| 🎯 **VP-FLMT** | Victory Points Tensor — target zones and strategic capture areas |

---

### 🧬 4. Second Layer Map Tensors (SLMT)

Based on FLMT analysis, AI Commander creates **higher-order tactical abstractions** to reason about strategy:

| Tensor | Description |
|--------|-------------|
| ⚔️ **A-SLMT** | Attrition Zones — areas where units may suffer gradual losses |
| 💥 **B-SLMT** | Breakthrough Opportunities — points with weak enemy control |
| 🪖 **G-SLMT** | Guarding Zones — essential to hold and control |
| ⏳ **D-SLMT** | Delaying Zones — useful for slowing enemy advance |

These tensors form the input into **AI Commander’s strategic and tactical engine**, enabling it to propose intelligent, context-aware movements.

---

✅ **Summary:**

> JSON Map → Cost Graphs → FLMT → SLMT → AI Decisions

