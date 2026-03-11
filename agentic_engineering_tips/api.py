import os
import asyncio
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from agent import PhoneExtractionAgent

app = FastAPI(title="Phone Extraction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = PhoneExtractionAgent()


@app.get("/extract/{name}")
async def extract_phone_by_name(name: str, text: str = Query(...)):
    """Extract phone number for a specific name - streaming response"""

    async def event_generator():
        async for chunk in agent.extract_stream(name=name, text=text):
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0.01)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/extract")
async def extract_all_phones(text: str = Query(...)):
    """Extract all phone numbers from text - streaming response"""

    async def event_generator():
        async for chunk in agent.extract_stream(text=text):
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0.01)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
