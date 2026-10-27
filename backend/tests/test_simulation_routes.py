from fastapi.testclient import TestClient

from app.api.routes import simulations
from app.main import app
from app.simulation.loader import IncompatibleFailureScenario

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


def test_create_simulation_passes_mode_to_engine_and_returns_it() -> None:
    response = client.post(
        "/api/simulations",
        json={"scenario_id": "earthquake", "mode": "hybrid"},
    )

    assert response.status_code == 201
    run_id = response.json()["run_id"]
    assert response.json()["coordination_mode"] == "hybrid"
    assert simulations.runs._get(run_id).coordination_mode.value == "hybrid"


def test_create_simulation_rejects_unknown_coordination_mode() -> None:
    response = client.post(
        "/api/simulations",
        json={"scenario_id": "earthquake", "mode": "unsupported"},
    )

    assert response.status_code == 422
    assert "centralized" in response.json()["detail"][0]["ctx"]["expected"]


def test_create_simulation_defaults_to_centralized_mode() -> None:
    response = client.post(
        "/api/simulations",
        json={"scenario_id": "earthquake"},
    )

    assert response.status_code == 201
    assert response.json()["coordination_mode"] == "centralized"


def test_decentralized_route_advances_and_returns_task_claims() -> None:
    created = client.post(
        "/api/simulations",
        json={"scenario_id": "earthquake", "mode": "decentralized"},
    )
    assert created.status_code == 201
    run_id = created.json()["run_id"]

    advanced = client.post(
        f"/api/simulations/{run_id}/ticks",
        json={"ticks": 10},
    )
    state = client.get(f"/api/simulations/{run_id}").json()

    assert advanced.status_code == 200
    assert state["coordination_mode"] == "decentralized"
    assert state["tick"] == 10
    assert any(task["claims"] for task in state["tasks"])
    assert all(
        len(task["assigned_to"]) <= task["required_drones"]
        or task["status"] == "completed"
        for task in state["tasks"]
    )


def test_hybrid_route_exposes_outage_reconciliation_and_recovery() -> None:
    created = client.post(
        "/api/simulations",
        json={"scenario_id": "earthquake", "mode": "hybrid"},
    )
    assert created.status_code == 201
    run_id = created.json()["run_id"]
    installed = client.post(
        f"/api/simulations/{run_id}/failures",
        json={"failure_scenario_id": "controller_failure"},
    )
    assert installed.status_code == 200

    outage = client.post(
        f"/api/simulations/{run_id}/ticks",
        json={"ticks": 60},
    )
    assert outage.status_code == 200
    assert outage.json()["operational_strategy"] == "decentralized_fallback"
    assert outage.json()["controller_available"] is False
    assert outage.json()["failure_events"][0]["status"] == "active"
    assert any(task["claims"] for task in outage.json()["tasks"])

    recovery = client.post(
        f"/api/simulations/{run_id}/ticks",
        json={"ticks": 93},
    )
    assert recovery.status_code == 200
    assert recovery.json()["tick"] == 153
    assert recovery.json()["operational_strategy"] == "reconciliation"
    assert recovery.json()["controller_reachable"] is True
    assert recovery.json()["reconciliation_history"]

    recovered = client.post(
        f"/api/simulations/{run_id}/ticks",
        json={"ticks": 4},
    )
    assert recovered.status_code == 200
    assert recovered.json()["tick"] == 157
    assert recovered.json()["operational_strategy"] == "centralized_allocation"
    assert recovered.json()["failure_events"][0]["status"] == "resolved"


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


def test_install_failure_schedule_and_advance_lifecycle() -> None:
    created = client.post(
        "/api/simulations",
        json={"scenario_id": "earthquake"},
    )
    run_id = created.json()["run_id"]

    installed = client.post(
        f"/api/simulations/{run_id}/failures",
        json={"failure_scenario_id": "demo_core"},
    )

    assert installed.status_code == 200
    assert installed.json()["failure_scenario_id"] == "demo_core"
    assert installed.json()["failure_test_matrix_entry"]["scenario_id"] == "earthquake"
    assert [event["status"] for event in installed.json()["failure_events"]] == [
        "scheduled",
        "scheduled",
    ]
    assert client.get(f"/api/simulations/{run_id}").json()["failure_scenario_id"] == "demo_core"

    advanced = client.post(
        f"/api/simulations/{run_id}/ticks",
        json={"ticks": 60},
    )
    assert advanced.status_code == 200
    assert advanced.json()["tick"] == 60
    assert advanced.json()["failure_events"][0]["status"] == "active"


def test_failure_schedule_validation_does_not_change_run_state() -> None:
    created = client.post(
        "/api/simulations",
        json={"scenario_id": "cyclone"},
    )
    run_id = created.json()["run_id"]

    unknown = client.post(
        f"/api/simulations/{run_id}/failures",
        json={"failure_scenario_id": "not-a-failure"},
    )
    assert unknown.status_code == 404
    assert client.get(f"/api/simulations/{run_id}").json()["failure_scenario_id"] is None

    extra_field = client.post(
        f"/api/simulations/{run_id}/failures",
        json={"failure_scenario_id": "demo_core", "type": "controller_outage"},
    )
    assert extra_field.status_code == 422
    assert client.get(f"/api/simulations/{run_id}").json()["failure_scenario_id"] is None

    missing_run = client.post(
        "/api/simulations/not-a-run/failures",
        json={"failure_scenario_id": "demo_core"},
    )
    assert missing_run.status_code == 404

    advanced = client.post(
        f"/api/simulations/{run_id}/ticks",
        json={"ticks": 1},
    )
    assert advanced.status_code == 200
    too_late = client.post(
        f"/api/simulations/{run_id}/failures",
        json={"failure_scenario_id": "demo_core"},
    )
    assert too_late.status_code == 409
    assert client.get(f"/api/simulations/{run_id}").json()["failure_scenario_id"] is None


def test_failure_schedule_request_requires_identifier() -> None:
    created = client.post(
        "/api/simulations",
        json={"scenario_id": "flood"},
    )
    response = client.post(
        f"/api/simulations/{created.json()['run_id']}/failures",
        json={},
    )
    assert response.status_code == 422


def test_incompatible_failure_schedule_does_not_change_run_state(monkeypatch) -> None:
    created = client.post(
        "/api/simulations",
        json={"scenario_id": "flood"},
    )
    run_id = created.json()["run_id"]

    def reject_pair(failure_scenario_id: str, scenario_id: str):
        raise IncompatibleFailureScenario("No matrix pair.")

    monkeypatch.setattr(simulations.loader, "load_failure_scenario", reject_pair)
    response = client.post(
        f"/api/simulations/{run_id}/failures",
        json={"failure_scenario_id": "demo_core"},
    )

    assert response.status_code == 422
    state = client.get(f"/api/simulations/{run_id}").json()
    assert state["failure_scenario_id"] is None
    assert state["failure_events"] == []
