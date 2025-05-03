# SuperTac

Repository containing multimodal tactile dataset, classification algorithms, and DOVE tactile language model.

## Repository Structure
```
- DOVE.zip              # Tactile language model source code
- classification.zip    # Classification algorithms
- dataset.zip           # Multimodal tactile dataset
- weights&logs.zip      # Pre-trained DOVE model weights
```

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
# Install dependencies
pip install -r requirements.txt

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

### Structure
```
- color/
- temperature/
- teng/
- texture/
```