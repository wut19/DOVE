import pickle 
import torch 
from torch.utils.data import Dataset
import numpy as np
import os
import ast
import csv
import natsort
from PIL import Image
from torchvision import transforms
import random
import json
from utils.constants import *
import glob
import torch.nn.functional as F


def get_frames(frames_path, image_processor, transforms_image, max_length=5, skip=True, return_indices=False):
    # get relevant object(s) and their frames
    tactile_tensors = []
    all_obj_sample_frames = natsort.natsorted(os.path.join(frames_path, i) for i in os.listdir(frames_path))
    num_frames = len(all_obj_sample_frames)
    if num_frames > max_length:
        if skip:
            all_obj_sample_frames = [all_obj_sample_frames[int(num_frames * i/ max_length)] for i in range(0, max_length)]
        else:
            all_obj_sample_frames = natsort.natsorted(random.sample(all_obj_sample_frames, k=max_length))
    
    for frame in all_obj_sample_frames:
        if image_processor is not None:
            if transforms_image is not None:
                tactile_tensors.append(transforms_image(image_processor.preprocess(Image.open(frame).convert('RGB'), return_tensors='pt')['pixel_values'][0]))
            else:
                tactile_tensors.append(image_processor.preprocess(Image.open(frame).convert('RGB'), return_tensors='pt')['pixel_values'][0])
    
    tactile_tensors = torch.stack(tactile_tensors, dim=0) # (l, c, h, w)

    if return_indices:
        frame_indices = [int(i.split("/")[-1].split(".jpg")[0]) for i in all_obj_sample_frames]
        return tactile_tensors, frame_indices
    return tactile_tensors
    

class CLIPPropertyUniqueDataset(Dataset):
    def __init__(self, image_processor, data_path, split_name, flip_p=0):
        super().__init__()
        self.split_name = split_name
        self.flip_p = flip_p
        self.image_processor = image_processor
        self.properties = ["hardness", "roughness", "texture"]
        json_path = [os.path.join(data_path, f"{self.split_name}_samples.json")]
        for i in range(len(json_path)):
            if i == 0:
                with open(json_path[i]) as json_file:
                    self.samples = json.load(json_file)
                    json_file.close()
            else:
                with open(json_path[i]) as json_file:
                    samples_temp = json.load(json_file)
                    json_file.close()
                for k, v in samples_temp.items():
                    if k in self.samples.keys():
                        self.samples[k] += v
                    else:
                        self.samples[k] = v

        self.objects = []
        self.all_samples = []
        for k in self.samples.keys():
            if k not in TRAIN_OBJECTS + VAL_OBJECTS + TEST_OBJECTS:
                continue
            for v in self.samples[k]:
                self.objects.append(k)
                self.all_samples.append(v)

    def get_frames_and_label(self, index, transforms_image):
        # get frames
        objects = self.objects[index]
        video = self.all_samples[index]
        objects_tactile_frames = []
        all_indices = []
        if self.split_name == "train":
            frames, indices = get_frames(video, self.image_processor, transforms_image, skip=False, return_indices=True)
        else:
            frames, indices = get_frames(video, self.image_processor, transforms_image, return_indices=True)
        objects_tactile_frames.append(frames) # [(l, c, h, w)]
        all_indices.append(indices)
        # get label
        hardness_label = RANKS["hardness"][objects]
        roughness_label = RANKS["roughness"][objects]
        texture_label = RANKS["texture"][objects]
        return objects_tactile_frames, hardness_label, roughness_label, texture_label, all_indices
    
    def __len__(self): 
        return len(self.objects)

    def __getitem__(self, index):
        # load tactile info
        transform_list = []
        if self.split_name == "train":
            if random.random() < self.flip_p:
                transform_list.append(transforms.RandomHorizontalFlip(1))
            if random.random() < self.flip_p:
                transform_list.append(transforms.RandomVerticalFlip(1))
        if len(transform_list) == 0:
            transforms_image = None
        else:
            transforms_image = transforms.Compose(transform_list)
        objects_tactile_frames, hardness_label, roughness_label, texture_label, all_indices = self.get_frames_and_label(index, transforms_image=transforms_image)
        return objects_tactile_frames, hardness_label, roughness_label, texture_label, all_indices

class TENGIMUDataset(Dataset):
    def __init__(self, root, img_processor):
        self.root = root
        self.img_processor = img_processor
        self.data_paths = glob.glob(os.path.join(root, '*','*curves_100.png'))
        self.label_dict = {'ABS': 0, 'Acrylic': 1, 'Cloth': 2, 'Metal': 3, 'Nylon': 4, 'PET': 5, 'PLA': 6, 'Resin': 7, 'Rubber': 8, 'Wood': 9}
        # self.transform = transforms.Compose([
        #     transforms.Resize([128, 128]),
        #     # transforms.RandomHorizontalFlip(),
        #     # transforms.RandomVerticalFlip(),
        #     transforms.ToTensor(),
        #     # transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)) 
        # ])

    def __getitem__(self, idx):
        data_path = self.data_paths[idx]
        label_name = data_path.split('/')[-2]
        for key in self.label_dict.keys():
            if key in label_name:
                label = self.label_dict[key]
                break
        # im = Image.open(data_path)
        # im = self.transform(im)[:3,:,:]
        im = self.img_processor.preprocess(Image.open(data_path).convert('RGB'), return_tensors='pt')['pixel_values'][0]

        # dirs = ['ABS', 'ABS2', 'ABS3', 'ABS4', 'ABS5', 'ABS6', 'ABS7']
        # if data_path.split('/')[-2][-1] in ['2', '3', '4', '5', '6', '7']:
        #     index = int(data_path.split('/')[-2][-1])
        #     dir = dirs[index-1]
        # else:
        #     dir = dirs[0]
        # im_path = os.path.join('_labelme', dir, 'label.png')
        # im_tactile = Image.open(im_path)
        # im_tactile = self.transform(im_tactile)

        return im, F.one_hot(torch.tensor([label]), num_classes=len(self.label_dict.keys())).squeeze(0)

    def __len__(self):
        return len(self.data_paths)

def split_data(dataset, cfg):
    indices = list(range(len(dataset)))
    split = int(len(dataset) * cfg['data_split'])
    np.random.shuffle(indices)
    train_indices, val_indices = indices[:split], indices[split:]

    train_sampler = torch.utils.data.sampler.SubsetRandomSampler(train_indices)
    val_sampler = torch.utils.data.sampler.SubsetRandomSampler(val_indices)

    train_data = torch.utils.data.DataLoader(
        dataset,
        batch_size=cfg['batch_size'],
        num_workers=cfg['num_workers'],
        sampler=train_sampler
    )
    val_data = torch.utils.data.DataLoader(
        dataset,
        batch_size=1,
        num_workers=cfg['num_workers'],
        sampler=val_sampler
    )

    return train_data, val_data


class TactileLLMDataset(Dataset):
    def __init__(self, image_processor, files, split_name, tokenizer, flip_p):
        super().__init__()
        self.split_name = split_name
        self.tokenizer = tokenizer
        self.bos_token = tokenizer.bos_token
        self.eos_token = tokenizer.eos_token
        self.pad_token = tokenizer.pad_token
        self.eos_token_number = self.tokenizer.encode(self.eos_token)
        self.flip_p = flip_p
        self.image_processor = image_processor
        self.samples = None
        for f in files:
            with open(f) as json_file:
                if self.samples is None:
                    self.samples = json.load(json_file)
                else:
                    self.samples += json.load(json_file)
                json_file.close()
    
    def __len__(self): 
        return len(self.samples)

    def __getitem__(self, index):
        # 1) sample get questions, answers and tactile paths
        # NOTE: ignore BOS tokens
        transform_list = []
        if self.split_name == "train":
            if random.random() < self.flip_p:
                transform_list.append(transforms.RandomHorizontalFlip(1))
            if random.random() < self.flip_p:
                transform_list.append(transforms.RandomVerticalFlip(1))
            transforms_image = transforms.Compose(transform_list)
        else:
            transforms_image = None
        sample = self.samples[index]
        question_type = sample[0]["question_type"]
        question_step = sample[0]["question_steps"]
        question = []
        tactile = []
        for s in sample[1:-1]:
            if s["role"] == "ASSISTANT":
                question += [s["role"]] + [": "] + s["content"] + [f"{self.eos_token}\n"]
            else:
                question += [s["role"]] + [": "] + s["content"] + ["\n"]
            tactile += s["tactile"]
        question += ["ASSISTANT: "]
        answer = "".join(sample[-1]["content"])
        # 2) get tokens
        answer_tokens = torch.tensor(self.tokenizer.encode(answer + f'{self.eos_token}'), dtype=torch.int64)[1:]
        # 3) get frame tensors
        all_tactile_frames = []
        all_indices = []
        for t in tactile:
            if self.split_name == "train":
                frames, indices = get_frames(t, self.image_processor, transforms_image, skip=False, return_indices=True)
            else:
                frames, indices = get_frames(t, self.image_processor, transforms_image, return_indices=True)
            all_tactile_frames.append(frames)
            all_indices.append(indices)

        return question, answer_tokens, all_tactile_frames, tactile, question_type, question_step, all_indices