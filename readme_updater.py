import os
import re

# Path to the root README.md
ROOT_README = 'README.md'

headers = []

def update_root_readme():
    # Store collected content
    collected_content = []

    # Traverse the subdirectories
    for item in os.listdir('.'):
        if os.path.isdir(item):
            sub_dir = item
            sub_readme_path = os.path.join(sub_dir, 'README.md')

            # Debug: Print the directory being checked
            # print(f"Checking: {sub_dir}")

            # Check if README.md exists in this subdirectory
            if os.path.exists(sub_readme_path):
                print(f"Found README.md in: {sub_readme_path}")

                # Read the content of the subdirectory's README.md
                with open(sub_readme_path, 'r', encoding='utf-8') as file:
                    content = file.read().strip()

                header = re.findall(r"^# (.*)", content)[0]
                # print(header)
                headers.append(header)

                # Adjust header levels using a single line regex replacement
                content = re.sub(r"(^#)", r"##", content, flags=re.MULTILINE)
                content = content.replace(f"## {header}", f"## {header}\n\n[WARN] This section is generated, to modify, please go to the {sub_readme_path}")

                # Collect the adjusted content
                print(f"Collecting and adjusting content from {sub_readme_path}...")
                collected_content.append(content + "\n")

    # Read the existing root-level README.md (if it exists)
    if os.path.exists(ROOT_README):
        print(f"Reading existing root-level README.md...")
        with open(ROOT_README, 'r', encoding='utf-8') as file:
            root_content = file.read()
        for header in headers:
            root_content = root_content.split(f"## {header}")[0]

    # Prepare the new content
    new_content = root_content + "\n".join(collected_content)

    # Write the updated content to the root README.md
    with open(ROOT_README, 'w', encoding='utf-8') as file:
        file.write(new_content)

    print("Root README.md updated successfully.")

if __name__ == "__main__":
    update_root_readme()
