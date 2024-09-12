from fastapi.testclient import TestClient

from app.core.openapi import add_custom_openapi_schema
from app.main import app

client = TestClient(app)


def test_custom_openapi_schema_already_set():
    openapi_schema = {
        "openapi": "3.0.2",
        "info": {"title": "Title", "version": "0.1.0"},
    }
    app.openapi_schema = openapi_schema
    add_custom_openapi_schema(app)
    assert app.openapi_schema["info"]["title"] == "Title"
