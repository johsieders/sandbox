import torch


def test_mps():
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        x = torch.ones(1, device=device)
        print(x)
    else:
        print("\nMPS device not found.")


def test_cuda():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        x = torch.ones(1, device=device)
        print(x)
    else:
        print("\Cuda device not found.")
