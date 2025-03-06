from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class villanChatRequest(BaseModel):
    villan_name: str
    user_message:str
    
    
    

@app.get("/")
async def root():
    return {"message": "Hello World"}