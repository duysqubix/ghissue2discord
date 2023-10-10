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

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="ghissueListener",
    version="0.1.0",
)

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

FORUM_CHANNEL_ID = int(os.getenv("FORUM_CHANNEL_ID"))


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
        f"**{issue_title}**\n\n{issue_content}\n\n{issue_url}\n\n"
        f"**Repository:** {repo_name}\n{repo_url}\n\n"
        f"**Created at:** {issue_creation_date}\n\n"
        f"id: {issue.get('id')}\n\n"
    )

    channel = client.get_channel(FORUM_CHANNEL_ID)
    thread = await channel.create_thread(
        name=issue_title,
        content=content,
    )

    for tag in channel.available_tags:
        if tag.name == repo_name:
            await thread.add_tag(tag)
            
    return thread


async def _handle_issue_close(payload):
    issueId = payload.get("issue", {}).get("id")

    if not issueId:
        raise Exception("Issue id not found")

    channel = client.get_channel(FORUM_CHANNEL_ID)
    thread = await channel.create_thread(
        name=issue_title,
        content=content,
    )
    return thread


async def handle_issues(payload):
    if payload.get("action") == "opened":
        return await _handle_issue_open(payload)

    if payload.get("action") == "closed":
        return await _handle_issue_close(payload)


async def handle_events(payload):
    if "issue" in payload:
        await handle_issues(payload)

    return True


@app.on_event("startup")
def setup():
    asyncio.create_task(client.start(os.getenv("DISCORD_TOKEN")))


@app.post("/gopxl/webhook")
async def handle_webhooks(payload=Body(...)):
    _ = await handle_events(payload)
