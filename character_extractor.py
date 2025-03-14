import requests
import json
import os
import time

# OpenRouter API Key and Model
API_KEY = "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"  
MODEL = "qwen/qwen2.5-vl-72b-instruct:free"

# Function to split the script into chunks
def split_text(file_path, lines_per_chunk=1000):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    chunks = []
    for i in range(0, len(lines), lines_per_chunk):
        chunk = "".join(lines[i:i + lines_per_chunk])
        chunks.append(chunk)

    return chunks

# Function to send a request to OpenRouter
def call_openrouter(text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Optimized prompt for structured extraction
    prompt = """
    You are an expert in analyzing character Sherlock Holmes dialogues from scripts. 
    Your task is to extract structured data from the provided script segment.
    
    **Extract the following details about the character(Sherlock):**
    - **Personal Information**: Full name, age, occupation, physical appearance.
    - **Personality Traits**: Key behavioral traits.
    - **Speaking Style**: Tone, pacing, vocabulary, unique phrases.
    - **Major Life Events**: Significant events that shaped the character.
    - **Relationships**: Other characters they interact with and their relationship types.
    - **Emotional Range**: What makes them happy, angry, or fearful.
    - **Strengths & Weaknesses**: Their strongest and weakest qualities.
    - **Dialogue Analysis**: Patterns, frequent phrases, and unique speech styles.

    Return the extracted data in **valid JSON format**.
    {
    "Personal Information": {
        "Full Name": "",
        "Age": "",
        "Occupation": "",
        "Appearance": []
    },
    "Personality Traits": [],
    "Speaking Style": {
        "Tone": [],
        "Pacing": [],
        "Vocabulary": []
    },
    "background life" : "",
    "Major Life Events": [
        {
            "Event": "Becoming a consulting detective",
            "Impact": "Shaped his identity as an independent thinker and problem-solver, prioritizing logic over social conventions."
        },
        {
            "Event": "Working with John Watson (implied through context)",
            "Impact": "Marks the start of a professional and personal dynamic that challenges his isolation."
        }
    ],
    "Relationships": [
        {
            "Character Name": "John Watson",
            "Relationship Type": "Professional partner/friend",
            "Description": "Sherlock collaborates with John, though their interactions suggest an evolving partnership where Sherlock\u2019s intellectual rigor contrasts with John\u2019s grounded perspective."
        },
        {
            "Character Name": "Detective Inspector Lestrade",
            "Relationship Type": "Professional contact",
            "Description": "Lestrade seeks Sherlock\u2019s expertise, indicating a working relationship where Sherlock\u2019s disdain for bureaucracy is tolerated due to his effectiveness."
        },
        {
            "Character Name": "Dr. Molly Hooper",
            "Relationship Type": "Colleague",
            "Description": "Molly offers personal connection (e.g., coffee invitation), but Sherlock remains professionally distant, prioritizing cases over social engagement."
        }
    ],
    "Emotional Range": {
        "Anger": "Being interrupted, ignored, or perceived as 'ordinary' (implied through his dismissive behavior toward social niceties)",
        "Fear": "Boredom or intellectual stagnation; fear of being misunderstood or irrelevant",
        "Happiness": "Solving puzzles, engaging in deductive reasoning, and outthinking others"
    },
    "Strengths & Weaknesses": {
        "Strengths": [
            "Exceptional deductive reasoning",
            "Observational brilliance",
            "Unmatched focus on problems",
            "Technical precision"
        ],
        "Weaknesses": []
    },
    "Dialogue Analysis": {
        "Frequent Phrases": [],
        "Speech Patterns": ""
    }
}
    """.strip()

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7,
        "top_p" : 0.9
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Error:", response.text)
        return None

# Main processing function
def process_script(file_path):
    chunks = split_text(file_path, lines_per_chunk=1000)
    structured_data = []

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}...")
        result = call_openrouter(chunk)
        if result:
            try:
                cleaned_result = result.strip("```json").strip("```")
                print(cleaned_result)
                structured_data.append(json.loads(cleaned_result))
               
                with open(f"sherlock_profile_files/Sherlock_chunk_{i + 1}.json", "w", encoding="utf-8") as f:
                    json.dump(json.loads(cleaned_result), f, indent=4)
                    
            except json.JSONDecodeError:
                print(f"Error decoding JSON for chunk {i + 1}")
            
        time.sleep(60)        

    # Save extracted data
    output_file = "structured_character_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=4)

    print(f"\n✅ Extraction completed! Data saved in {output_file}")

# Run the script
if __name__ == "__main__":
    file_path = "Sherlock_script.txt"  
    process_script(file_path)

