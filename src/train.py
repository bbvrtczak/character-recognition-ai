from model import CNN
import torch
from load_dataset import *
import torch.nn as nn


def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    LEARNING_RATE = 5e-4
    NUM_EPOCHS = 20
    BATCH_SIZE = 16

    train_loader, test_loader = load_emnist(BATCH_SIZE)

    model = CNN().to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    step = 0
    total_steps = len(train_loader) * NUM_EPOCHS
    for epoch in range(NUM_EPOCHS):
        for idx, (images, labels) in enumerate(train_loader):
            images = images.to(device)
            labels = labels.to(device)

            print(images[0])
            outputs = model(images)

            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (idx + 1) % 1000 == 0:
                print(f'Epoch: {epoch + 1}/{NUM_EPOCHS} | Step: {step + 1};{total_steps} | Loss: {loss}')
            step += 1


if __name__ == "__main__":
    train()
    print("ok")
