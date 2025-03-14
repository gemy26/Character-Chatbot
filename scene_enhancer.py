import json
import requests
import re
import time
OPENROUTER_API = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"  

with open("Scenes/Series 1, Episode 1.json", "r") as file:
    scenes = json.load(file)

def extract_json(text):
    """ Extracts only the JSON part from LLM response. """
    match = re.search(r"\{.*\}", text, re.DOTALL)  
    return match.group(0) if match else None

def process_scene(scene_text):
    prompt = f"""
You are an AI assistant that extracts structured scenes from TV scripts.
Given the raw text of a scene, you will:

1️⃣ Identify key elements:
   - Scene Title
   - Location
   - Characters involved
   - Dialogue (who speaks, what they say)
   - Actions or key events
   - Emotions (if relevant)

2️⃣ Format the extracted data as **valid JSON** (strict JSON formatting).  

📌 **Important:** Only return the JSON. Do NOT include any explanations or comments.
📌 **Example JSON Output:**
```json
{{
    "scene_title": "Sherlock Meets Watson",
    "location": "St. Bart's Hospital, London",
    "characters": ["Sherlock Holmes", "Dr. John Watson"],
    "dialogue": [
        {{"speaker": "Sherlock", "text": "Hello, I'm Sherlock Holmes. I hear you're looking for a flatmate."}},
        {{"speaker": "Watson", "text": "Yes. How did you know that?"}}
    ],
    "actions": [
        "Sherlock studies Watson with sharp eyes.",
        "Watson shifts uncomfortably under Sherlock’s gaze."
    ]
}}

Scene: {scene_text}
"""

    response = requests.post(
        OPENROUTER_API,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "qwen/qwen2.5-vl-72b-instruct:free",  
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    try:
        response_data = response.json()  
        if "choices" not in response_data:
            print(f"⚠️ API Error: Unexpected response format:\n{response_data}")
            return None
        
        structured_output = response_data["choices"][0]["message"]["content"]
        cleaned_json = extract_json(structured_output)  # Extract valid JSON only
        
        return json.loads(cleaned_json) if cleaned_json else None
    except (KeyError, json.JSONDecodeError):
        print(f"⚠️ Error: Invalid JSON output from LLM. Full API response:\n{response.json()}")
        return None

processed_scenes = []
for scene in scenes:
    completed_scene = process_scene(scene["scene"])
    if completed_scene:
        processed_scenes.append(completed_scene)
    time.sleep(120) 

with open(f"structured__scenes.json", "w") as file:
    json.dump(processed_scenes, file, indent=2)

print("✅ Scene structuring & completion done! 🎬")
