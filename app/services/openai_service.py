import requests
import json
import os
from app.utils.helper_functions import build_prompt, construct_messages_list

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_EMBEDDING_MODEL = 'text-embedding-ada-002'
PROMPT_LIMIT = 3750
CHATGPT_MODEL = 'gpt-4-1106-preview'

def get_embedding(chunk):
    try:
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f"Bearer {OPENAI_API_KEY}"
        }
        data = {'model': OPENAI_EMBEDDING_MODEL, 'input': chunk}
        response = requests.post('https://api.openai.com/v1/embeddings', headers=headers, json=data)
        response.raise_for_status()
        embedding = response.json()["data"][0]["embedding"]
        return embedding
    except requests.RequestException as e:
        print(f"Failed to get embedding: {e}")
        return []

def get_llm_answer(prompt):
  # Aggregate a messages array to send to the LLM
  messages = [{"role": "system", "content": "You are a helpful assistant and brand voice classifier."}]
  messages.append({"role": "user", "content": prompt})
  print(f'prompt: {prompt}')
  url = 'https://api.openai.com/v1/chat/completions'
  headers = {
      'content-type': 'application/json; charset=utf-8',
      'Authorization': f"Bearer {OPENAI_API_KEY}"            
  }
  data = {
      'model': CHATGPT_MODEL,
      'messages': messages,
      'temperature': 1, 
      'max_tokens': 1000
  }
  response = requests.post(url, headers=headers, data=json.dumps(data))
  
  # return the final answer
  response_json = response.json()
  completion = response_json["choices"][0]["message"]["content"]
  return completion