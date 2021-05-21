import pytest

def test_homepage_get(client):
    res = client.get('/')
    assert res.status_code == 200