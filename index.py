import pandas as pd
import slugify
from sqlalchemy import create_engine
from datetime import datetime
import json
import base64
from tabulate import tabulate
import os

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
    
    photo_path = message.get('photo', None)
    
    # Skip if 'photo' is None or the file doesn't exist
    if photo_path is None or not os.path.exists(photo_path):
        print(f"Skipping element with no valid 'photo' file: {message}")
        continue

    date_str = message.get('date', None)
    created_at = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

    title = message.get('text', None)
    if isinstance(title, list):
        title = ''.join([str(elem) if isinstance(elem, (str, int)) else json.dumps(elem) for elem in title])

    # Truncate title to fit within the allowed length (191 characters)
    title = title[:191]
    price = 100000
    discount = 100000 % 5
    base_slug = slugify.slugify(title, max_length=50, word_boundary=True)
    
    # Append a counter to make the slug unique
    counter = 1
    slug = base_slug
    while slug in [item['slug'] for item in result_list]:
        slug = f"{base_slug}-{counter}"
        counter += 1

    # Read image binary data
    with open(photo_path, 'rb') as photo_file:
        photo_binary_data = base64.b64encode(photo_file.read()).decode('utf-8')

    result_list.append({
        'id': message.get('id', None),
        'title': title,
        'slug': slug,
        'price': price,
        'discount': discount,
        'photo': photo_binary_data,  # Store binary image data
        'cat_id': 1,
        'brand_id': 1,
        'child_cat_id': 1,
        'is_featured': False,
        'status': 'inactive',
        'condition': 'default',
        'size': 'M',
        'stock': 1,
        'created_at': created_at,
        'updated_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    })


# Creating a new DataFrame with the extracted data
result_df = pd.DataFrame(result_list)

# Displaying the DataFrame using tabulate
print(tabulate(result_df[['id', 'title', 'slug', 'price', 'discount', 'cat_id', 'brand_id', 'photo', 'created_at', 'updated_at']], headers='keys', tablefmt='pretty', showindex=False))

# SQLAlchemy engine to connect to PostgreSQL
engine = create_engine('postgresql://postgres:1111@localhost:5432/test')

# Storing the DataFrame to PostgreSQL
try:
    # Storing the DataFrame to PostgreSQL
    result_df.to_sql('products', con=engine, if_exists='append', index=False)
    print("Data inserted successfully.")
except Exception as e:
    print(f"Error inserting data: {e}")
