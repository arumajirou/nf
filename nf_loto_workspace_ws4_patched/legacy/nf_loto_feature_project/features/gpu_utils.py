import os

try:
    import torch
except Exception:  # torch が無い環境でも動くように
    torch = None

def get_device() -> str:
    if torch is not None and torch.cuda.is_available():
        return "cuda"
    return "cpu"

def get_num_workers(max_workers: int = 4) -> int:
    return min(max_workers, os.cpu_count() or 1)
