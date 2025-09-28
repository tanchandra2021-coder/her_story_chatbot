from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:3000"] for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    leader: str
    user_input: str

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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_intro},
                {"role": "user", "content": request.user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Error: {e}"

    return {"response": reply}


