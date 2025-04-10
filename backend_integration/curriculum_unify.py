import json

def unify_course_format(data):
    def process_entry(entry):
        # If entry is a dictionary, extract the course code
        if isinstance(entry, dict):
            return list(entry.keys())[0]
        return entry

    for category, course_groups in data.items():
        for i, group in enumerate(course_groups):
            data[category][i] = [process_entry(course) for course in group]

    return data

# Load the JSON file
with open("backend_integration\major_curriculum.json", "r", encoding="utf-8") as f:
    curriculum_data = json.load(f)

# Unify the course format
unified_data = unify_course_format(curriculum_data)

# Save the modified JSON back to a file
with open("backend_integration\major_curriculum_unified.json", "w", encoding="utf-8") as f:
    json.dump(unified_data, f, indent=4)
