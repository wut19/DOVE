# SuperTac

Repository containing DOVE tactile language model and multimodal tactile dataset.


## DOVE

### Directory Structure
```
- configs/              # Configuration files
- utils/                # Utility functions
- train_clip_tactile.py # CLIP encoder finetuning
- train_tllm.py         # Language model training
- requirements.txt      # Dependencies
```

### Usage

```bash

# create virtual environment for DOVE
conda create -n dove python=3.8

# Install dependencies
pip install -r requirements.txt

# preprocess the data and generate training samples and validation samples for each modality

python utils/process_dataset.py --dataset_path data/color/ --output_path data/color/

python utils/process_dataset.py --dataset_path data/temperature/ --output_path data/temperature/

python utils/process_dataset.py --dataset_path data/teng --output_path data/teng

python utils/process_dataset.py --dataset_path data/texture/data2 --output_path data/texture

# Finetune CLIP encoder (modify config path in script)
python train_clip_tactile.py

# Generate Q&A data for LLM training
python utils/generate_qa.py --data_path [dataset_path]

# Train tactile language model (modify config path in script)
python train_tllm.py
```

The training process includes two stages:
1. Embedding alignment to the same vector space
2. Language model backbone finetuning

Pre-trained weights and experiment logs are available in `weights&logs.zip`.

## Dataset
Dataset can be found at [this address](https://cloud.tsinghua.edu.cn/d/f6abfcf5845a42018e2a/files/?p=%2FData%2Fdataset.zip)
### Structure
```
- color/
- temperature/
- teng/
- texture/
```