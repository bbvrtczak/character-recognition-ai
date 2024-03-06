import torchvision.datasets as datasets
import torchvision.transforms as tfm
from torch.utils.data import DataLoader


def load_emnist(batch_size):
    transforms = tfm.Compose([
        tfm.ToTensor(),
        tfm.Normalize((0.0,), (1.0,))
    ])

    trainset = datasets.EMNIST("../data", "byclass", train=True, download=True, transform=transforms)
    testset = datasets.EMNIST("../data", "byclass", train=False, download=True, transform=transforms)

    train_loader = DataLoader(trainset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(testset, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader
