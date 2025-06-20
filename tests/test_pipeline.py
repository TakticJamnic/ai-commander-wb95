import json
import os
from ai_commander.tools.map_generator import RandomMapGenerator
from ai_commander.mcg import MovementCostGraphBuilder
from ai_commander.mflmt import ManueverabilityFirstLayerMapTensor
from ai_commander.PlayerPathDataset import PlayerPathDataset
from ai_commander.tools.path_generator import PathGenerator


def suggest_next_move(model, current_path, goal, mcg, unit_type):
    candidate_ids, probs = model(current_path, goal, mcg, unit_type)
    return list(zip(candidate_ids, probs.tolist()))

if __name__ == "__main__":
    base_directory = "tests/generated/"
    model_name = "clever_aisha"

    ## Get map JSON data
    if (model_name):
        output_file = base_directory + model_name + "/map.json"
        with open (output_file) as map_file:
            map_data = [model_name, json.load(map_file)]
            print(f"✅ Map already exists in ➡️  {output_file}")
    else:
        map_data = RandomMapGenerator().generate(base_directory)
        model_name = map_data[0]

    model_directory = base_directory + model_name

    ## Get Cost Graph
    mcg_file_path = model_directory + "/mcg.json"
    if (os.path.exists(mcg_file_path)): 
        with open(mcg_file_path) as mcg_file:
            mcg = json.load(mcg_file)
            print(f"✅ MCG already exists in ➡️  {mcg_file_path}")
    else: 
        mcg = MovementCostGraphBuilder(map_data=map_data[1]).save_graph(output_base = model_directory)
    
    ## Train M-FLMT
    # Data
    paths_file = model_directory + "/paths.txt"
    
    path_generator = PathGenerator(mcg_file_path, unit_type="INF")
    sample_pairs = path_generator.generate_unique_pairs(count=2000)

    paths = path_generator.generate_paths(sample_pairs, paths_file)

    # Model
    mflmt = ManueverabilityFirstLayerMapTensor()
    dataset = PlayerPathDataset(paths, mcg, unit_type="INF")

    # Train
    mflmt.train_mflmt(dataset, epochs=100)

    # Test
    moves = suggest_next_move(mflmt, ["0101", "0102", "0202"], "0503", mcg, "INF")
    print("➡️ Suggested next hexes:")
    for hex_id, prob in moves:
        print(f"{hex_id}: {prob:.3f}")

