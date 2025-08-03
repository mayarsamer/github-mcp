import asyncio
from fastmcp import Client
from google import genai
import os


mcp_client = Client("http://0.0.0.0:8000/mcp/")
gemini_client = genai.Client()

async def main():    
    async with mcp_client:
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents="make another issue for the repo mayar-is-awesome called 'the webpage is messed up fix it' with label 'bug' and body 'hello are you there fix it nowww!'",
            config=genai.types.GenerateContentConfig(
                temperature=0,
                tools=[mcp_client.session],  # Pass the FastMCP client session
            ),
        )
        print(response.text)

if __name__ == "__main__":
    asyncio.run(main())