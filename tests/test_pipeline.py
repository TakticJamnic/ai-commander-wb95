import json
import os
from ai_commander.tools.map_generator import RandomMapGenerator
from ai_commander.mcg import MovementCostGraphBuilder


if __name__ == "__main__":
    base_directory = "tests/generated/"
    model_name = "clever_aisha"

    ## Get map JSON data
    if (model_name):
        with open (base_directory + model_name + "/map.json") as map_file:
            map_data = [model_name, json.load(map_file)]
    else:
        map_data = RandomMapGenerator().generate(base_directory)
        model_name = map_data[0]

    ## Get Cost Graph
    mcg_file_path = base_directory + model_name + "/mcg.json"
    if (os.path.exists(mcg_file_path)): 
        with open(mcg_file_path) as mcg_file:
            mcg = json.load(mcg_file)
    else: 
        mcg = MovementCostGraphBuilder(map_data=map_data[1]).save_graph(output_base = base_directory + model_name)
    

