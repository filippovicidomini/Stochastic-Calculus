
import torch
print("PyTorch:", torch.__version__)
print("MPS available:", torch.backends.mps.is_available())
print("MPS built:", torch.backends.mps.is_built())
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print("Using device:", device)

# test_mps.py
import torch, time
dev = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

def bench(device, N=4096*2):
    a = torch.randn(N, N, device=device, dtype=torch.float32)
    b = torch.randn(N, N, device=device, dtype=torch.float32)
    # warmup
    for _ in range(3): (a @ b).sum().item()
    torch.mps.synchronize() if device.type=="mps" else None

    t0 = time.time()
    c = (a @ b).sum()
    torch.mps.synchronize() if device.type=="mps" else None
    dt = time.time() - t0
    return float(c), dt

for d in [torch.device("cpu"), dev]:
    val, sec = bench(d)
    print(f"{d}: {sec:.3f}s, result={val}")