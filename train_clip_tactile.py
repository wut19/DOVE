import os 
os.environ['HF_ENDPOINT']="https://hf-mirror.com"

import torch.nn as nn 
import torch 
from torch.utils.data import DataLoader
from torch import optim
import tqdm
import json
import numpy as np
from utils.dataset import *
from utils.model import *
from utils.promptclip import *
import random
import yaml
from datetime import datetime
import sys
from transformers import CLIPImageProcessor
from transformers.utils import logging


class PropertyClassifierEvaluator:
    def evaluate(self, preds, labels):
        return self.get_correct_num(preds, labels)
    
    def get_correct_num(self, preds, labels):
        return (torch.argmax(labels, dim=1) == torch.argmax(preds, dim=1)).sum().item()


def main(configs, exp_name, device):
    print(exp_name)
    # data
    image_processor = CLIPImageProcessor.from_pretrained(configs["use_clip"])
    if 'teng' in exp_name:
        dataset = TENGIMUDataset(root=configs['data_dir'], img_processor=image_processor)
    elif 'color' in exp_name:
        dataset = RGBDataset(root=configs['data_dir'], img_processor=image_processor)
    elif 'temperature' in exp_name:
        dataset = TempDataset(root=configs['data_dir'], img_processor=image_processor)
    elif 'texture' in exp_name:
        dataset  = TextureDataset(root=configs['data_dir'], img_processor=image_processor)
    else:
        raise NotImplementedError('Dataset not implemented')
    train_loader, val_loader = split_data(dataset, configs)
    
    # models
    if 'teng' in exp_name:
        num_class = 10
    elif 'color' in exp_name:
        num_class = 6
    elif 'temperature' in exp_name:
        num_class = 3
    elif 'texture' in exp_name:
        num_class = 6
    else:
        raise NotImplementedError(' not implemented')
    encoder = CLIPTactileEncoder(clip_model=configs["use_clip"]).to(device)
    classifier = CLIPClassifier(output_size=configs["output_size"], num_class=num_class).to(device)
    if configs["prompt_learning"]:
        clip = PromptLearningCLIPModel.from_pretrained(configs["use_clip"], configs).to(device)
    else:
        clip = CLIPModel.from_pretrained(configs["use_clip"]).to(device)
    taclip = TactileCLIP(clip, freeze_text_encoder=True).to(device)
    if configs["prompt_learning"]:
        for name, param in taclip.named_parameters():
            # Make sure that VPT prompts are updated
            if "VPT" in name:
                param.requires_grad_(True)
            else:
                param.requires_grad_(False)
    # training
    evaluator = PropertyClassifierEvaluator()
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer_clip = torch.optim.AdamW(taclip.parameters(), lr=configs["lr"])
    optimizer_classifier = torch.optim.AdamW(classifier.parameters(), lr=configs["classifier_lr"])
    scheduler_clip = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer_clip, T_max=len(train_loader) / configs["gradient_accumulation_steps"], eta_min=configs["lr"] / 100)
    scheduler_classifier = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer_classifier, T_max=len(train_loader) / configs["gradient_accumulation_steps"], eta_min=configs["classifier_lr"] / 100)
    best_val_acc = -1
    epochs = configs["num_epochs"]
    for epoch in tqdm.tqdm(range(epochs)):
        total_train_correct = 0
        num_train_samples = 0
        taclip.train()
        classifier.train()
        for train_batch_step, batch in enumerate(t:=tqdm.tqdm(train_loader)):
            objects_tactile_frames, labels = batch
            labels = labels.to(device)
            batch_size = objects_tactile_frames.shape[0]
            vision_features, _, _, _ = taclip(objects_tactile_frames.to(device), None, None)
            preds = classifier(vision_features)
            loss = loss_fn(preds, labels.float()) / configs["gradient_accumulation_steps"]
            loss.backward()
            if (train_batch_step + 1) % configs["gradient_accumulation_steps"] == 0:
                optimizer_clip.step()
                optimizer_classifier.step()
                scheduler_clip.step()
                scheduler_classifier.step()
                optimizer_clip.zero_grad()
                optimizer_classifier.zero_grad()
            num_train_samples += batch_size
            total_train_correct += evaluator.evaluate(preds, labels)
        # validation
        taclip.eval()
        classifier.eval()
        # total_val_correct = 0
        total_val_correct = 0
        num_val_samples = 0
        with torch.no_grad():
            for val_sample_step, batch in enumerate(t:=tqdm.tqdm(val_loader)):
                objects_tactile_frames, labels = batch
                labels = labels.to(device)
                batch_size = objects_tactile_frames.shape[0]
                vision_features, _, _, _ = taclip(objects_tactile_frames.to(device), None, None)
                preds = classifier(vision_features)
                num_val_samples += batch_size
                total_val_correct += evaluator.evaluate(preds, labels)
        print(f"\nTRAIN epoch: {epoch+1} / {epochs}")
        print(f"TRAIN accuracies: {total_train_correct / num_train_samples}")
        print(f"VAL accuracies: {total_val_correct / num_val_samples}")
        if total_val_correct / num_val_samples > best_val_acc:
            print("Saving encoder...")
            best_val_acc = total_val_correct / num_val_samples
            encoder.model.vision_model = taclip.clip_model.vision_model
            torch.save(encoder.state_dict(), f"{configs['exps_path']}/{exp_name}/encoder.pt")
            torch.save(classifier.state_dict(), f"{configs['exps_path']}/{exp_name}/classifier.pt")
            torch.save(taclip.state_dict(), f"{configs['exps_path']}/{exp_name}/taclip.pt")


if __name__ == "__main__":
    # exp_type = f"train_clip_teng"
    # exp_type = f"train_clip_color"
    # exp_type = f"train_clip_temperature"
    exp_type = f"train_clip_texture"
    config_path = f'configs/{exp_type}_config.yaml'
    # get configs
    with open(config_path, 'r') as file:
        configs = yaml.safe_load(file)
    exp_id = input("Identifier for experiment: ")
    if len(exp_id) == 0:
        exp_id = exp_type
    else:
        exp_id = exp_type + "_" + exp_id

    # make stats and weights folders
    now = datetime.now()
    exp_name = now.strftime("%Y_%m_%d_%H_%M_%S")
    exp_name = exp_name + "_" + exp_id
    os.makedirs(f"{configs['exps_path']}", exist_ok=True)
    os.makedirs(f"{configs['exps_path']}/{exp_name}", exist_ok=True)
    with open(f"{configs['exps_path']}/{exp_name}/{exp_type}_config.yaml", 'w') as file:
        documents = yaml.dump(configs, file)
        file.close()

    # log outputs
    sys.stdout = open(f"{configs['exps_path']}/{exp_name}/log.txt", 'w')
    logging.set_verbosity_error()

    # seed
    torch.manual_seed(configs["seed"])
    torch.random.manual_seed(configs["seed"])
    torch.cuda.manual_seed(configs["seed"])
    torch.cuda.manual_seed_all(configs["seed"])
    # torch.use_deterministic_algorithms(True)
    random.seed(configs["seed"])
    def seed_worker(worker_id):
        worker_seed = torch.initial_seed() % 2**32
        np.random.seed(worker_seed)
        random.seed(worker_seed)
    device = f'cuda:{configs["cuda"]}' # for inputs and model if not device_map

    print("Training CLIP...")
    main(configs, exp_name, device)
    print("\nCLIP trained!")