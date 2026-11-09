"""Tests for the Hollowmere app (release 1.0)."""

import pytest

import app as fest


@pytest.fixture
def client():
    fest.app.config["TESTING"] = True
    return fest.app.test_client()


def test_health_says_ok(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_version_matches_the_code(client):
    assert client.get("/version").get_json() == {"version": fest.APP_VERSION}


def test_lineup_json_for_scripts(client):
    data = client.get("/lineup").get_json()
    assert data["version"] == fest.APP_VERSION
    assert len(data["sets"]) == 8
    assert data["ticket"] is None


def test_a_general_ticket_sees_the_lineup(client):
    data = client.get("/lineup?ticket=102").get_json()
    assert data["tier"] == "General"
    assert len(data["sets"]) == 8


def test_join_deals_a_three_digit_wristband(client):
    reply = client.get("/join")
    assert reply.status_code == 302
    ticket = client.get_cookie("ticket").value
    assert len(ticket) == 3
    assert int(ticket) not in fest.NOT_DEALT
    assert client.get_cookie("tier").value in ("General", "VIP")


def test_one_wristband_in_five_is_vip():
    tiers = [fest.deal_ticket()[1] for _ in range(50)]
    assert tiers.count("VIP") == 10


def test_scanning_again_keeps_your_wristband(client):
    client.get("/join")
    first = client.get_cookie("ticket").value
    client.get("/join")
    assert client.get_cookie("ticket").value == first


def test_request_id_comes_back(client):
    reply = client.get("/version", headers={"X-Request-ID": "demo1234"})
    assert reply.headers["X-Request-ID"] == "demo1234"


def test_crew_page_has_a_qr_code(client):
    assert b"<svg" in client.get("/crew").data


def test_metrics_count_lineup_requests(client):
    client.get("/lineup")
    assert b'fest_requests_total{path="/lineup",status="200"}' in client.get("/metrics").data
