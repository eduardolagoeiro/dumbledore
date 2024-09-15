from database import find_by_text
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def send_message(prompt):
    retrieved_docs = find_by_text(prompt)
    
    print(f"docs: {len(retrieved_docs)}, {', '.join(map(lambda x: x.key, retrieved_docs))}")
    
    if retrieved_docs:
        retrieved_texts = "\n".join([doc.text for doc in retrieved_docs])
        augmented_prompt = f"Context:\n{retrieved_texts}\n\nQuestion: {prompt}"
    else:
        augmented_prompt = prompt

    payload = {
        "model": "llama3.1",
        "prompt": augmented_prompt
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    data = json.loads(decoded_line)
                    if "response" in data:
                        full_response += data["response"]
                except json.JSONDecodeError:
                    continue

        return full_response or "No response from Ollama."
    
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {str(e)}"
