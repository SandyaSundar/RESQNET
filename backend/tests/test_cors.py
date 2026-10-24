from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import app


def test_cors_allows_configured_production_frontend() -> None:
    response = TestClient(app).options(
        "/api/health",
        headers={
            "Origin": "https://resqnet-eight-psi.vercel.app",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == (
        "https://resqnet-eight-psi.vercel.app"
    )
    assert "access-control-allow-credentials" not in response.headers


def test_cors_rejects_unconfigured_origin() -> None:
    response = TestClient(app).options(
        "/api/health",
        headers={
            "Origin": "https://unlisted.example",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers

def test_cors_origins_can_be_overridden_with_comma_separated_values(monkeypatch) -> None:
    monkeypatch.setenv(
        "CORS_ORIGINS",
        "https://resqnet-eight-psi.vercel.app, https://preview.example",
    )

    configured = Settings()

    assert configured.allowed_cors_origins == [
        "https://resqnet-eight-psi.vercel.app",
        "https://preview.example",
    ]