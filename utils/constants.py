
TEMPERATURE_MAPS = {
    'cold': 'cold',
    'hot': 'hot',
    'normal': 'at room temperature',
}

TEXTURE_DESCRIPTIONS = {
    'D1':[
        'The object appears to have a spherical shape, the texture of which seems to be with noticeable dimples.',
        'The object exhibits a spherical shape, with a texture characterized by prominent dimples.',
        'Despite its spherical form, the object\'s surface texture is marked by distinct dimples.',
        'The object appears to be spherical, with its surface texture notably featuring dimples.',
        'The spherical shape of the object is complemented by a texture that includes visible dimples.',
        'While the object has a generally spherical shape, its texture is defined by noticeable dimples.',
    ],
    'D2':[
        'The texture remains generally smooth, but there are very subtle and narrow undulations that suggest it might have a gentle, almost imperceptible unevenness. ',
        'The surface texture is largely smooth, though it displays narrow and subtle undulations that imply a slight, nearly imperceptible irregularity.',
        'Despite its overall smooth appearance, the texture contains narrow and faint undulations, indicating a gentle and barely noticeable unevenness.',
        'The texture maintains a generally smooth surface, yet closer inspection reveals narrow, subtle undulations that suggest a minor, almost undetectable unevenness.',
        'Although the texture appears predominantly smooth, it exhibits narrow, delicate undulations that hint at a slight, nearly imperceptible unevenness.',
        'The texture, while mostly smooth, is characterized by narrow and subtle variations that introduce a gentle, almost imperceptible unevenness.',
    ],
    'D3':[
        'The object has raised, somewhat uneven surfaces, while the surrounding area appears to have a few shallow grooves or dimples.',
        'The object features raised, slightly uneven surfaces, contrasted by the surrounding area, which displays a few shallow grooves or dimples.',
        'While the object has raised and somewhat irregular surfaces, the adjacent areas are marked by a series of shallow grooves or dimples.',
        'The surface of the object is characterized by elevated, somewhat uneven areas, with the surrounding region showing a few shallow dimples or grooves.',
        'The object presents raised surfaces with slight irregularities, while the surrounding area contains a number of shallow grooves or dimples.',
        'The raised and somewhat uneven surfaces of the object are complemented by surrounding areas that exhibit shallow grooves or dimples.',
    ],
    'D4':[
        'The object has a smooth texture but introduces a noticeable indentation or groove running across the surface.',
        'The object features a smooth texture, interrupted by a distinct indentation or groove traversing its surface.',
        'Despite its overall smooth texture, the object presents a prominent indentation or groove that runs across the surface.',
        'The surface of the object is generally smooth, but it incorporates a noticeable indentation or groove along its length.',
        'The object\'s texture is predominantly smooth, yet it includes a distinct groove or indentation extending across the surface.',
        'While the object maintains a smooth texture, a noticeable groove or indentation disrupts the continuity of the surface.',
    ],
    'D5':[
        'The texture remains generally smooth, but there are very subtle and wide undulations that suggest it might have a gentle, almost imperceptible unevenness.',
        'The surface texture appears predominantly smooth, yet it exhibits faint and broad undulations that imply a slight, nearly imperceptible irregularity.',
        'Despite its generally smooth appearance, the texture reveals wide and subtle undulations, indicating a gentle and barely noticeable unevenness.',
        'The texture retains an overall smoothness, but closer examination reveals subtle, broad undulations that suggest a minor, almost undetectable irregularity.',
        'Although the texture is mostly smooth, it features wide, faint undulations that hint at a slight, nearly imperceptible unevenness.',
        'The texture, while generally smooth, contains subtle and broad variations that introduce a gentle, almost imperceptible unevenness to the surface.',
    ],
    'D7':[
        'The object has a textured surface with a repeating pattern that resembles a series of small, raised, crescent-shaped bumps or scales. The pattern is uniform, covering the entire surface of the object.',
        'The object features a textured surface characterized by a uniform pattern of small, raised, crescent-shaped bumps or scales that cover the entire surface.',
        'The surface of the object is textured with a repeating pattern resembling a series of crescent-shaped, raised bumps or scales, uniformly distributed across the entire surface.',
        'A consistent pattern of small, raised, crescent-shaped bumps or scales covers the entire surface of the object, giving it a textured appearance.',
        'The object’s surface is uniformly textured with a repeating pattern of crescent-shaped, raised bumps or scales that extend across its entirety.',
        'The textured surface of the object is defined by a regular pattern of small, raised, crescent-shaped bumps or scales, which covers the entire object uniformly.',
    ],
}


def get_object_hypotheses(sample):
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
    return object_hypotheses