import pandas as pd
import json
from tabulate import tabulate

# Assuming 'result.json' contains the JSON data
with open('result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Assuming the messages are nested under a key (e.g., 'messages')
messages = data.get('messages', [])

# Extracting desired fields
result_list = []
for message in messages:
    # Skip if the element is not a dictionary
    if not isinstance(message, dict):
        print(f"Skipping non-dictionary element: {message}")
        continue
    
    photo = message.get('photo', None)
    
    # Skip if 'photo' is None
    if photo is None:
        print(f"Skipping element with no 'photo': {message}")
        continue
    
    result_list.append({
        'id': message.get('id', None),
        'photo': photo,
        'text': message.get('text', None),
        'date': message.get('date', None)
    })

# Creating a new DataFrame with the extracted data
result_df = pd.DataFrame(result_list)

# Displaying the DataFrame using tabulate
print(tabulate(result_df, headers='keys', tablefmt='pretty', showindex=False))

# Saving the DataFrame to a new JSON file
result_df.to_json('result_output.json', orient='records', lines=True)
