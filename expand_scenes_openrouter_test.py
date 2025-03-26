import requests
import json
import re
# OpenRouter API key (Replace with your actual API key)
API_KEY = "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" 
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def extract_json_from_text(text):
    """
    Extract JSON content from a text block that contains additional explanations or formatting.
    """
    match = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            json_data = json.loads(json_str)  # Validate JSON format
            return json.dumps(json_data, indent=4)  # Pretty-print JSON
        except json.JSONDecodeError:
            print("Invalid JSON format detected.")
    return None


# Function to send a scene to OpenRouter API and get formatted output
def format_scene_with_llm(scene_text):
    """Formats a raw scene using OpenRouter's LLM."""
    
    prompt = f"""
    You are an expert screenwriter. Your task is to take a raw scene and format it into a structured experience for AI training.

    ### Raw Scene:
    {scene_text}

    ### Instructions:
    1. Expand the scene with **vivid descriptions, emotions, and natural dialogue**.
    2. Format the scene using the **standard JSON structure** below.
    3. Stay **true to the character’s personality, relationships, and knowledge**.

    ### Output Format:
    {{
      "scene_id": "[Auto-generate Scene ID]",
      "title": "[Expanded Scene Title]",
      "location": "[Expanded Setting Details]",
      "time": "[Expanded Time Context]",
      "characters": ["[Character List]"],
      "scene_description": "[Expanded Narrative]",
      "dialogue": [
        {{"speaker": "[Character Name]", "line": "[Expanded Dialogue]"}},
        {{"speaker": "[Character Name]", "line": "[More Dialogue]"}}
      ],
      "thoughts": [
        {{"character": "[Character Name]", "line": "[Expanded Internal Monologue]"}}
      ],
      "actions": [
        {{"character": "[Character Name]", "action": "[Expanded Physical Action]"}}
      ],
      "emotions": {{
        "[Character Name]": "[Emotional State]",
        "[Character Name]": "[Emotional State]"
      }},
      "outcome": "[Describe how the scene resolves]"
    }}

    Now, expand and format the following scene:
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemma-3-27b-it",  
        "messages": [{"role": "system", "content": "You are an expert script formatter."},
                     {"role": "user", "content": prompt}],
                     "temperature": 0.7,
        "top_p" : 0.9
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Error:", response.text)
        return None




raw_scenes = []
with open('Scenes\Series 1, Episode 1.json', 'r', encoding='UTF-8') as r:
    raw_scenes = json.load(r)

# Load character profiles
with open("character_profiles.json", "r") as file:
    character_profiles = json.load(file)

formatted_scenes = []
for scene in raw_scenes:
    character_name = "Sherlock"  
    formatted_scene = extract_json_from_text(format_scene_with_llm(scene["scene"]))
    print(formatted_scene)
    print("######################")
    if formatted_scene:
        formatted_scenes.append(json.loads(formatted_scene))

# Save formatted scenes
with open("formatted_scenes_openRouter_Google: Gemma 3 27B.json", "w") as file:
    json.dump(formatted_scenes, file, indent=4)

print("Formatted scenes saved to formatted_scenes.json")

formatted_scene = extract_json_from_text(format_scene_with_llm(raw_scenes[3]["scene"]))
print(formatted_scene)