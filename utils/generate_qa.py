import os
import random
from constants import *
import json
import argparse

def get_sample_description_custom(sample, properties):
    description = "After touch, I feel that"
    assert len(properties) >= 1
    if 'color' in properties:
        description += f" the object is in {sample['color']} color"
    if 'color' in properties and "temperature" in properties:
        description += f" and"
    else:
        description += "."
    if "temperature" in properties:
        description += f" it is {TEMPERATURE_MAPS[sample['temperature']]} to touch."
    if "texture" in properties:
        description += " "
        description += random.choice(TEXTURE_DESCRIPTIONS[sample['texture']])
    if "teng" in properties:
        description += f" With TENG data, I think the object is made of {sample['teng']}."
    return description

def generate_one_step_qa_custom(start_prompt, json_path, data_path, split, num_samples, use_unstructured, use_properties):
    properties = ["color", "temperature", "texture", "teng"]
    
    # prompt setup
    object_property_description = [{
        "object_property_description_0": ["How does it feel to touch <tact_start>", "<img_tokens>", "<img_tokens>","<img_tokens>","<img_tokens>", "<tact_end>?"],
        "object_property_description_1": ["Describe the object <tact_start>", "<img_tokens>","<img_tokens>","<img_tokens>","<img_tokens>", "<tact_end> after touch."],
        "object_property_description_2": ["Could you specify the properties of <tact_start>", "<img_tokens>","<img_tokens>","<img_tokens>","<img_tokens>", "<tact_end> after touching it?"],
    }]

    if split == "train":
        property_questions = {
            "train_object_property_description": object_property_description,
        }
        # if use_properties:
        #     property_questions["train_object_property_description"] = object_property_description
    elif split == "eval":
        property_questions = {
            "eval_object_property_description": object_property_description,
        }

    # load samples
    samples = {}
    for key, path in json_path.items():
        with open(path) as json_file:
            samples[key] = json.load(json_file)
            json_file.close()

    # data
    all_data = []

    if split == "eval":
        existing = {
            "eval_object_property_description": [],
        }
    
    for i in range(num_samples):
        if split == "eval":
            exist = False
        question_type = random.choice(list(property_questions.keys()))
        question_steps =  random.randint(1, len(property_questions[question_type]))
        data = [{
            "question_type": question_type,
            "question_steps": question_steps
        }]
        if question_type == f"{split}_object_property_description":
            for qs in range(question_steps):
                question_key = random.choice(list(property_questions[question_type][qs].keys()))
                question = property_questions[question_type][qs][question_key].copy()
                # get relevant object(s) and their frames
                sample = {}
                tactile = {}
                for key in samples.keys():
                    sample[key] = random.sample(samples[key].keys(), k=1)[0]
                    tactile[key] = [random.choice(samples[key][sample[key]])]
                answer = get_sample_description_custom(sample, properties)
                if qs == 0:
                    question.insert(0, start_prompt)
                data.append({
                        "role": "USER",
                        "content": question,
                        "tactile": [tactile]
                    })
                data.append({
                        "role": "ASSISTANT",
                        "content": [answer],
                        "tactile": []
                    })
        else:
            raise NotImplementedError('Question type not implemented')
        
        if split == "eval":
            if not exist:
                all_data.append(data)
        else:
            all_data.append(data)

    # save all data
    if split == "eval":
        file_name = f"test_qa"
    else:
        file_name = f"{split}_qa"
    # if not use_properties:
    #     file_name += "_no_properties"
    # if not use_unstructured:
    #     file_name += "_no_unstructured"
    data_file = open(os.path.join(data_path, f"{file_name}.json"), "w")
    json.dump(all_data, data_file, indent=4) 
    data_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', help='directory to save processed frames and sample files')
    args = parser.parse_args()

    use_unstructured = False
    use_tactile = True
    use_properties = True
    # create question-answer pairs for each split
    start_prompt = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.\n\n"
    train_json_path = {
        'color': os.path.join('data/color', "train_samples.json"),
        'temperature': os.path.join('data/temperature', "train_samples.json"),
        'texture': os.path.join('data/texture', "train_samples.json"),
        'teng': os.path.join('data/teng', "train_samples.json"),
    }
    val_json_path = {
        'color': os.path.join('data/color', "val_samples.json"),
        'temperature': os.path.join('data/temperature', "val_samples.json"),
        'texture': os.path.join('data/texture', "val_samples.json"),
        'teng': os.path.join('data/teng', "val_samples.json"),
    }
    
    print("Generating QA...")
    # 1) training
    generate_one_step_qa_custom(start_prompt, train_json_path, args.data_path, "train", 30000, use_unstructured, use_properties)
    # 2) evaluation
    generate_one_step_qa_custom(start_prompt, val_json_path, args.data_path, "eval", 1000, use_unstructured, use_properties)
    print("Done!")