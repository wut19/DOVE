# SuperTac
## Biomimetic Multimodal Tactile Sens-ing Enables Human-like Robotic Per-ception
Repository containing DOVE tactile language model and multimodal tactile dataset.


## DOVE

### Directory Structure
```
- configs/              # Configuration files
- utils/                # Utility functions and scripts
- train_clip_tactile.py # CLIP encoder finetuning
- train_tllm.py         # Language model training
- requirements.txt      # Dependencies
```

### Usage
1. Configure the virtual environment.
    ```bash
    # create virtual environment for DOVE
    conda create -n dove python=3.8

    # Install dependencies
    pip install -r requirements.txt
    ```
2. Download [dataset](https://cloud.tsinghua.edu.cn/d/f6abfcf5845a42018e2a/files/?p=%2FData%2Fdataset.zip) to `./data` and generate datasets.
    ```bash
    # Preprocess the data and generate training samples and validation samples for each modality

    python utils/process_dataset.py --dataset_path data/color/ --output_path data/color/

    python utils/process_dataset.py --dataset_path data/temperature/ --output_path data/temperature/

    python utils/process_dataset.py --dataset_path data/teng --output_path data/teng

    python utils/process_dataset.py --dataset_path data/texture/data2 --output_path data/texture
    ```
    ```bash
    # Generate Q&A data for LLM training
    python utils/generate_qa.py --data_path data
    ```
3. Finetune the CLIP encoder for each modality.
    ```bash
    python train_clip_tactile.py --exp_type train_clip_color # customize the config file before running

    python train_clip_tactile.py --exp_type train_clip_temperature # customize the config file before running

    python train_clip_tactile.py --exp_type train_clip_teng # customize the config file before running

    python train_clip_tactile.py --exp_type train_clip_texture # customize the config file before running
    ```
4. Train the projection layer and align the tactile and language inputs.
    ```bash
    python train_tllm.py --stage 1 # customize the config file before running
    ```
5. Tune the model end-to-end.
    ```bash
    python train_tllm.py --stage 2 # customize the config file before running
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
