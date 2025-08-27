import os
import random
from constants import *
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
    # Get property values
    color = sample.get('color', 'unknown')
    temperature = sample.get('temperature', 'normal')
    texture = sample.get('texture', 'unknown')
    material = sample.get('material', 'unknown')
    
    # Daily life object hypotheses
    object_hypotheses = []
    
    # RED objects - everyday items
    if color == 'red':
        if material == 'Metal' and temperature == 'hot':
            object_hypotheses.append({
                'name': 'hot cooking pot handle or heated spoon',
                'function': 'for cooking meals, stirring hot soup, or serving hot food at home',
                'reasoning': 'Red color is common for kitchen utensils, metal conducts heat from cooking, and hot temperature indicates recent use in food preparation',
                'confidence': 'high'
            })
        elif material == 'Rubber' and texture == 'dimpled surface':
            object_hypotheses.append({
                'name': 'playground ball or exercise ball',
                'function': 'for children playing games, sports activities, or home fitness exercises',
                'reasoning': 'Red color makes balls visible during play, rubber provides bounce and safety, and dimpled texture helps with grip during games',
                'confidence': 'high'
            })
        elif material == 'PET' and temperature == 'cold':
            object_hypotheses.append({
                'name': 'tomato sauce bottle or fruit juice container',
                'function': 'for storing condiments in the refrigerator or keeping drinks cold',
                'reasoning': 'Red color matches tomato products or fruit drinks, PET is used for food containers, and cold temperature indicates refrigerator storage',
                'confidence': 'high'
            })
        elif material == 'Cloth' and texture == 'smooth surface':
            object_hypotheses.append({
                'name': 'kitchen towel or napkin',
                'function': 'for wiping hands while cooking, cleaning spills, or table setting',
                'reasoning': 'Red is a popular color for kitchen textiles, cloth material absorbs moisture, and smooth texture is comfortable for cleaning',
                'confidence': 'high'
            })
    
    # WHITE objects - clean, hygienic daily items
    elif color == 'white':
        if material == 'Cloth' and texture == 'smooth surface':
            object_hypotheses.append({
                'name': 'bath towel or face cloth',
                'function': 'for drying after shower, washing face, or personal hygiene',
                'reasoning': 'White shows cleanliness and allows easy spot detection, cloth absorbs water well, and smooth texture is gentle on skin',
                'confidence': 'high'
            })
        elif material == 'PET' and temperature == 'cold':
            object_hypotheses.append({
                'name': 'milk bottle or yogurt container',
                'function': 'for storing dairy products in the refrigerator or daily breakfast consumption',
                'reasoning': 'White color is associated with dairy products, PET is food-safe, and cold temperature indicates refrigerated storage',
                'confidence': 'high'
            })
        elif material == 'Metal' and texture == 'grooved edge':
            object_hypotheses.append({
                'name': 'kitchen knife or can opener',
                'function': 'for cutting vegetables, preparing meals, or opening food containers',
                'reasoning': 'White handles are common in kitchen tools for hygiene visibility, metal provides sharpness, and grooved edge indicates cutting function',
                'confidence': 'high'
            })
        elif material == 'Acrylic' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'storage container or food box',
                'function': 'for organizing kitchen items, storing leftovers, or keeping food fresh',
                'reasoning': 'White acrylic is popular for kitchen storage, provides transparency to see contents, and normal temperature indicates pantry storage',
                'confidence': 'high'
            })
    
    # BLACK objects - electronics and tools
    elif color == 'black':
        if material == 'ABS' and texture == 'smooth surface':
            object_hypotheses.append({
                'name': 'TV remote control or smartphone',
                'function': 'for controlling entertainment devices or daily communication',
                'reasoning': 'Black is standard for electronics, ABS plastic is durable for frequent handling, and smooth surface is comfortable to hold',
                'confidence': 'high'
            })
        elif material == 'Rubber' and texture == 'crescent-patterned surface':
            object_hypotheses.append({
                'name': 'car tire or bicycle tire',
                'function': 'for daily transportation, commuting to work, or weekend cycling',
                'reasoning': 'Black rubber is standard for tires, provides durability, and textured surface gives road traction for safe driving',
                'confidence': 'high'
            })
        elif material == 'Metal' and texture == 'grooved edge':
            object_hypotheses.append({
                'name': 'screwdriver or wrench',
                'function': 'for home repairs, assembling furniture, or fixing household items',
                'reasoning': 'Black tools are common for durability, metal provides strength, and grooved edge gives grip for turning screws',
                'confidence': 'high'
            })
        elif material == 'Cloth' and texture == 'smooth surface':
            object_hypotheses.append({
                'name': 'work shirt or pants',
                'function': 'for daily work attire, professional appearance, or casual wear',
                'reasoning': 'Black clothing is versatile and professional, cloth provides comfort, and smooth texture is suitable for daily wear',
                'confidence': 'high'
            })
    
    # BLUE objects - water-related and casual items
    elif color == 'blue':
        if material == 'PET' and temperature == 'cold':
            object_hypotheses.append({
                'name': 'water bottle or sports drink',
                'function': 'for daily hydration, exercise, or staying refreshed throughout the day',
                'reasoning': 'Blue suggests clean water or refreshing drinks, PET is safe for beverages, and cold temperature keeps drinks refreshing',
                'confidence': 'high'
            })
        elif material == 'Cloth' and texture == 'smooth surface':
            object_hypotheses.append({
                'name': 'jeans or casual shirt',
                'function': 'for everyday casual wear, weekend activities, or comfortable clothing',
                'reasoning': 'Blue is classic for casual clothing like jeans, cloth provides comfort, and smooth texture is pleasant to wear',
                'confidence': 'high'
            })
        elif material == 'Acrylic' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'bathroom cup or toothbrush holder',
                'function': 'for daily oral hygiene, holding bathroom items, or morning routine',
                'reasoning': 'Blue acrylic is popular in bathrooms, easy to clean, and normal temperature indicates indoor bathroom use',
                'confidence': 'high'
            })
    
    # GREEN objects - nature and food-related
    elif color == 'green':
        if material == 'PET' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'soda bottle or juice container',
                'function': 'for daily beverages, lunch drinks, or refreshment storage',
                'reasoning': 'Green is common for certain drink brands, PET is standard for beverages, and normal temperature indicates room storage',
                'confidence': 'high'
            })
        elif material == 'Cloth' and texture == 'smooth surface':
            object_hypotheses.append({
                'name': 'garden gloves or cleaning cloth',
                'function': 'for gardening work, household cleaning, or outdoor activities',
                'reasoning': 'Green color suits outdoor work, cloth provides comfort and absorption, and smooth texture is practical for handling',
                'confidence': 'high'
            })
        elif material == 'Rubber' and texture == 'crescent-patterned surface':
            object_hypotheses.append({
                'name': 'garden hose or outdoor mat',
                'function': 'for watering plants, cleaning outdoor areas, or entrance protection',
                'reasoning': 'Green blends with outdoor settings, rubber withstands weather, and textured surface provides grip and drainage',
                'confidence': 'high'
            })
    
    # YELLOW objects - bright and attention-getting
    elif color == 'yellow':
        if material == 'Rubber' and texture == 'dimpled surface':
            object_hypotheses.append({
                'name': 'tennis ball or dog toy',
                'function': 'for sports activities, pet play, or recreational games',
                'reasoning': 'Yellow is standard for tennis balls and visible for pets, rubber provides bounce, and dimpled texture improves grip',
                'confidence': 'high'
            })
        elif material == 'PET' and temperature == 'cold':
            object_hypotheses.append({
                'name': 'lemon juice bottle or sports drink',
                'function': 'for cooking ingredients, refreshing drinks, or post-workout hydration',
                'reasoning': 'Yellow matches citrus flavors, PET is food-safe, and cold temperature keeps drinks refreshing',
                'confidence': 'high'
            })
        elif material == 'Cloth' and texture == 'smooth surface':
            object_hypotheses.append({
                'name': 'cleaning sponge or dish cloth',
                'function': 'for washing dishes, cleaning surfaces, or kitchen maintenance',
                'reasoning': 'Yellow is popular for cleaning supplies, cloth absorbs well, and smooth texture is gentle on surfaces',
                'confidence': 'high'
            })
    
    # Temperature-based reasoning for daily objects
    if temperature == 'hot':
        if material == 'Metal':
            object_hypotheses.append({
                'name': 'coffee mug handle or cooking utensil',
                'function': 'for drinking hot beverages or cooking meals',
                'reasoning': 'Hot temperature indicates recent contact with hot drinks or cooking, metal conducts heat from daily use',
                'confidence': 'high'
            })
        elif material == 'Cloth':
            object_hypotheses.append({
                'name': 'oven mitt or hot towel',
                'function': 'for handling hot cookware or warm comfort during daily activities',
                'reasoning': 'Hot temperature shows recent heating, cloth provides insulation and comfort for safe handling',
                'confidence': 'high'
            })
    
    elif temperature == 'cold':
        if material == 'Metal':
            object_hypotheses.append({
                'name': 'refrigerator handle or ice cream scoop',
                'function': 'for accessing cold storage or serving frozen treats',
                'reasoning': 'Cold temperature indicates contact with refrigerated items, metal conducts cold from daily kitchen use',
                'confidence': 'high'
            })
        elif material == 'PET':
            object_hypotheses.append({
                'name': 'cold beverage bottle or yogurt container',
                'function': 'for refreshing drinks or refrigerated food storage',
                'reasoning': 'Cold temperature indicates refrigerator storage, PET is common for food and drink containers',
                'confidence': 'high'
            })
    
    # Texture-based daily object reasoning
    if texture == 'dimpled surface':
        if material == 'Rubber':
            object_hypotheses.append({
                'name': 'stress ball or massage ball',
                'function': 'for stress relief during work or muscle relaxation at home',
                'reasoning': 'Dimpled texture provides tactile stimulation, rubber offers comfortable firmness for daily stress management',
                'confidence': 'high'
            })
        elif material == 'PET':
            object_hypotheses.append({
                'name': 'sports drink bottle or textured container',
                'function': 'for better grip during exercise or preventing slipping during daily use',
                'reasoning': 'Dimpled texture improves grip, PET is lightweight and safe for beverages during daily activities',
                'confidence': 'medium'
            })
    
    elif texture == 'smooth surface':
        if material == 'Acrylic':
            object_hypotheses.append({
                'name': 'picture frame or storage box',
                'function': 'for displaying family photos or organizing household items',
                'reasoning': 'Smooth surface is easy to clean, acrylic provides clarity and durability for home decoration',
                'confidence': 'high'
            })
        elif material == 'Cloth':
            object_hypotheses.append({
                'name': 'bedsheet or pillow case',
                'function': 'for comfortable sleep and daily rest',
                'reasoning': 'Smooth texture is comfortable against skin, cloth provides softness for daily sleeping comfort',
                'confidence': 'high'
            })
    
    elif texture == 'grooved edge':
        if material == 'Metal':
            object_hypotheses.append({
                'name': 'kitchen knife or bottle opener',
                'function': 'for daily food preparation or opening containers',
                'reasoning': 'Grooved edge provides cutting function, metal ensures sharpness for daily kitchen tasks',
                'confidence': 'high'
            })
        elif material == 'Wood':
            object_hypotheses.append({
                'name': 'cutting board or wooden spoon',
                'function': 'for food preparation or cooking daily meals',
                'reasoning': 'Grooved edge aids in food cutting, wood is food-safe and traditional for kitchen use',
                'confidence': 'high'
            })
    
    # Material-specific daily objects
    if material == 'Wood':
        if temperature == 'normal':
            object_hypotheses.append({
                'name': 'wooden spoon or cutting board',
                'function': 'for cooking, food preparation, or serving meals',
                'reasoning': 'Wood is traditional for kitchen tools, safe for food contact, and normal temperature indicates ready for use',
                'confidence': 'high'
            })
        elif texture == 'smooth surface':
            object_hypotheses.append({
                'name': 'furniture handle or decorative item',
                'function': 'for daily use of cabinets, drawers, or home decoration',
                'reasoning': 'Wood provides natural beauty, smooth surface is comfortable to touch, suitable for daily furniture use',
                'confidence': 'medium'
            })
    
    elif material == 'Nylon':
        if texture == 'smooth surface':
            object_hypotheses.append({
                'name': 'toothbrush or cleaning brush',
                'function': 'for daily oral hygiene or household cleaning',
                'reasoning': 'Nylon is standard for brush bristles, smooth surface is gentle yet effective for daily cleaning',
                'confidence': 'high'
            })
        elif color in ['white', 'blue']:
            object_hypotheses.append({
                'name': 'shower curtain or laundry bag',
                'function': 'for bathroom privacy or organizing clothes',
                'reasoning': 'Nylon is water-resistant and durable, suitable colors for bathroom and laundry use',
                'confidence': 'medium'
            })
    
    elif material == 'Resin':
        if texture == 'smooth surface':
            object_hypotheses.append({
                'name': 'decorative ornament or jewelry',
                'function': 'for home decoration or personal accessories',
                'reasoning': 'Resin allows detailed crafting, smooth surface provides attractive finish for decorative items',
                'confidence': 'medium'
            })
        elif color in ['white', 'black']:
            object_hypotheses.append({
                'name': 'phone case or small container',
                'function': 'for protecting devices or storing small items',
                'reasoning': 'Resin provides protection and customization, popular colors for everyday accessories',
                'confidence': 'medium'
            })
    
    # Common daily combinations
    if color == 'white' and material == 'Cloth' and temperature == 'hot':
        object_hypotheses.append({
            'name': 'fresh laundry or heated towel',
            'function': 'for daily hygiene, comfort, or household maintenance',
            'reasoning': 'White cloth shows cleanliness, hot temperature indicates recent washing or heating for comfort',
            'confidence': 'high'
        })
    
    if color == 'black' and material == 'Rubber' and temperature == 'normal':
        object_hypotheses.append({
            'name': 'phone case or computer mouse',
            'function': 'for protecting devices or daily computer work',
            'reasoning': 'Black rubber is common for device protection, normal temperature indicates regular daily use',
            'confidence': 'high'
        })
    
    # Default fallbacks for daily objects
    if not object_hypotheses:
        if material == 'Metal':
            object_hypotheses.append({
                'name': 'kitchen utensil or household tool',
                'function': 'for daily cooking, food preparation, or home maintenance',
                'reasoning': 'Metal is commonly used in kitchen and household items for durability and functionality',
                'confidence': 'medium'
            })
        elif material == 'Cloth':
            object_hypotheses.append({
                'name': 'clothing item or household textile',
                'function': 'for daily wear, comfort, or home cleaning',
                'reasoning': 'Cloth is fundamental for clothing and household textiles used in daily life',
                'confidence': 'medium'
            })
        elif material == 'PET':
            object_hypotheses.append({
                'name': 'food container or beverage bottle',
                'function': 'for storing drinks, food, or daily consumption items',
                'reasoning': 'PET is widely used for food and beverage containers in daily life',
                'confidence': 'medium'
            })
        elif material in ['ABS', 'PLA']:
            object_hypotheses.append({
                'name': 'household item or electronic device part',
                'function': 'for daily convenience, organization, or device functionality',
                'reasoning': 'Plastic materials are common in household items and electronics used daily',
                'confidence': 'medium'
            })
        elif material == 'Rubber':
            object_hypotheses.append({
                'name': 'grip handle or protective item',
                'function': 'for comfortable handling or protection during daily activities',
                'reasoning': 'Rubber provides comfort and protection in many daily-use items',
                'confidence': 'medium'
            })
        else:
            object_hypotheses.append({
                'name': 'everyday household item',
                'function': 'for daily activities, comfort, or practical use around the home',
                'reasoning': 'The tactile properties suggest a common household item used in daily life',
                'confidence': 'low'
            })
    
    # Select best hypothesis
    if object_hypotheses:
        best_hypothesis = max(object_hypotheses, key=lambda x: 
                            (({'high': 3, 'medium': 2, 'low': 1}[x['confidence']]), len(x['function'])))
        
        # Chain of thought reasoning
        reasoning = f"Let me think about what this could be in daily life: {best_hypothesis['reasoning']}. "
        
        # Add color context for daily objects
        if color in ['red', 'white', 'black', 'blue', 'green', 'yellow'] and color != 'unknown':
            reasoning += f"The {color} color suggests "
            if color == 'red':
                reasoning += "something meant to be noticed or associated with food/cooking. "
            elif color == 'white':
                reasoning += "cleanliness, hygiene, or purity - common in kitchens and bathrooms. "
            elif color == 'black':
                reasoning += "a professional or durable item, often electronics or tools. "
            elif color == 'blue':
                reasoning += "something refreshing or casual, like water or everyday clothing. "
            elif color == 'green':
                reasoning += "nature, outdoor activities, or eco-friendly products. "
            elif color == 'yellow':
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