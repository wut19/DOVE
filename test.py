import os 
os.environ['HF_ENDPOINT']="https://hf-mirror.com"

from utils.dataset import *

from transformers import CLIPImageProcessor
image_processor = CLIPImageProcessor.from_pretrained("openai/clip-vit-large-patch14")
dataset = RGBDataset(root='_modalities/color', img_processor=image_processor)
for data in dataset:
    print(data[1])