from fastapi.testclient import TestClient

from social_console.main import AGENTS, app


def test_console_registers_exactly_six_social_agents():
    assert len(AGENTS) == 6
    assert len({agent.key for agent in AGENTS}) == 6


def test_console_exposes_a_read_only_agent_api():
    with TestClient(app) as client:
        response = client.get("/api/agents")
        unknown = client.get("/api/agents/unknown")

    assert response.status_code == 200
    assert len(response.json()) == 6
    assert unknown.status_code == 404
