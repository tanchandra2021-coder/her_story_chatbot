from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

# Load model once
model_name = "EleutherAI/gpt-j-6B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()

# Request body model
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
        inputs = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                pad_token_id=tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.replace(prompt, "").strip()
    except Exception as e:
        response = f"Error: {e}"
    
    return {"response": response}
