import numpy as np
import torch
from model import get_model
from PIL.Image import Image
import PIL.Image


def convert(input_image: Image):
    input_image = input_image.rotate(-90).transpose(PIL.Image.FLIP_LEFT_RIGHT)
    input_image = np.where(np.array(input_image), 1, 0)
    return input_image


def get_model_output(input_image: Image):
    model = get_model()
    model.eval()

    input = torch.from_numpy(convert(input_image)).float()
    input = input.unsqueeze(0).to(model.DEVICE)

    output = model(input).squeeze(0)
    _, top_indices = torch.topk(output, k=2, dim=0)
    return model.LABELS[top_indices[0]], model.LABELS[top_indices[1]]
