import pytest
from flask import url_for, request

def test_homepage_get(client):
    res = client.get(url_for('/'), follow_redirects=True)
    assert res.status_code == 200