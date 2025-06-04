import torch


def test_cuda():
    print("Cuda's availability is %s" % torch.cuda.is_available())
