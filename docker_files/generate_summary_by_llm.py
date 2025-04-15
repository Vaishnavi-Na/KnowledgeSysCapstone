import json
import requests
import os
import concurrent.futures

def build_prompt(comments, last_name):
    """Build the prompt for the LLM from the professor's comments."""
    prompt = f"Provide a concise overview of Professor {last_name} based on student comments. Use definitive language, be direct, and limit to 3-4 sentences maximum. Focus on overall teaching quality, not individual student experiences:\n\n"
    for comment in comments[:8]:
        prompt += f"- {comment}\n"
    return prompt

def call_llm_api(prompt):
    """Call the local LLM API with the given prompt and return the summary."""
    url = "http://localhost:8008/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "Qwen/Qwen2.5-32B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
        "temperature": 0.5,
        "stop": ["\n\n"]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        summary = response.json()["choices"][0]["message"]["content"].strip()
        return summary
    except Exception as e:
        print(f"Error in API call: {e}")
        try:
            print("Response content:", response.text)
        except Exception:
            pass
        return "Error generating summary"

def get_llm_summary(comments, last_name):
    """Generate the summary given a list of comments."""
    prompt = build_prompt(comments, last_name)
    return call_llm_api(prompt)

def update_professor(professor, summary):
    if "summary_comment" in professor:
        del professor["summary_comment"]
    new_prof = {}
    summary_inserted = False
    for key in professor:
        new_prof[key] = professor[key]
        if key == "numRatings":
            new_prof["summary_comment"] = summary
            summary_inserted = True
    if not summary_inserted:
        new_prof["summary_comment"] = summary
    professor.clear()
    professor.update(new_prof)

def process_json_file(input_path):
    print(f"Processing file: {input_path}")
    with open(input_path, 'r') as f:
        professors = json.load(f)
    
    # Collect tasks for professors with available comments.
    tasks = []
    for index, professor in enumerate(professors):
        comments = []
        last_name = professor.get("lastName", "Unknown")
        if "Ratings" in professor:
            comments = [rating["comment"] for rating in professor["Ratings"]
                        if "comment" in rating and rating["comment"]]
        if comments:
            tasks.append((index, comments, last_name))
        else:
            update_professor(professor, "No comments available")
    
    # Run requests concurrently, mapping each request to its professor index.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_index = {executor.submit(get_llm_summary, comments, last_name): index 
                          for index, comments, last_name in tasks}
        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            summary = future.result()
            update_professor(professors[index], summary)
    
    with open(input_path, 'w') as f:
        json.dump(professors, f, indent=2)

def main():
    json_dir = "profs_sort_by_department"
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    
    print(f"Found {len(json_files)} JSON files to process.")
    
    for json_file in json_files:
        json_path = os.path.join(json_dir, json_file)
        process_json_file(json_path)
    
    print("Processing complete. All JSON files have been updated with summaries.")

if __name__ == "__main__":
    main()