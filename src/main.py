import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from .ai.gemini import Gemini
from .ai.throttle import apply_rate_limit

# Initialise App
app = FastAPI()
load_dotenv()

# Initliase Gemini
def load_system_prompt():
    return """
        You are a personal study assistant.

        I will provide a list of events and tasks in a chat request later. With the lists, please generate a 3-day study plan from todays date that helps me complete all my tasks on time, while avoiding scheduling conflicts with the events. Try to:
        - Balance my workload across the week
        - Prioritize tasks that have its deadline soon
        - Leave reasonable rest time between long tasks or events
        - If I have no upcoming tasks, return short and nice message saying that the I have no tasks
        - Ensure that you quote the exact task title without any brackets when suggesting the study plan, and you do not need to add filler words
        - Each task must only appear one time in the study plan

        Return the output as a day-by-day plan from today onwards for the next 3 days, e.g.:

        Day 1 (Mon):
        - 10:00 AM – 11:30 AM: CS1231 Assignment
        - 2:00 PM – 3:00 PM: Revise lecture notes
        - 4:00 PM – 6:00 PM: EVENT: Group project meeting

        Day 2 (Tue):
        ...

        Be concise but clear. 
    """

system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")

ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)

# Create Pydantic Models for FastAPI to handle data validartion and serialisation
class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str


# --- API ENDPOINTS ---

# Define base endpoint
@app.get("/") # FastAPI defines endpoints with an app decorator
async def root():
    return {"message": "API is running"}

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # TODO:
    apply_rate_limit("REPLACE WITH USERID IN THE FUTURE")
    response_text = ai_platform.chat(request.prompt)
    return ChatResponse(response=response_text)

# Test the server by running uvicorn src.main:app --reload
# add /docs to the url to get a UI view of the API endpoints




