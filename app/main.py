from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Body
from dotenv import load_dotenv
from discord.threads import ChannelType


import discord
import asyncio
import json
import os
import logging
import re


logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="ghissueListener",
    version="0.1.0",
)

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
FORUM_CHANNEL_ID = int(os.getenv("FORUM_CHANNEL_ID"))


async def handle_events(payload):
    if "issue" in payload:
        await handle_issues(payload)

    return True


async def _handle_issue_open(payload):
    issue = payload.get("issue")
    issue_url = issue.get("html_url")
    issue_title = issue.get("title")
    issue_creation_date = issue.get("created_at")
    issue_content = issue.get("body")

    repo = payload.get("repository")
    repo_name = repo.get("name")
    repo_url = repo.get("html_url")

    content = (
        f"{issue_content}\n\n"
        f"{issue_url}\n\n"
        f"**Repository:**\n{repo_url}\n\n"
        f"**Created at:** {issue_creation_date} by "
        f"[{issue.get('user').get('login')}]( {issue.get('user').get('html_url')} )\n\n"
        f"id:{issue.get('id')}\n"
    )

    channel = client.get_channel(FORUM_CHANNEL_ID)
    thread = await channel.create_thread(
        name=issue_title,
        content=content,
    )


async def _handle_issue_close(payload):
    issue = payload.get("issue")
    id = issue.get("id")

    rpattern = re.compile(r"id:(\d+)")

    channel = client.get_channel(FORUM_CHANNEL_ID)
    thread = channel.threads[0]
    for thread in channel.threads:
        hist = thread.history(oldest_first=True)
        async for msg in hist:
            if rp := rpattern.search(msg.content):
                if int(rp.group(1)) == id:
                    await thread.send("Issue closed, archiving thread.")
                    await thread.archive(locked=True)
                    return


async def handle_issues(payload):
    if payload.get("action") == "opened":
        return await _handle_issue_open(payload)

    if payload.get("action") == "closed":
        return await _handle_issue_close(payload)


@app.on_event("startup")
def setup():
    asyncio.create_task(client.start(DISCORD_TOKEN))


@app.post("/gopxl/webhook")
async def test_create_issue(payload=Body(...)):
    thread = await handle_events(payload)
