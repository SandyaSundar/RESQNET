from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_scenarios_returns_real_dataset() -> None:
    response = client.get("/api/simulations/scenarios")

    assert response.status_code == 200
    assert {scenario["scenario_id"] for scenario in response.json()} == {
        "earthquake",
        "cyclone",
        "flood",
    }


def test_frontend_dataset_endpoints_and_production_cors() -> None:
    dataset = client.get("/api/datasets/drone-config")
    assert dataset.status_code == 200
    assert isinstance(dataset.json()["fleets"], list)

    preflight = client.options(
        "/api/health",
        headers={
            "Origin": "https://resqnet-eight-psi.vercel.app",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert preflight.status_code == 200
    assert preflight.headers["access-control-allow-origin"] == (
        "https://resqnet-eight-psi.vercel.app"
    )


def test_create_advance_and_retrieve_run() -> None:
    created = client.post(
        "/api/simulations",
        json={"scenario_id": "earthquake"},
    )

    assert created.status_code == 201
    initial_state = created.json()
    assert len(initial_state["drones"]) == 6
    assert initial_state["tick"] == 0

    advanced = client.post(
        f"/api/simulations/{initial_state['run_id']}/ticks",
        json={"ticks": 1},
    )
    retrieved = client.get(f"/api/simulations/{initial_state['run_id']}")

    assert advanced.status_code == 200
    assert advanced.json()["tick"] == 1
    assert retrieved.json()["tick"] == 1


def test_unknown_scenario_and_run_are_not_found() -> None:
    assert client.post(
        "/api/simulations",
        json={"scenario_id": "not-a-scenario"},
    ).status_code == 404
    assert client.get("/api/simulations/not-a-run").status_code == 404


def test_invalid_tick_request_is_rejected() -> None:
    created = client.post(
        "/api/simulations",
        json={"scenario_id": "flood"},
    )

    response = client.post(
        f"/api/simulations/{created.json()['run_id']}/ticks",
        json={"ticks": 0},
    )

    assert response.status_code == 422
