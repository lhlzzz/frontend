"""One browser-facing observation surface for social media agents."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from fastapi import FastAPI, HTTPException


STATIC_DIR = Path(__file__).resolve().parent / "static"


@dataclass(frozen=True)
class Agent:
    key: str
    name: str
    role: str
    workspace: str
    adapter_env: str
    default_adapter: str | None = None


AGENTS: tuple[Agent, ...] = (
    Agent("douyin", "抖音", "分发型短视频准备", "douyin", "DOUYIN_SOCIAL_API_BASE_URL", "http://127.0.0.1:8010"),
    Agent("xiaohongshu", "小红书", "搜索型笔记准备", "xiaohongshu", "XIAOHONGSHU_SOCIAL_API_BASE_URL"),
    Agent("kuaishou", "快手", "信任型短视频准备", "kuaishou", "KUAISHOU_SOCIAL_API_BASE_URL"),
    Agent("x_twitter", "X", "英文内容与公开研究", "x", "X_TWITTER_SOCIAL_API_BASE_URL"),
    Agent("wechat_channels", "视频号", "蓝 V 信任内容准备", "shipinghao", "WECHAT_CHANNELS_SOCIAL_API_BASE_URL"),
    Agent("xianyu", "闲鱼", "商品文案与买家路径准备", "xianyu", "XIANYU_SOCIAL_API_BASE_URL"),
)


def get_agent(key: str) -> Agent:
    for agent in AGENTS:
        if agent.key == key:
            return agent
    raise KeyError(key)


def adapter_url(agent: Agent) -> str | None:
    return os.getenv(agent.adapter_env) or agent.default_adapter


def read_snapshot(agent: Agent) -> dict:
    base_url = adapter_url(agent)
    if base_url is None:
        return {"agent": asdict(agent), "state": "not_configured", "snapshot": None}
    try:
        with urlopen(f"{base_url.rstrip('/')}/api/dashboard", timeout=1.5) as response:
            payload = json.load(response)
    except (URLError, TimeoutError, OSError, json.JSONDecodeError):
        return {"agent": asdict(agent), "state": "unavailable", "snapshot": None}

    counts = payload.get("counts", {})
    snapshot = {
        "voice": payload.get("voice"),
        "boundary": payload.get("boundary"),
        "metrics": {
            "briefs": int(counts.get("briefs", 0)),
            "scripts": int(counts.get("scripts", 0)),
            "blocked": int(counts.get("blocked", 0)),
        },
        "records": payload.get("briefs", []),
    }
    return {"agent": asdict(agent), "state": "connected", "snapshot": snapshot}


app = FastAPI(
    title="Hermes Social Media Console",
    description="Read-only internal observation for independently owned platform data.",
)


@app.get("/api/agents")
def list_agents() -> list[dict]:
    return [read_snapshot(agent) for agent in AGENTS]


@app.get("/api/agents/{agent_key}")
def agent_overview(agent_key: str) -> dict:
    try:
        agent = get_agent(agent_key)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Unknown social media agent.") from error
    return read_snapshot(agent)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "system": "social_media_console"}


app.frontend("/", directory=str(STATIC_DIR))
