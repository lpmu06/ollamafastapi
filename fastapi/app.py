from fastapi import FastAPI, Response
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello"}

@app.get('/ask')
def ask(prompt: str):
    res = requests.post('http://ollama:11434/api/generate', json={
        'prompt': prompt,
        'stream': False,
        'model': 'phi3',
        'max_tokens': 500,
        'temperature': 0.5
        #'top_p': 0.9,
        #'top_k': 50,
        #'stop': None,
    })

    return Response(content=res.text, media_type="application/json")
