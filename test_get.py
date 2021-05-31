import pytest
from flask import url_for, request

def test_homepage_get(client):
    test_client = client.test_client()
    with test_client:
        res = test_client.get(url_for('/'), follow_redirects=True)
        assert res.status_code == 200