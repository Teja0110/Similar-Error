# import json to read a json file
import json

# Read json file and Create a list of plain_text and markup
# input : json file input
def process_data(input):
    new_dict = []
    # Read json file to a dictionary
    with open(input) as json_file:
        data = json.load(json_file)
    
    # Add only plaintext and markup to the result
    for text in data:
        tmp_text = text['plaintext']
        markup = text['grades'][1]['markup']
        new_dict.append({'plaintext' : tmp_text, 'markup' : markup})
    
    # Return result
    return new_dict


