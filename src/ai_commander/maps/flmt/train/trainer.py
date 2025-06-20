import torch
from torch.utils.data import DataLoader
from torch.nn import CrossEntropyLoss
from tqdm import tqdm

def hex_to_int(hex_id): return int(hex_id)

def train_mflmt(model, dataset, epochs=5, batch_size=1, lr=1e-3):
    dataloader = DataLoader(dataset, shuffle=True, batch_size=batch_size)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = CrossEntropyLoss()

    for epoch in range(epochs):
        total_loss = 0
        for batch in tqdm(dataloader, desc=f"Epoch {epoch+1}"):
            context_batch, target_hex_batch, goal_batch = batch
            loss = 0

            for context, true_next_hex, goal in zip(context_batch, target_hex_batch, goal_batch):
                context = list(context)
                candidate_ids, probs = model(context, goal, dataset.mcg, dataset.unit_type)

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