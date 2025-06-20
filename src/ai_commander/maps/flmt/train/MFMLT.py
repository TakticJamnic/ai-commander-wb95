import torch
import torch.nn as nn
import torch.nn.functional as F

class MFLMT(nn.Module):
    def __init__(self, embedding_dim=32):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.hex_embed = nn.Embedding(10000, embedding_dim)  # zakładamy max 10k heksów
        self.linear_path = nn.Linear(embedding_dim, embedding_dim)
        self.linear_target = nn.Linear(embedding_dim, embedding_dim)
        self.output_layer = nn.Linear(embedding_dim, 1)  # ocena kandydata

    def forward(self, path_ids, target_id, mcg, unit_type):
        """
        path_ids: List[str] - sekwencja odwiedzonych heksów (np. ["0101", "0102"])
        target_id: str - docelowy heks (np. "0505")
        mcg: dict - movement cost graph
        unit_type: str - jednostka ("INF", "ATV")
        """

        device = next(self.parameters()).device
        hex_to_idx = lambda hex_id: int(hex_id)  # np. "0101" -> 101

        # Embedding ścieżki (średnia)
        path_tensor = torch.tensor([hex_to_idx(h) for h in path_ids], dtype=torch.long, device=device)
        path_embed = self.hex_embed(path_tensor).mean(dim=0)  # (E,)

        # Embedding celu
        target_tensor = torch.tensor([hex_to_idx(target_id)], dtype=torch.long, device=device)
        target_embed = self.hex_embed(target_tensor).squeeze(0)  # (E,)

        # Połącz embeddingi
        combined_context = self.linear_path(path_embed) + self.linear_target(target_embed)  # (E,)

        # Ostatni heks jako źródło ruchu
        current_hex = path_ids[-1]
        neighbors = mcg.get(unit_type, {}).get(current_hex, {})

        if not neighbors:
            return None  # brak sąsiadów

        # Embedding sąsiadów i scoring
        candidate_ids = list(neighbors.keys())
        candidate_tensor = torch.tensor([hex_to_idx(h) for h in candidate_ids], dtype=torch.long, device=device)
        candidate_embeds = self.hex_embed(candidate_tensor)  # (N, E)

        # Dodaj kontekst i oceniaj
        scores = self.output_layer(F.relu(candidate_embeds + combined_context))  # (N, 1)
        probs = F.softmax(scores.squeeze(1), dim=0)  # (N,)

        return candidate_ids, probs  # lista sąsiadów i ich prawdopodobieństwa