from ai_commander.maps.flmt.train.MFMLT import MFLMT
from ai_commander.maps.flmt.train.PlayerPathDataset import PlayerPathDataset
from ai_commander.maps.flmt.train.trainer import train_mflmt
import json

def suggest_next_move(model, current_path, goal, mcg, unit_type):
    candidate_ids, probs = model(current_path, goal, mcg, unit_type)
    return list(zip(candidate_ids, probs.tolist()))

if __name__ == "__main__":
    # Dane
    paths = [
        ["0101", "0102", "0202", "0302", "0403", "0503"],
        ["0201", "0202", "0302", "0402", "0502"],
        ["0301", "0302", "0402", "0503"]
    ]

    with open('generated/movement-cost-graph.json') as f:
        mcg = json.load(f)

        # Model + dane
        model = MFLMT()
        dataset = PlayerPathDataset(paths, mcg, unit_type="INF")

        # Trenuj
        train_mflmt(model, dataset, epochs=10)

        # Test
        moves = suggest_next_move(model, ["0101", "0102", "0202"], "0503", mcg, "INF")
        print("➡️ Suggested next hexes:")
        for hex_id, prob in moves:
            print(f"{hex_id}: {prob:.3f}")