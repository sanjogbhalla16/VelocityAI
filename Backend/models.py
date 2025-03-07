#here we will create the models for our database. Ensures the API gets structured input/output.

class villanChatRequest(BaseModel):
    villan_name: str
    user_message:str

class villanChatResponse(BaseModel):
    villan_response:str