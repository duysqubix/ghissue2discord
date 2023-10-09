from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Body

import discord
from discord.threads import ChannelType
import asyncio
import json

app = FastAPI(
    title="ghissueListener",
    version="0.1.0",
    # docs_url=None,
    # redoc_url="/docs",
)

_TOKEN = "MTE2MDc2MTYxMjU1OTQ1MDI1NA.GSmaQJ.Dw39JyuO7VIbJVY4Q-8Kf6pGsq6zhvMzwLX6I0"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@app.on_event("startup")
def setup():
    asyncio.create_task(client.start(_TOKEN))


@app.post("/test")
async def test_create_issue():
    channel = client.get_channel(int(1160755411549429880))
    thread = await channel.create_thread(
        name="@Dusk125", auto_archive_duration=1440, content="I love technology."
    )

    return {"message": "Hello World"}
