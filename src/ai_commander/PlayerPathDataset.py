from torch.utils.data import Dataset
import random

class PlayerPathDataset(Dataset):
    def __init__(self, paths, mcg, unit_type="INF"):
        """
        paths: List[List[str]] - każda lista to ścieżka gracza
        mcg: movement cost graph
        """
        self.samples = []
        self.mcg = mcg
        self.unit_type = unit_type

        for path in paths:
            if len(path) < 4:
                continue
            for i in range(2, len(path) - 1):
                masked = path[i]
                context = path[:i]
                target = path[-1]
                self.samples.append((context, masked, target))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        context, masked, target = self.samples[idx]
        return context, masked, target