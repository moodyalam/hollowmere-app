"""FEST-42: VIP backstage sets (Riya)."""

import app as fest


def client():
    fest.app.config["TESTING"] = True
    return fest.app.test_client()


def test_general_wristband_sees_no_backstage_sets():
    sets = client().get("/lineup?ticket=102").get_json()["sets"]
    assert not any(s.get("backstage") for s in sets)


def test_no_wristband_sees_the_public_lineup():
    sets = client().get("/lineup").get_json()["sets"]
    assert len(sets) == 8
