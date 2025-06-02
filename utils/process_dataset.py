import os
import numpy as np
import cv2
import random
import json
import argparse
import glob

def generate_dataset_json(root, output_path, ratio=0.8):
    if 'texture' in root:
        samples = glob.glob(os.path.join(root, '*','rgb/*.jpg'))
    elif 'teng' in root:
        samples = glob.glob(os.path.join(root, '*','*teng_curve.png'))
    elif 'temperature' in root:
        samples = glob.glob(os.path.join(root, '*','*/*.jpg'))
    elif 'color' in root:
        samples = glob.glob(os.path.join(root, '*','*/*.jpg'))
    else:
        raise NotImplementedError()
    
    random.shuffle(samples)
    train_samples = samples[:int(len(samples)*ratio)]
    val_samples = samples[int(len(samples)*ratio):]
    
    train_sample_paths = {}
    val_sample_paths = {}
    for sample in train_samples:
        if 'texture' in root:
            sample_type = sample.split('/')[-3]
        elif 'teng' in root:
            sample_type = sample.split('/')[-2]
            sample_type = ''.join([i for i in sample_type if not i.isdigit()])
        elif 'temperature' in root:
            sample_type = sample.split('/')[-3]
        elif 'color' in root:
            sample_type = sample.split('/')[-3]
        else:
            raise NotImplementedError()
        if sample_type not in train_sample_paths.keys():
            train_sample_paths[sample_type] = [sample]
        else:
            train_sample_paths[sample_type].append(sample)
    
    for sample in val_samples:
        if 'texture' in root:
            sample_type = sample.split('/')[-3]
        elif 'teng' in root:
            sample_type = sample.split('/')[-2]
            sample_type = ''.join([i for i in sample_type if not i.isdigit()])
        elif 'temperature' in root:
            sample_type = sample.split('/')[-3]
        elif 'color' in root:
            sample_type = sample.split('/')[-3]
        else:
            raise NotImplementedError()
        if sample_type not in val_sample_paths.keys():
            val_sample_paths[sample_type] = [sample]
        else:
            val_sample_paths[sample_type].append(sample)
    
    with open(os.path.join(output_path, 'train_samples.json'), 'w') as f:
        json.dump(train_sample_paths, f)
        f.close()
    with open(os.path.join(output_path, 'val_samples.json'), 'w') as f:
        json.dump(val_sample_paths, f)
        f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', default='data/texture/data2', help='directory with tactile data')
    parser.add_argument('--output_path', default='data/texture', help='directory to save processed sample files')
    args = parser.parse_args()
    os.makedirs(args.output_path, exist_ok=True)
    
    generate_dataset_json(args.dataset_path, args.output_path)