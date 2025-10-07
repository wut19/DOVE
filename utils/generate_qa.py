import os
import random
from constants import *
from constants import get_object_hypotheses
import json
import argparse

def get_sample_description(sample, properties):
    """ Get description of the sample """
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
    if "material" in properties:
        description += f" With TENG data, I think the object is made of {sample['material']}."
    return description

def get_sample_comparison(sample1, sample2, properties):
    """ Given a sample, compare another sample with it. Get the comparison results """
    # First generate descriptions for each sample
    description1 = get_sample_description(sample1, properties)
    description2 = get_sample_description(sample2, properties)
    
    # Start the comparison with the descriptions
    comparison = f"For the first object: {description1}\n\nFor the second object: {description2}\n\n"
    
    # Now derive the comparison
    comparison += "I think "
    all_same = True
    same_properties = []
    different_properties = []
    for i in range(len(properties)):
        if sample1[properties[i]] == sample2[properties[i]]:
            same_properties.append(properties[i])
        else:
            all_same = False
            different_properties.append(properties[i])
    if all_same:
        comparison += "they are the same object, because all of their tactile properties are the same."
    else:
        if len(same_properties) == 0:
            comparison += "they are different objects, because "
        else:
            comparison += "they are different objects, because while "
            for i in range(len(same_properties)):
                if i == len(same_properties) - 1:
                    if len(same_properties) > 1:
                        comparison += f"and {same_properties[i]}s "
                    else:
                        comparison += f"{same_properties[i]}s "
                else:
                    comparison += f"{same_properties[i]}s, "
            comparison += "are the same, "
        for i in range(len(different_properties)):
            if i == len(different_properties) - 1:
                if len(different_properties) > 1:
                        comparison += f"and {different_properties[i]}s "
                else:
                    comparison += f"{different_properties[i]}s "
            else:
                comparison += f"{different_properties[i]}s, "
        comparison += "are different."
    return comparison

def get_sample_reason(sample, properties):
    """
    Reason about the object name and its function based on tactile inputs.
    Focus on everyday, common objects that people encounter in daily life.
    
    Args:
        sample: Dictionary containing tactile properties (color, temperature, texture, material)
        properties: List of properties to consider for reasoning
    
    Returns:
        String describing the reasoned object name and function
    """

    object_hypotheses = get_object_hypotheses(sample)
    # Select best hypothesis
    if object_hypotheses:
        best_hypothesis = max(object_hypotheses, key=lambda x: 
                            (({'high': 3, 'medium': 2, 'low': 1}[x['confidence']]), len(x['function'])))
        
        # Chain of thought reasoning
        reasoning = f"Let me think about what this could be in daily life: {best_hypothesis['reasoning']}. "
        
        # Add color context for daily objects
        if sample['color'] in ['red', 'white', 'black', 'blue', 'green', 'yellow'] and sample['color'] != 'unknown':
            reasoning += f"The {sample['color']} color suggests "
            if sample['color'] == 'red':
                reasoning += "something meant to be noticed or associated with food/cooking. "
            elif sample['color'] == 'white':
                reasoning += "cleanliness, hygiene, or purity - common in kitchens and bathrooms. "
            elif sample['color'] == 'black':
                reasoning += "a professional or durable item, often electronics or tools. "
            elif sample['color'] == 'blue':
                reasoning += "something refreshing or casual, like water or everyday clothing. "
            elif sample['color'] == 'green':
                reasoning += "nature, outdoor activities, or eco-friendly products. "
            elif sample['color'] == 'yellow':
                reasoning += "visibility, cheerfulness, or citrus-related items. "
        
        # Add confidence in daily context
        if best_hypothesis['confidence'] == 'high':
            reasoning += "This combination strongly matches common household items I encounter daily. "
        elif best_hypothesis['confidence'] == 'medium':
            reasoning += "This seems like a reasonable everyday item, though it could be one of a few similar things. "
        else:
            reasoning += "This appears to be a household item, though I'd need more details to be certain. "
        
        # Present conclusion
        reasoning += f"I believe this is most likely a {best_hypothesis['name']}. "
        reasoning += f"You would use it {best_hypothesis['function']}."
        
    else:
        reasoning = "Based on these tactile properties, this seems like an everyday household item, but I'd need more specific details to identify exactly what it is and how it's used in daily life."
    
    return reasoning

def generate_qa(start_prompt, json_path, data_path, split, num_samples):
    properties = ["color", "temperature", "texture", "material"]
    
    # prompt setup
    object_property_description = [{
        "object_property_description_0": ["How does it feel to touch <tact_start>", "<img_tokens>", "<img_tokens>","<img_tokens>","<img_tokens>", "<tact_end>?"],
        "object_property_description_1": ["Describe the object <tact_start>", "<img_tokens>","<img_tokens>","<img_tokens>","<img_tokens>", "<tact_end> after touch."],
        "object_property_description_2": ["Could you specify the properties of <tact_start>", "<img_tokens>","<img_tokens>","<img_tokens>","<img_tokens>", "<tact_end> after touching it?"],
        "object_property_description_3": ["How would you characterize the tactile experience of  <tact_start>", "<img_tokens>","<img_tokens>","<img_tokens>","<img_tokens>", "<tact_end>?"],
        "object_property_description_4": ["Can you describe the sensation of touching <tact_start>", "<img_tokens>","<img_tokens>","<img_tokens>","<img_tokens>", "<tact_end>?"],
    }]

    object_comparison = [{
        "object_comparison_description_0": ["I touched two objects: <tact_start>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end> and", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end>. Are they identical?"],
        "object_comparison_description_1": ["After touching these two objects: <tact_start>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end> and", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end>. Do you think they are the same?"],
        "object_comparison_description_2": ["Based on these two touches: <tact_start>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end> and", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end>. Did I feel the same object twice?"],
        "object_comparison_description_3": ["Here's how two objects felt to me: <tact_start>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end> and", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end>. Were they the same?"],
        "object_comparison_description_4": ["I felt two items: <tact_start>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end> and", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end>. Are they the same or different?"],
    }]

    object_reasoning = [{
        "object_reasoning_description_0": ["Based on these tactile properties: <tact_start>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end>. What do you think this object is?"],
        "object_reasoning_description_1": ["Can you identify the object from this touch: <tact_start>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end>?"],
        "object_reasoning_description_2": ["From how it feels: <tact_start>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end>, what do you think this object is used for?"],
        "object_reasoning_description_3": ["What do you think this object is used for based on these tactile properties: <tact_start>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end>?"],
        "object_reasoning_description_4": ["Given this tactile feedback: <tact_start>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end>, what do you think this object is, and what does it do?"],
        "object_reasoning_description_5": ["Can you identify this object and describe its purpose from the tactile information: <tact_start>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<img_tokens>", "<tact_end>?"],
    }]

    if split == "train":
        property_questions = {
            "train_object_property_description": object_property_description,
            "train_object_comparison": object_comparison,
            "train_object_reasoning": object_reasoning,
        }

    elif split == "eval":
        property_questions = {
            "eval_object_property_description": object_property_description,
            "eval_object_comparison": object_comparison,
            "eval_object_reasoning": object_reasoning,
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
            "eval_object_comparison": [],
            "eval_object_reasoning": [],
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
                answer = get_sample_description(sample, properties)
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
        elif question_type == f"{split}_object_comparison":
            for qs in range(question_steps):
                question_key = random.choice(list(property_questions[question_type][qs].keys()))
                question = property_questions[question_type][qs][question_key].copy()
                # get relevant object(s) and their frames
                sample1 = {}
                tactile1 = {}
                sample2 = {}
                tactile2 = {}
                rand_ = random.random()
                if rand_ < 0.9:
                    for key in samples.keys():
                        sample1[key] = random.sample(samples[key].keys(), k=1)[0]
                        tactile1[key] = [random.choice(samples[key][sample1[key]])]
                        rand = random.random()
                        if rand < 0.3:
                            sample2[key] = sample1[key]
                        else:
                            sample2[key] = random.sample(samples[key].keys(), k=1)[0]
                        tactile2[key] = [random.choice(samples[key][sample2[key]])]
                else:
                    for key in samples.keys():
                        sample1[key] = random.sample(samples[key].keys(), k=1)[0]
                        tactile1[key] = [random.choice(samples[key][sample1[key]])]
                        sample2[key] = sample1[key]
                        tactile2[key] = [random.choice(samples[key][sample2[key]])]
                answer = get_sample_comparison(sample1, sample2, properties)
                if qs == 0:     
                    question.insert(0, start_prompt)
                data.append({
                        "role": "USER",
                        "content": question,
                        "tactile": [tactile1, tactile2]
                    })            
                data.append({
                        "role": "ASSISTANT",
                        "content": [answer],
                        "tactile": []
                    })
        elif question_type == f"{split}_object_reasoning":
            for qs in range(question_steps):
                question_key = random.choice(list(property_questions[question_type][qs].keys()))
                question = property_questions[question_type][qs][question_key].copy()
                # get relevant object(s) and their frames
                sample = {}
                tactile = {}
                for key in samples.keys():
                    sample[key] = random.sample(samples[key].keys(), k=1)[0]
                    tactile[key] = [random.choice(samples[key][sample[key]])]
                answer = get_sample_reason(sample, properties)
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

    # create question-answer pairs for each split
    start_prompt = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.\n\n"
    train_json_path = {
        'color': os.path.join('data/color', "train_samples.json"),
        'temperature': os.path.join('data/temperature', "train_samples.json"),
        'texture': os.path.join('data/texture', "train_samples.json"),
        'material': os.path.join('data/teng', "train_samples.json"),
    }
    val_json_path = {
        'color': os.path.join('data/color', "val_samples.json"),
        'temperature': os.path.join('data/temperature', "val_samples.json"),
        'texture': os.path.join('data/texture', "val_samples.json"),
        'material': os.path.join('data/teng', "val_samples.json"),
    }
    
    print("Generating QA...")
    # 1) training
    generate_qa(start_prompt, train_json_path, args.data_path, "train", 30000)
    # 2) evaluation
    generate_qa(start_prompt, val_json_path, args.data_path, "eval", 1000)
    print("Done!")