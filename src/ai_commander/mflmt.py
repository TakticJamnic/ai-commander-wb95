import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.nn import CrossEntropyLoss
from tqdm import tqdm
import os

class ManueverabilityFirstLayerMapTensor(nn.Module):
    def __init__(self, embedding_dim=32):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.hex_embed = nn.Embedding(10000, embedding_dim)  # max 10k hexes
        self.linear_path = nn.Linear(embedding_dim, embedding_dim)
        self.linear_target = nn.Linear(embedding_dim, embedding_dim)
        self.output_layer = nn.Linear(embedding_dim, 1)

    def forward(self, path_ids, target_id, mcg, unit_type):
        device = next(self.parameters()).device
        hex_to_idx = lambda hex_id: int(hex_id)

        path_tensor = torch.tensor([hex_to_idx(h) for h in path_ids], dtype=torch.long, device=device)
        path_embed = self.hex_embed(path_tensor).mean(dim=0)

        target_tensor = torch.tensor([hex_to_idx(target_id)], dtype=torch.long, device=device)
        target_embed = self.hex_embed(target_tensor).squeeze(0)

        combined_context = self.linear_path(path_embed) + self.linear_target(target_embed)

        current_hex = path_ids[-1]
        neighbors = mcg.get(unit_type, {}).get(current_hex, {})

        if not neighbors:
            return None

        candidate_ids = list(neighbors.keys())
        candidate_tensor = torch.tensor([hex_to_idx(h) for h in candidate_ids], dtype=torch.long, device=device)
        candidate_embeds = self.hex_embed(candidate_tensor)

        scores = self.output_layer(F.relu(candidate_embeds + combined_context))
        probs = F.softmax(scores.squeeze(1), dim=0)

        return candidate_ids, probs

    def hex_to_int(self, hex_id): return int(hex_id)

    def train_mflmt(self, dataset, epochs=5, batch_size=1, lr=1e-3, model_dir="models", model_name="mflmt.pt"):
        dataloader = DataLoader(dataset, shuffle=True, batch_size=batch_size)
        optimizer = torch.optim.Adam(self.parameters(), lr=lr)
        loss_fn = CrossEntropyLoss()

        for epoch in range(epochs):
            total_loss = 0
            for batch in tqdm(dataloader, desc=f"Epoch {epoch+1}"):
                context_batch, target_hex_batch, goal_batch = batch
                loss = 0

                for context, true_next_hex, goal in zip(context_batch, target_hex_batch, goal_batch):
                    context = list(context)
                    candidate_ids, probs = self(context, goal, dataset.mcg, dataset.unit_type)

                    if probs is None or true_next_hex not in candidate_ids:
                        continue

                    true_idx = candidate_ids.index(true_next_hex)
                    target = torch.tensor([true_idx], dtype=torch.long, device=probs.device)
                    loss += loss_fn(probs.unsqueeze(0), target)

                if loss > 0:
                    loss.backward()
                    optimizer.step()
                    optimizer.zero_grad()
                    total_loss += loss.item()

            print(f"✅ Epoch {epoch+1} Loss: {total_loss:.4f}")

        # 🔽 Zapisz model
        os.makedirs(model_dir, exist_ok=True)
        full_path = os.path.join(model_dir, model_name)
        torch.save(self.state_dict(), full_path)
        print(f"💾 Model saved to {full_path}")