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
    comparison = "I think "
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
    
    Args:
        sample: Dictionary containing tactile properties (color, temperature, texture, material)
        properties: List of properties to consider for reasoning
    
    Returns:
        String describing the reasoned object name and function
    """
    # Object reasoning based on tactile properties
    reasoning = ""
    
    # Get property values
    color = sample.get('color', 'unknown')
    temperature = sample.get('temperature', 'normal')
    texture = sample.get('texture', 'unknown')
    material = sample.get('material', 'unknown')
    
    # Reasoning logic based on property combinations
    object_hypotheses = []
    
    # Highly specific color-material-texture-temperature combinations
    
    # RED objects - very specific identification
    if color == 'red':
        if material == 'Metal' and temperature == 'hot':
            object_hypotheses.append({
                'name': 'heated kitchen knife or soldering iron tip',
                'function': 'for cutting hot food materials or joining electronic components through heat application',
                'reasoning': 'The red color indicates emergency/warning context, metal material suggests durability and heat conduction, and hot temperature confirms active heating use',
                'confidence': 'high'
            })
        elif material == 'Metal' and texture == 'D4':
            object_hypotheses.append({
                'name': 'emergency fire axe blade or rescue tool',
                'function': 'for breaking through doors, cutting rescue openings, or emergency building access',
                'reasoning': 'Red color signals emergency equipment, metal provides necessary strength, and grooved edge texture indicates a cutting edge design',
                'confidence': 'high'
            })
        elif material == 'Rubber' and texture == 'D1':
            object_hypotheses.append({
                'name': 'dodgeball or kickball',
                'function': 'for playground games, physical education classes, or recreational sports activities',
                'reasoning': 'Red color enhances visibility for sports, rubber material provides bounce and safety, and dimpled surface texture improves grip during play',
                'confidence': 'high'
            })
        elif material == 'Rubber' and texture == 'D7':
            object_hypotheses.append({
                'name': 'emergency vehicle tire tread or safety grip mat',
                'function': 'for providing maximum traction on wet surfaces or emergency vehicle stopping power',
                'reasoning': 'Red indicates emergency/safety use, rubber material provides flexibility and grip, and crescent-patterned texture maximizes surface contact for traction',
                'confidence': 'high'
            })
        elif material == 'PET' and temperature == 'cold':
            object_hypotheses.append({
                'name': 'ketchup bottle or tomato juice container',
                'function': 'for storing and dispensing condiments or vegetable-based beverages in refrigerated conditions',
                'reasoning': 'Red color matches tomato-based products, PET material is food-safe and transparent, and cold temperature indicates refrigerated storage',
                'confidence': 'high'
            })
        elif material in ['ABS', 'PLA'] and texture == 'D1':
            object_hypotheses.append({
                'name': '3D printed stress ball or fidget toy',
                'function': 'for anxiety relief, hand exercise, or therapeutic grip strengthening activities',
                'reasoning': 'Red color provides visual stimulation for therapy, ABS/PLA indicates custom 3D printing, and dimpled surface texture enhances tactile feedback',
                'confidence': 'high'
            })
    
    # WHITE objects - medical/clean applications
    elif color == 'white':
        if material == 'Acrylic' and temperature == 'cold':
            object_hypotheses.append({
                'name': 'laboratory sample container or medical specimen holder',
                'function': 'for sterile storage of biological samples, chemical reagents, or pharmaceutical preparations',
                'reasoning': 'White color indicates sterile medical environment, acrylic provides chemical resistance and transparency, and cold temperature preserves sample integrity',
                'confidence': 'high'
            })
        elif material == 'Cloth' and texture == 'D2':
            object_hypotheses.append({
                'name': 'surgical bandage or medical gauze',
                'function': 'for wound dressing, blood absorption, or post-operative care in clinical settings',
                'reasoning': 'White color shows cleanliness and allows contamination detection, cloth material provides absorbency, and smooth weave texture indicates soft medical-grade material',
                'confidence': 'high'
            })
        elif material == 'Metal' and texture == 'D4':
            object_hypotheses.append({
                'name': 'surgical scalpel or medical cutting instrument',
                'function': 'for precise tissue incision, surgical procedures, or medical sample preparation',
                'reasoning': 'White color indicates medical sterilization, metal material ensures sharpness and durability, and grooved edge texture forms the cutting edge',
                'confidence': 'high'
            })
        elif material in ['ABS', 'PLA'] and temperature == 'normal':
            object_hypotheses.append({
                'name': 'medical device housing or pharmaceutical dispenser',
                'function': 'for protecting electronic medical equipment or controlled medication distribution',
                'reasoning': 'White color meets medical cleanliness standards, ABS/PLA materials are chemical-resistant and moldable for complex shapes',
                'confidence': 'medium'
            })
    
    # BLACK objects - professional/technical
    elif color == 'black':
        if material == 'Metal' and texture == 'D4' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'precision machining tool or automotive wrench',
                'function': 'for high-tolerance mechanical work, engine repair, or industrial assembly operations',
                'reasoning': 'Black color reduces glare and shows professionalism, metal provides strength and precision, grooved edge texture creates the functional working edge, and normal temperature indicates ready-to-use condition',
                'confidence': 'high'
            })
        elif material == 'Rubber' and texture == 'D7':
            object_hypotheses.append({
                'name': 'industrial safety mat or anti-vibration pad',
                'function': 'for worker protection on factory floors, machinery vibration dampening, or electrical insulation',
                'reasoning': 'Black color hides industrial dirt and provides UV resistance, rubber material absorbs shock and vibration, and crescent-patterned texture distributes weight and provides grip',
                'confidence': 'high'
            })
        elif material in ['ABS', 'PLA'] and texture == 'D2':
            object_hypotheses.append({
                'name': 'electronic device enclosure or computer component housing',
                'function': 'for protecting circuit boards, providing electromagnetic shielding, or housing control systems',
                'reasoning': 'Black color provides professional appearance and heat dissipation, ABS/PLA materials offer electrical insulation, and smooth surface texture allows precise manufacturing tolerances',
                'confidence': 'high'
            })
        elif material == 'Nylon' and texture == 'D7':
            object_hypotheses.append({
                'name': 'industrial cable management strip or machinery belt',
                'function': 'for organizing electrical wiring systems or transmitting rotational power in manufacturing',
                'reasoning': 'Black color provides industrial durability and UV resistance, nylon material offers flexibility and strength, and crescent-patterned texture provides grip and prevents slipping',
                'confidence': 'high'
            })
    
    # BLUE objects - utility/water-related
    elif color == 'blue':
        if material == 'PET' and temperature == 'cold':
            object_hypotheses.append({
                'name': 'filtered water bottle or hydration container',
                'function': 'for storing purified drinking water, sports hydration, or outdoor activity fluid replacement',
                'reasoning': 'Blue color psychologically associates with clean water and trust, PET material is food-safe and lightweight, and cold temperature indicates chilled beverage storage',
                'confidence': 'high'
            })
        elif material == 'Cloth' and texture == 'D2':
            object_hypotheses.append({
                'name': 'industrial work uniform or mechanic coveralls',
                'function': 'for protecting workers from oil stains, chemical spills, or industrial debris during maintenance',
                'reasoning': 'Blue color is standard for industrial workwear and hides stains well, cloth material provides comfort and breathability, and smooth weave texture indicates durable construction',
                'confidence': 'high'
            })
        elif material == 'Acrylic' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'laboratory beaker or chemical mixing vessel',
                'function': 'for precise liquid measurement, chemical reactions, or solution preparation in research',
                'reasoning': 'Blue color helps with liquid level visibility, acrylic material provides chemical resistance and clarity, and normal temperature indicates standard lab conditions',
                'confidence': 'medium'
            })
    
    # GREEN objects - environmental/outdoor
    elif color == 'green':
        if material == 'PET' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'recycled beverage bottle or eco-friendly container',
                'function': 'for sustainable liquid storage, environmental waste reduction, or green packaging solutions',
                'reasoning': 'Green color symbolizes environmental friendliness and recycling, PET material is highly recyclable, and normal temperature indicates standard storage conditions',
                'confidence': 'high'
            })
        elif material in ['ABS', 'PLA'] and texture == 'D1':
            object_hypotheses.append({
                'name': 'outdoor camping gear component or hiking equipment part',
                'function': 'for wilderness survival, portable shelter assembly, or outdoor recreation activities',
                'reasoning': 'Green color provides natural camouflage in outdoor settings, ABS/PLA materials are lightweight and durable, and dimpled surface texture provides grip for outdoor handling',
                'confidence': 'medium'
            })
        elif material == 'Rubber' and texture == 'D7':
            object_hypotheses.append({
                'name': 'garden tool grip or outdoor equipment handle',
                'function': 'for landscaping work, plant cultivation, or outdoor maintenance activities with secure handling',
                'reasoning': 'Green color blends with garden environment, rubber material provides comfortable grip and weather resistance, and crescent-patterned texture prevents slipping during use',
                'confidence': 'medium'
            })
    
    # YELLOW objects - warning/construction
    elif color == 'yellow':
        if material == 'Metal' and texture == 'D4':
            object_hypotheses.append({
                'name': 'construction utility knife or safety cutting tool',
                'function': 'for building material cutting, safety rope severing, or emergency rescue operations',
                'reasoning': 'Yellow color provides high visibility for safety compliance, metal material ensures cutting effectiveness, and grooved edge texture forms the sharp cutting edge',
                'confidence': 'high'
            })
        elif material in ['ABS', 'PLA'] and texture == 'D7':
            object_hypotheses.append({
                'name': 'safety warning marker or construction barrier component',
                'function': 'for hazard identification, traffic control, or construction zone safety demarcation',
                'reasoning': 'Yellow color maximizes visibility for safety warnings, ABS/PLA materials provide weather resistance, and crescent-patterned texture may help with stacking or interlocking',
                'confidence': 'high'
            })
        elif material == 'Rubber' and texture == 'D1':
            object_hypotheses.append({
                'name': 'safety training ball or visibility sports equipment',
                'function': 'for emergency response training, high-visibility sports activities, or safety education programs',
                'reasoning': 'Yellow color ensures high visibility during training, rubber material provides safe impact characteristics, and dimpled surface texture improves grip and handling',
                'confidence': 'medium'
            })
    
    # Temperature-specific detailed reasoning
    if temperature == 'hot':
        if material == 'Metal' and texture == 'D4':
            object_hypotheses.append({
                'name': 'heated chef knife or industrial cutting blade',
                'function': 'for cutting through hard materials like frozen foods, plastics, or heated manufacturing processes',
                'reasoning': 'Hot temperature indicates active heating for enhanced cutting, metal material conducts heat effectively, and grooved edge texture provides the cutting edge geometry',
                'confidence': 'high'
            })
        elif material == 'Wood' and texture == 'D4':
            object_hypotheses.append({
                'name': 'heated wooden cooking utensil or craft tool',
                'function': 'for stirring hot sauces, wood burning art, or heated food preparation without heat transfer',
                'reasoning': 'Hot temperature shows recent contact with heat source, wood material insulates handle from heat transfer, and grooved edge provides functional edge or grip',
                'confidence': 'high'
            })
    elif temperature == 'cold':
        if material == 'Metal' and texture == 'D2':
            object_hypotheses.append({
                'name': 'refrigerated surgical instrument or precision cold tool',
                'function': 'for cryogenic procedures, cold-sensitive material handling, or temperature-controlled manufacturing',
                'reasoning': 'Cold temperature indicates refrigerated storage for precision work, metal material maintains temperature effectively, and smooth surface texture allows precise manipulation',
                'confidence': 'high'
            })
    
    # Texture-specific detailed reasoning
    if texture == 'D1':  # Dimpled surface
        if material == 'Rubber' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'massage therapy ball or physical rehabilitation sphere',
                'function': 'for muscle tension relief, trigger point therapy, or physical therapy rehabilitation exercises',
                'reasoning': 'Dimpled surface texture provides therapeutic pressure points, rubber material offers appropriate firmness and safety, and normal temperature ensures comfortable therapeutic use',
                'confidence': 'high'
            })
        elif material == 'Wood':
            object_hypotheses.append({
                'name': 'wooden massage tool or acupressure sphere',
                'function': 'for traditional massage therapy, reflexology treatment, or holistic healing practices',
                'reasoning': 'Dimpled surface texture creates acupressure points, wood material provides natural therapeutic properties and appropriate hardness for pressure point therapy',
                'confidence': 'medium'
            })
    
    elif texture == 'D4':  # Grooved edge
        if material == 'Wood' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'wooden cutting board edge or kitchen prep tool',
                'function': 'for food preparation, ingredient chopping, or culinary presentation with guided cutting',
                'reasoning': 'Grooved edge texture provides cutting guide or edge, wood material is food-safe and knife-friendly, and normal temperature indicates ready-to-use kitchen condition',
                'confidence': 'high'
            })
        elif material == 'Nylon' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'industrial cable guide or machinery track component',
                'function': 'for directing moving parts, cable management, or precision mechanical guidance systems',
                'reasoning': 'Grooved edge texture creates guidance channel, nylon material provides low friction and durability, and normal temperature indicates standard operating conditions',
                'confidence': 'high'
            })
    
    elif texture == 'D7':  # Crescent-patterned surface
        if material == 'Rubber' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'anti-slip shoe sole or safety flooring',
                'function': 'for preventing workplace accidents, enhanced walking stability, or specialized footwear traction',
                'reasoning': 'Crescent-patterned texture maximizes surface contact for traction, rubber material provides grip and flexibility, and normal temperature indicates standard use conditions',
                'confidence': 'high'
            })
        elif material == 'Metal':
            object_hypotheses.append({
                'name': 'industrial grip plate or machinery safety surface',
                'function': 'for worker safety on platforms, enhanced grip on tools, or anti-slip industrial applications',
                'reasoning': 'Crescent-patterned texture provides mechanical grip texture, metal material offers durability in harsh industrial environments and load-bearing capacity',
                'confidence': 'high'
            })
    
    # Material-specific detailed applications
    if material == 'Cloth':
        if temperature == 'hot':
            object_hypotheses.append({
                'name': 'heated therapeutic compress or warming pad cover',
                'function': 'for pain relief therapy, muscle relaxation, or medical heat treatment applications',
                'reasoning': 'Hot temperature indicates therapeutic heating, cloth material provides safe skin contact and heat distribution for medical applications',
                'confidence': 'medium'
            })
        elif texture == 'D5':
            object_hypotheses.append({
                'name': 'microfiber cleaning cloth or precision wiping material',
                'function': 'for delicate surface cleaning, optical lens care, or dust-free maintenance procedures',
                'reasoning': 'Fine textured surface provides gentle cleaning action, cloth material offers absorbency and surface safety for delicate cleaning tasks',
                'confidence': 'medium'
            })
        elif color == 'white' and temperature == 'cold':
            object_hypotheses.append({
                'name': 'sterile medical drape or surgical covering',
                'function': 'for maintaining sterile fields during medical procedures or protecting surfaces from contamination',
                'reasoning': 'White color indicates medical sterility, cloth material provides flexible coverage, and cold temperature suggests sterile storage conditions',
                'confidence': 'high'
            })
        elif color == 'blue' and texture == 'D1':
            object_hypotheses.append({
                'name': 'workout towel or gym equipment cover',
                'function': 'for moisture absorption during exercise, equipment protection, or athletic facility hygiene maintenance',
                'reasoning': 'Blue color is common in athletic settings, cloth material provides absorbency, and dimpled texture enhances moisture-wicking properties',
                'confidence': 'medium'
            })
    
    elif material == 'Resin':
        if temperature == 'normal' and texture == 'D2':
            object_hypotheses.append({
                'name': 'decorative art piece or custom jewelry component',
                'function': 'for artistic display, personalized accessories, or handcrafted decorative applications',
                'reasoning': 'Smooth surface texture allows fine detail in casting, resin material enables complex shapes and transparent effects, and normal temperature indicates completed curing process',
                'confidence': 'medium'
            })
        elif color == 'yellow' and texture == 'D4':
            object_hypotheses.append({
                'name': 'safety marker or warning component',
                'function': 'for hazard identification, construction safety marking, or emergency equipment visibility enhancement',
                'reasoning': 'Yellow color provides high visibility for safety, resin material offers weather resistance, and grooved texture may aid in mounting or gripping',
                'confidence': 'medium'
            })
        elif temperature == 'hot':
            object_hypotheses.append({
                'name': 'heated craft tool or molding implement',
                'function': 'for shaping materials, craft applications, or heated forming processes requiring precise temperature control',
                'reasoning': 'Hot temperature indicates active heating for material work, resin material maintains shape under heat stress for precision tools',
                'confidence': 'medium'
            })
    
    elif material == 'Acrylic':
        if color == 'green' and texture == 'D2':
            object_hypotheses.append({
                'name': 'greenhouse panel or plant protection shield',
                'function': 'for plant cultivation, weather protection, or controlled growing environment maintenance',
                'reasoning': 'Green color blends with plant environments, acrylic material provides transparency and weather resistance, and smooth surface allows easy cleaning',
                'confidence': 'high'
            })
        elif temperature == 'hot' and texture == 'D4':
            object_hypotheses.append({
                'name': 'heated display case edge or warming panel',
                'function': 'for temperature-controlled displays, food warming applications, or climate-controlled exhibition cases',
                'reasoning': 'Hot temperature indicates active heating, acrylic provides transparency and heat resistance, and grooved edge allows secure mounting',
                'confidence': 'medium'
            })
        elif color == 'red' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'emergency equipment cover or safety display panel',
                'function': 'for protecting emergency tools, displaying safety information, or providing clear access to critical equipment',
                'reasoning': 'Red color signals emergency applications, acrylic material provides protection while maintaining visibility of contents',
                'confidence': 'high'
            })
    
    elif material == 'Nylon':
        if texture == 'D1' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'sports equipment grip or athletic gear component',
                'function': 'for enhancing grip on sporting goods, providing comfort during athletic activities, or improving performance equipment handling',
                'reasoning': 'Dimpled texture enhances grip performance, nylon material provides durability and flexibility for athletic applications',
                'confidence': 'high'
            })
        elif color == 'white' and texture == 'D5':
            object_hypotheses.append({
                'name': 'precision filter material or clean room component',
                'function': 'for air filtration, particle removal, or maintaining sterile environments in laboratory settings',
                'reasoning': 'White color indicates cleanliness standards, nylon material provides filtration properties, and fine texture creates effective barrier',
                'confidence': 'medium'
            })
        elif temperature == 'cold' and texture == 'D7':
            object_hypotheses.append({
                'name': 'cold storage packaging or refrigeration component',
                'function': 'for maintaining low temperatures, protecting frozen goods, or providing insulation in cooling systems',
                'reasoning': 'Cold temperature indicates refrigeration use, nylon material provides flexibility at low temperatures, and textured surface aids in handling',
                'confidence': 'medium'
            })
    
    elif material == 'Wood':
        if color == 'red' and texture == 'D2':
            object_hypotheses.append({
                'name': 'decorative cutting board or ceremonial serving tray',
                'function': 'for food presentation, special occasion serving, or decorative kitchen display with food-safe properties',
                'reasoning': 'Red wood suggests decorative staining, smooth surface is food-safe, and wood material provides natural antimicrobial properties',
                'confidence': 'high'
            })
        elif temperature == 'cold' and texture == 'D1':
            object_hypotheses.append({
                'name': 'massage therapy tool or reflexology instrument',
                'function': 'for therapeutic pressure point treatment, muscle therapy, or traditional healing practices requiring cool application',
                'reasoning': 'Cold temperature provides therapeutic cooling effect, wood material offers appropriate firmness, and dimpled texture creates pressure points',
                'confidence': 'medium'
            })
        elif color == 'green' and texture == 'D7':
            object_hypotheses.append({
                'name': 'garden tool handle or outdoor equipment component',
                'function': 'for landscaping work, plant care, or outdoor maintenance requiring comfortable and secure grip',
                'reasoning': 'Green color blends with garden environment, wood material provides natural grip comfort, and textured surface prevents slipping',
                'confidence': 'high'
            })
    
    # Additional specific temperature-texture combinations
    if temperature == 'hot':
        if texture == 'D1' and material in ['Rubber', 'Wood']:
            object_hypotheses.append({
                'name': 'heated massage stone or therapeutic tool',
                'function': 'for hot stone therapy, muscle relaxation, or spa treatment applications requiring controlled heat application',
                'reasoning': 'Hot temperature provides therapeutic heating, dimpled texture creates pressure points for massage, and material ensures safe heat retention',
                'confidence': 'high'
            })
        elif texture == 'D2' and material == 'Acrylic':
            object_hypotheses.append({
                'name': 'heated display surface or warming plate',
                'function': 'for food warming, display heating, or temperature-controlled presentation requiring transparent heat distribution',
                'reasoning': 'Hot temperature indicates active heating function, smooth surface allows easy cleaning, and acrylic provides heat-resistant transparency',
                'confidence': 'medium'
            })
    
    elif temperature == 'cold':
        if texture == 'D5' and material in ['Metal', 'Acrylic']:
            object_hypotheses.append({
                'name': 'precision cooling tool or laboratory instrument',
                'function': 'for temperature-sensitive procedures, precision cooling applications, or scientific measurement requiring stable cold conditions',
                'reasoning': 'Cold temperature provides controlled cooling, fine texture allows precise manipulation, and material ensures temperature stability',
                'confidence': 'high'
            })
        elif texture == 'D7' and material == 'Rubber':
            object_hypotheses.append({
                'name': 'cold therapy pad or cryogenic application tool',
                'function': 'for injury treatment, inflammation reduction, or medical cold therapy requiring flexible cold application',
                'reasoning': 'Cold temperature provides therapeutic cooling, textured surface enhances contact, and rubber material remains flexible when cold',
                'confidence': 'high'
            })
    
    # Additional texture-specific combinations
    if texture == 'D5':  # Fine textured
        if material == 'Metal' and color == 'black':
            object_hypotheses.append({
                'name': 'precision electronic component or semiconductor device',
                'function': 'for electronic circuits, computer components, or high-tech applications requiring precise surface characteristics',
                'reasoning': 'Fine texture provides precise surface finish, black color aids heat dissipation, and metal material ensures electrical conductivity',
                'confidence': 'high'
            })
        elif material == 'PET' and temperature == 'normal':
            object_hypotheses.append({
                'name': 'specialty container or precision storage vessel',
                'function': 'for sensitive material storage, laboratory sample containment, or applications requiring controlled surface properties',
                'reasoning': 'Fine texture provides controlled surface characteristics, PET material ensures chemical resistance, and normal temperature indicates standard storage',
                'confidence': 'medium'
            })
    
    # Edge cases and unusual combinations
    if material == 'ABS' or material == 'PLA':
        if color == 'white' and texture == 'D5' and temperature == 'cold':
            object_hypotheses.append({
                'name': '3D printed medical device or laboratory tool',
                'function': 'for specialized medical applications, custom laboratory equipment, or precision scientific instruments requiring sterile cold storage',
                'reasoning': 'White color meets medical standards, fine texture allows precise 3D printing detail, plastic material enables custom shapes, and cold temperature indicates sterile storage',
                'confidence': 'high'
            })
        elif color == 'black' and temperature == 'hot':
            object_hypotheses.append({
                'name': 'heated 3D printer component or thermal processing tool',
                'function': 'for additive manufacturing, thermal processing, or heated fabrication requiring temperature-controlled plastic components',
                'reasoning': 'Black color aids heat absorption and dissipation, hot temperature indicates active thermal processing, and plastic material suitable for heated applications',
                'confidence': 'medium'
            })
    
    # Multi-property specific cases
    if color == 'yellow' and material == 'Rubber' and temperature == 'cold':
        object_hypotheses.append({
            'name': 'safety equipment for cold environments or arctic gear component',
            'function': 'for cold weather safety, arctic equipment identification, or low-temperature emergency applications requiring high visibility',
            'reasoning': 'Yellow color ensures visibility in harsh conditions, rubber material remains flexible in cold, and cold temperature indicates arctic/winter use conditions',
            'confidence': 'high'
        })
    
    if color == 'blue' and material == 'Metal' and texture == 'D5':
        object_hypotheses.append({
            'name': 'precision water system component or hydraulic instrument',
            'function': 'for water management systems, hydraulic control, or fluid handling requiring precise surface characteristics and reliability',
            'reasoning': 'Blue color associates with water systems, metal material provides durability and pressure resistance, and fine texture ensures precise sealing and operation',
            'confidence': 'high'
        })
    
    if color == 'green' and temperature == 'hot' and material in ['Wood', 'Rubber']:
        object_hypotheses.append({
            'name': 'heated garden tool or greenhouse equipment',
            'function': 'for plant cultivation, heated greenhouse applications, or agricultural equipment requiring controlled temperature for optimal plant growth',
            'reasoning': 'Green color blends with plant environment, hot temperature provides growing heat, and material ensures safe handling during heated agricultural work',
            'confidence': 'medium'
        })
    
    # Additional rare but important combinations
    if material == 'PET':
        if color == 'white' and texture == 'D7' and temperature == 'hot':
            object_hypotheses.append({
                'name': 'heated food packaging or thermal processing container',
                'function': 'for hot food storage, thermal food processing, or heated packaging applications requiring food-safe materials',
                'reasoning': 'White color meets food safety visibility standards, PET material is food-safe at controlled temperatures, textured surface aids grip handling, and hot temperature indicates thermal processing use',
                'confidence': 'high'
            })
        elif color == 'black' and temperature == 'cold':
            object_hypotheses.append({
                'name': 'UV-protected storage container or light-sensitive material holder',
                'function': 'for protecting light-sensitive contents, UV filtration, or cold storage of materials requiring darkness',
                'reasoning': 'Black color provides UV protection and light blocking, PET material offers chemical resistance, and cold temperature indicates preservation storage',
                'confidence': 'medium'
            })
    
    # Uncommon texture combinations
    if texture == 'D1' and texture == 'D7':  # This shouldn't happen but adding fallback
        object_hypotheses.append({
            'name': 'complex textured specialized tool or custom equipment',
            'function': 'for specialized applications requiring multiple texture characteristics or custom manufacturing solutions',
            'reasoning': 'Multiple texture patterns suggest specialized custom manufacturing for specific functional requirements',
            'confidence': 'low'
        })
    
    # Material combinations that might be rare
    if material in ['Resin', 'Acrylic'] and color == 'black' and texture == 'D1':
        object_hypotheses.append({
            'name': 'optical component or precision instrument part',
            'function': 'for light control, optical applications, or precision equipment requiring specific surface characteristics',
            'reasoning': 'Black color provides light absorption, transparent materials enable optical properties, and textured surface creates controlled light interaction',
            'confidence': 'medium'
        })
    
    # Temperature edge cases
    if temperature == 'hot' and material == 'Cloth' and texture == 'D7':
        object_hypotheses.append({
            'name': 'heated protective clothing or thermal safety gear',
            'function': 'for worker protection in high-temperature environments, heated safety applications, or thermal protective equipment',
            'reasoning': 'Hot temperature indicates thermal protection needs, cloth material provides comfort and flexibility, and textured surface enhances protective characteristics',
            'confidence': 'medium'
        })
    
    # Default fallbacks for unusual combinations
    if not object_hypotheses:
        # Try broader material-based reasoning
        if material == 'Metal':
            object_hypotheses.append({
                'name': 'metal tool or mechanical component',
                'function': 'for mechanical applications, structural support, or industrial use requiring metal durability and strength',
                'reasoning': 'Metal material suggests mechanical or structural applications requiring durability, though specific function requires more detailed analysis',
                'confidence': 'low'
            })
        elif material in ['Rubber', 'Nylon']:
            object_hypotheses.append({
                'name': 'flexible component or safety equipment',
                'function': 'for applications requiring flexibility, shock absorption, or protective characteristics',
                'reasoning': 'Flexible materials suggest safety, comfort, or protective applications, though specific identification requires additional context',
                'confidence': 'low'
            })
        elif material in ['ABS', 'PLA', 'Acrylic', 'Resin']:
            object_hypotheses.append({
                'name': 'manufactured component or custom device',
                'function': 'for specialized applications, custom manufacturing, or precision molded parts requiring specific material properties',
                'reasoning': 'Synthetic materials suggest manufactured applications with specific engineering requirements, though exact purpose needs more analysis',
                'confidence': 'low'
            })
        elif material in ['Cloth', 'Wood']:
            object_hypotheses.append({
                'name': 'natural material object or traditional tool',
                'function': 'for applications utilizing natural material properties, traditional craftsmanship, or sustainable solutions',
                'reasoning': 'Natural materials suggest traditional applications or sustainable solutions, though specific function requires additional property analysis',
                'confidence': 'low'
            })
        elif material == 'PET':
            object_hypotheses.append({
                'name': 'container or packaging component',
                'function': 'for storage, transportation, or containment applications requiring chemical resistance and transparency',
                'reasoning': 'PET material commonly used for containment applications, though specific use requires analysis of other properties',
                'confidence': 'low'
            })
        else:
            # Ultimate fallback
            object_hypotheses.append({
                'name': 'unknown specialized object',
                'function': 'for specialized applications that require unique combinations of tactile properties',
                'reasoning': 'The combination of tactile properties suggests a specialized or custom application, but specific identification requires additional context or information',
                'confidence': 'very low'
            })
    
    # Additional confidence boosters for strong combinations
    for hypothesis in object_hypotheses:
        # Boost confidence for combinations with multiple matching properties
        matching_properties = 0
        if color in ['red', 'white', 'black', 'blue', 'green', 'yellow']:
            matching_properties += 1
        if temperature in ['hot', 'cold']:
            matching_properties += 1  
        if texture in ['D1', 'D2', 'D4', 'D5', 'D7']:
            matching_properties += 1
        if material in ['ABS', 'Acrylic', 'Cloth', 'Metal', 'Nylon', 'PET', 'PLA', 'Resin', 'Rubber', 'Wood']:
            matching_properties += 1
        
        # Boost confidence for highly specific combinations
        if matching_properties >= 3 and hypothesis['confidence'] == 'medium':
            hypothesis['confidence'] = 'high'
        elif matching_properties >= 4 and hypothesis['confidence'] == 'low':
            hypothesis['confidence'] = 'medium'
    
    # Select best hypothesis with detailed reasoning
    if object_hypotheses:
        # Prefer high confidence hypotheses, then most specific ones
        best_hypothesis = max(object_hypotheses, key=lambda x: 
                            (({'high': 3, 'medium': 2, 'low': 1}[x['confidence']]), len(x['function'])))
        
        # Start with the reasoning process (Chain of Thought)
        reasoning += f"Let me analyze each tactile property: {best_hypothesis['reasoning']}. "
        
        # Add detailed color context in the reasoning chain
        if color in ['red', 'white', 'black', 'blue', 'green', 'yellow'] and color != 'unknown':
            reasoning += f"The {color} color specifically indicates "
            if color == 'red':
                reasoning += "either emergency/safety applications requiring immediate attention, or sports/recreational equipment designed for visibility. "
            elif color == 'white':
                reasoning += "medical/sterile applications where contamination detection is critical, or clean environments requiring hygiene standards. "
            elif color == 'black':
                reasoning += "professional/industrial applications where durability and heat absorption are important, or technical equipment requiring non-reflective surfaces. "
            elif color == 'blue':
                reasoning += "utility applications often related to water systems, or professional environments requiring trust and reliability. "
            elif color == 'green':
                reasoning += "environmental applications emphasizing sustainability, or outdoor equipment designed for natural settings. "
            elif color == 'yellow':
                reasoning += "safety applications requiring high visibility, or construction environments where hazard awareness is critical. "
        
        # Add confidence level in reasoning
        if best_hypothesis['confidence'] == 'high':
            reasoning += "The combination of tactile properties strongly matches a specific object type, giving me high confidence. "
        elif best_hypothesis['confidence'] == 'medium':
            reasoning += "The tactile properties provide good indicators, though they could potentially match a few similar object types. "
        else:
            reasoning += "The tactile properties suggest a likely identification, though additional information would help distinguish between similar categories. "
        
        # Now present the conclusion
        reasoning += f"Based on this analysis, I believe this is most likely a {best_hypothesis['name']}. "
        reasoning += f"Its specific function would be {best_hypothesis['function']}."
        
    else:
        reasoning += "After analyzing the tactile properties, they suggest a functional object, but the specific combination doesn't match common object patterns in my knowledge base, making it difficult to draw a definitive conclusion about its identity or function."
    
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
                if rand_ < 0.4:
                    for key in samples.keys():
                        sample1[key] = random.sample(samples[key].keys(), k=1)[0]
                        tactile1[key] = [random.choice(samples[key][sample1[key]])]
                        rand = random.random()
                        if rand < 0.5:
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