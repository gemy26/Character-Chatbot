import requests
import json

MISTRAL_API_KEY = "iEcMcl2U2bV1tj1h4OGkX76XBqE3rtTY"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def format_scene_with_mistral(scene_text):
    """Formats and expands a raw scene using Mistral AI."""
    
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
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-large-latest",  
        "messages": [{"role": "system", "content": "You are an expert script formatter."},
                     {"role": "user", "content": prompt}]
    }

    response = requests.post(MISTRAL_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Error:", response.text)
        return None

raw_scenes = []
with open('Scenes\Series 1, Episode 1.json', 'r', encoding='UTF-8') as r:
    raw_scenes = json.load(r)

# # Load character profiles
# with open("character_profiles.json", "r") as file:
#     character_profiles = json.load(file)

# Process each scene using Mistral AI
formatted_scenes = []
for scene in raw_scenes[:10]:
    character_name = "Sherlock"  
    # profile = character_profiles.get(character_name, "No profile available")
    formatted_scene = format_scene_with_mistral(scene["scene"]).strip("```json").strip("```")
    print(formatted_scene)
    print("######################")
    if formatted_scene:
        formatted_scenes.append(json.loads(formatted_scene))

# Save formatted scenes
with open("formatted_scenes.json", "w") as file:
    json.dump(formatted_scenes, file, indent=4)

print("Formatted scenes saved to formatted_scenes.json")




