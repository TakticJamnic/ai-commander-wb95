from ai_commander.mcg import MovementCostGraphBuilder

# === ENTRY POINT ===
if __name__ == "__main__":
    builder = MovementCostGraphBuilder.from_file("tests/generated/clever_aisha/generated-map.json")
    builder.save_graph("tests/generated/clever_aisha/movement-cost-graph.json")