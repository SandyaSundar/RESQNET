# RESQNET — Backend Services

**Decentralized Multi-Agent Drone Coordination for Disaster Response**

## 1. Overview

The RESQNET backend is responsible for connecting the mission-control frontend with disaster-scenario data, drone coordination mechanisms, computer-vision predictions, and area-prioritization logic.

It serves as the communication and processing layer of the system, enabling mission information to be exchanged, search tasks to be managed, and potential person detections to contribute to disaster-response decisions.

The backend is designed to support a decentralized coordination architecture in which drones can make local decisions when central communication becomes unavailable.

## 2. Objectives

- Provide structured API access to disaster scenarios and mission information.
- Manage search tasks, task status, and area-level progress.
- Receive and process candidate person-detection results from the computer-vision module.
- Associate detections with the relevant image, drone, and search area.
- Support rule-based prioritization of disaster-affected areas.
- Facilitate task recovery and synchronization after simulated communication failures.
- Maintain consistency between mission data and the frontend dashboard.

## 3. System Architecture

The backend is designed to connect the following components:

- **Frontend:** React, TypeScript, and Vite-based mission-control dashboard.
- **API layer:** Python and FastAPI for HTTP endpoints and data exchange.
- **Scenario management:** JSON-based disaster scenarios containing affected zones, obstacles, no-fly areas, and mission tasks.
- **Computer vision:** Pretrained YOLO inference that produces candidate person detections.
- **Coordination logic:** Task allocation, progress tracking, reassignment, and synchronization.
- **Priority engine:** Rule-based scoring of eligible search areas.

### Data Flow

1. The frontend requests scenario and mission information.
2. The backend retrieves or processes the relevant scenario data.
3. Drone coordination logic evaluates task assignments and search progress.
4. The computer-vision module supplies detection evidence when connected.
5. The priority engine evaluates relevant evidence and task urgency.
6. Updated task and priority information can be returned to the frontend.

## 4. Core Backend Modules

### 4.1 Scenario Management

The scenario-management module handles disaster scenarios supplied in the project's JSON format.

Scenario information may include:

- Scenario identifier and disaster type.
- Search-zone identifiers and locations within the simulation grid.
- Task priorities, deadlines, and required drone counts.
- Obstacles, no-fly zones, and communication dead zones.
- Drone operational constraints and hub-range information.

The backend should preserve the scenario schema and validate incoming data before processing it.

### 4.2 Drone Task Management

The task-management module tracks the lifecycle of search tasks.

Expected task states may include:

- Pending
- Assigned
- In progress
- Completed
- Interrupted
- Reassigned

When a drone becomes unavailable or communication is interrupted, unfinished tasks can be identified for reassignment according to the coordination rules.

A task should not be marked complete solely because a drone visited an area. Completion should follow the project's defined search and verification criteria.

### 4.3 Computer-Vision Integration

The computer-vision module uses a pretrained YOLO model to identify potential people in aerial disaster imagery.

A proposed structured detection record is:

    {
      "drone_id": "DR01",
      "area_id": "B4",
      "image_id": "IMG001",
      "person_count": 2,
      "detections": [
        {
          "bbox": [120, 80, 190, 220],
          "confidence": 0.87,
          "verification_status": "unverified"
        }
      ]
    }

The bounding-box values represent image pixel coordinates in the order `[x1, y1, x2, y2]`. The example values are illustrative.

Detection records should retain their association with the relevant image and simulated search area. A model prediction represents a potential sighting, not a confirmed survivor.

### 4.4 Area Prioritization

The backend can pass validated scenario information and detection evidence to a separate priority engine.

The priority engine may consider:

- Existing scenario priority.
- Person-detection evidence and confidence.
- Remaining task deadline.
- Search progress and coverage.
- Communication or coordination problems.

Drone availability, battery limitations, blocked routes, and no-fly zones must be evaluated as feasibility constraints before a task is assigned.

The scoring formula and its implementation should remain configurable and independently testable.

### 4.5 Communication and Recovery

The coordination layer is intended to handle simulated network interruptions by preserving local task state, identifying unfinished tasks, and supporting reassignment.

When communication resumes, the system should reconcile task updates and avoid conflicting assignments or duplicate completion records.

The exact persistence, synchronization, and conflict-resolution mechanisms depend on the backend implementation.

## 5. Proposed API Structure

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/scenarios` | Retrieve available disaster scenarios |
| GET | `/api/scenarios/{scenario_id}` | Retrieve a specific scenario |
| GET | `/api/tasks` | Retrieve task information |
| GET | `/api/areas/priorities` | Retrieve area-priority results |
| POST | `/api/detections` | Submit computer-vision detection results |
| POST | `/api/tasks/{task_id}/status` | Update task status |

These endpoints are a proposed interface and should be aligned with the actual route definitions in the backend code before use.

## 6. Validation and Error Handling

The backend should validate:

- Required fields and data types.
- Valid scenario, area, and task identifiers.
- Confidence values within the range 0–1.
- Valid bounding-box coordinates.
- Duplicate or outdated task updates.
- Invalid requests and unavailable resources.

Appropriate HTTP status codes and descriptive error responses should be returned for invalid requests and processing failures.

## 7. Security and Reliability

Potential production requirements include request validation, controlled API access, structured logging, error monitoring, and safe handling of scenario and detection data.

Communication failure should not silently convert unknown task status into completed status.

## 8. Technology Stack

- Python
- FastAPI
- REST APIs and JSON
- Existing RESQNET scenario schema
- Integration with the YOLO-based computer-vision module

## 9. Development and Validation Status

The backend must be evaluated independently and then tested with the frontend and computer-vision module.

Document each endpoint, coordination mechanism, and recovery feature as implemented only after the corresponding tests pass.

## 10. Future Enhancements

- Persistent mission-state storage.
- Real-time mission updates.
- Improved conflict resolution after reconnection.
- Drone battery and route-feasibility integration.
- Authentication, monitoring, and deployment support.
- Integration with physical drone platforms.

## Conclusion

The RESQNET backend provides the planned foundation for connecting disaster scenarios, detection evidence, and multi-drone coordination. Its central objective is to support reliable mission-state management and failure-aware search operations within a disaster-response simulation.
