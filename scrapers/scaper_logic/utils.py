import os
import json
from datetime import datetime

def write_json(tips, filename):


    # Get timestamp yyyymmddhhmmss
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")



    current_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    file_path = os.path.join(current_directory, f'{filename}_{timestamp}.json')
    with open(file_path, 'w') as outfile:
        json.dump(tips, outfile, indent=4)