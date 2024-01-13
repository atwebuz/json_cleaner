import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import json

import tabulate

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

    date_str = message.get('date', None)
    created_at = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

    result_list.append({
        'id': message.get('id', None),
        'title': message.get('text', None),  # Change 'text' to 'title'
        'photo': photo,
        'cat_id': 1,
        'brand_id': 1,
        'created_at': created_at,  # Use the converted datetime string
        'updated_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # Set 'updated_at' to the current UTC time
    })

# Creating a new DataFrame with the extracted data
result_df = pd.DataFrame(result_list)

# Displaying the DataFrame using tabulate
print(tabulate.tabulate(result_df, headers='keys', tablefmt='pretty', showindex=False))

# SQLAlchemy engine to connect to PostgreSQL
engine = create_engine('postgresql://postgres:1111@localhost:5432/adminLte_logistic')

# Storing the DataFrame to PostgreSQL
try:
    # Storing the DataFrame to PostgreSQL
    result_df.to_sql('products', con=engine, if_exists='replace', index=False)
    print("Data inserted successfully.")
except Exception as e:
    print(f"Error inserting data: {e}")
