import ijson

def explore_json_structure(file_path):
    with open(file_path, 'rb') as file:
        objects = ijson.items(file, '')  # Empty prefix to get top-level objects
        for i, obj in enumerate(objects):
            print(obj)
            if i >= 10:  # Limit to first 10 items
                break

# Replace 'your_file.json' with the path to your JSON file
explore_json_structure(r'C:\loganalyzer\1.json')
