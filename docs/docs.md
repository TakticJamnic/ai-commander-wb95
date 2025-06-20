# Documentation

* [Maps](maps/maps.md)
    - [JSON Map](maps/json_maps.md) - what is valid format of map input
    - [Cost Graphs](maps/cost-graphs.md) - how the JSON Map is transformed into Cost Graphs and what it means
    - First Layer Map Tensors
        * 🔄 [M-FLMT](maps/flnt/maneuverability.md) - Maneuverability Tensor — how easily units can traverse the terrain
        * 🛡️ **DP-FLMT** - Defensive Positions Tensor — terrain defensibility and cover
        * 🎯 **VP-FLMT** - Victory Points Tensor — target zones and strategic capture areas
    - Second Layer Map Tensors
        * ⚔️ **A-SLMT** - Attrition Zones — areas where units may suffer gradual losses
        * 💥 **B-SLMT** - Breakthrough Opportunities — points with weak enemy control
        * 🪖 **G-SLMT** - Guarding Zones — essential to hold and control
        * ⏳ **D-SLMT** - Delaying Zones — useful for slowing enemy advance
    - Map Visualiser