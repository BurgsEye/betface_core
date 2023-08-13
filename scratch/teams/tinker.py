import json

# Step 1: Read from 'teams.json'
with open('teams.json', 'r') as f:
    data = json.load(f)

# Step 2: Process the data
for item in data:
    item.pop('id', None)
    item.pop('short_name', None)
    item['sport'] = 1

# Step 3: Write the processed data to 'team_cleaned.json'
with open('team_cleaned.json', 'w') as f:
    json.dump(data, f, indent=4)  # 'indent=4' for pretty printing
