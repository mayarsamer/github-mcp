# fastapi_server.py

import asyncio
from fastmcp import Client, FastMCP
from google import genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class PromptPayload(BaseModel):
    prompt: str

app = FastAPI()
mcp_client = Client("http://localhost:9000/mcp/")
gemini_client = genai.Client()

@app.on_event("startup")
async def startup_event():
    await mcp_client.__aenter__()

@app.on_event("shutdown")
async def shutdown_event():
    await mcp_client.__aexit__()

@app.post("/ask")
async def ask(payload: PromptPayload):
    try:
        response = await asyncio.wait_for(
            gemini_client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=payload.prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0,
                    tools=[mcp_client.session],
                ),
            ),
            
            timeout=10.0
        )
        return {"response": response.text}
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Request to Gemini timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
