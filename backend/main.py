from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Load API key from environment variable
# Make sure to set OPENAI_API_KEY in your Codespace secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

# Request body model
class ChatRequest(BaseModel):
    leader: str
    user_input: str

# Leader prompts
LEADERS = {
    "Michelle Obama": "You are Michelle Obama, a policy-minded and empathetic mentor. Give direct finance advice.",
    "Frida Kahlo": "You are Frida Kahlo, reflective and artistic. Give finance advice using metaphors.",
    "Marie Curie": "You are Marie Curie, scientific and evidence-first. Give clear finance advice.",
    "Rosa Parks": "You are Rosa Parks, calm and principled. Give concise finance advice.",
    "Malala Yousafzai": "You are Malala Yousafzai, clear and empowering. Give actionable finance advice."
}

@app.post("/chat")
def chat(request: ChatRequest):
    prompt_intro = LEADERS.get(request.leader, "")
    prompt = f"{prompt_intro}\nUser: {request.user_input}\n{request.leader}:"
    
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        reply = response.choices[0].text.strip()
    except Exception as e:
        reply = f"Error: {e}"
    
    return {"response": reply}

