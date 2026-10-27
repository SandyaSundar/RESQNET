import logging
from threading import RLock
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from app.simulation.engine import (
    CoordinationMode,
    MAX_TICKS_PER_ADVANCE,
    FailureScheduleConflict,
    SimulationEngine,
)
from app.simulation.loader import (
    DatasetError,
    FailureScenarioNotFound,
    IncompatibleFailureScenario,
    ScenarioLoader,
)

logger = logging.getLogger(__name__)
router = APIRouter()
loader = ScenarioLoader()


class CreateSimulationRequest(BaseModel):
    scenario_id: str = Field(min_length=1)
    mode: CoordinationMode = CoordinationMode.CENTRALIZED


class AdvanceTicksRequest(BaseModel):
    ticks: int = Field(default=1, ge=1, le=MAX_TICKS_PER_ADVANCE)


class InstallFailureScheduleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    failure_scenario_id: str = Field(min_length=1, max_length=100)


class SimulationRuns:
    def __init__(self) -> None:
        self._runs: dict[str, SimulationEngine] = {}
        self._lock = RLock()

    def create(self, engine: SimulationEngine) -> dict[str, Any]:
        with self._lock:
            self._runs[engine.run_id] = engine
            return engine.get_state()

    def advance(self, run_id: str, ticks: int) -> dict[str, Any]:
        with self._lock:
            return self._get(run_id).advance(ticks)

    def install_failure_schedule(
        self,
        run_id: str,
        failure_scenario_id: str,
    ) -> dict[str, Any]:
        with self._lock:
            engine = self._get(run_id)
            schedule = loader.load_failure_scenario(
                failure_scenario_id,
                engine.scenario.scenario_id,
            )
            return engine.install_failure_schedule(schedule)

    def state(self, run_id: str) -> dict[str, Any]:
        with self._lock:
            return self._get(run_id).get_state()

    def _get(self, run_id: str) -> SimulationEngine:
        engine = self._runs.get(run_id)
        if engine is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Simulation run not found.",
            )
        return engine


runs = SimulationRuns()


def _load_scenarios():
    try:
        return loader.load_all()
    except DatasetError:
        logger.exception("Scenario dataset validation failed.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Scenario dataset is unavailable or invalid.",
        ) from None


@router.get("/scenarios")
def list_scenarios() -> list[dict[str, Any]]:
    return [
        {
            "scenario_id": scenario.scenario_id,
            "name": scenario.name,
            "disaster_type": scenario.disaster_type,
            "width": scenario.width,
            "height": scenario.height,
            "task_count": len(scenario.tasks),
            "drone_count": len(scenario.drones),
            "candidate_detection_count": len(scenario.candidate_detections),
        }
        for scenario in _load_scenarios()
    ]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_simulation(request: CreateSimulationRequest) -> dict[str, Any]:
    scenario = next(
        (
            item
            for item in _load_scenarios()
            if item.scenario_id == request.scenario_id
        ),
        None,
    )
    if scenario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found.",
        )
    return runs.create(
        SimulationEngine(scenario, coordination_mode=request.mode)
    )


@router.post("/{run_id}/ticks")
def advance_simulation(
    run_id: str,
    request: AdvanceTicksRequest,
) -> dict[str, Any]:
    try:
        return runs.advance(run_id, request.ticks)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid tick count.",
        ) from None


@router.post("/{run_id}/failures")
def install_failure_schedule(
    run_id: str,
    request: InstallFailureScheduleRequest,
) -> dict[str, Any]:
    try:
        return runs.install_failure_schedule(run_id, request.failure_scenario_id)
    except FailureScenarioNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failure scenario not found.",
        ) from None
    except IncompatibleFailureScenario:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Failure scenario is not configured for this scenario.",
        ) from None
    except FailureScheduleConflict as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from None
    except DatasetError:
        logger.exception("Failure scenario dataset validation failed.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failure scenario dataset is unavailable or invalid.",
        ) from None


@router.get("/{run_id}")
def get_simulation(run_id: str) -> dict[str, Any]:
    return runs.state(run_id)
