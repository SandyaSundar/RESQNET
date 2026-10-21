# RESQNET
### Resilient Multi-Agent Drone Coordination for Disaster Response

> **Building resilient, simulation-based drone coordination for disaster-response scenarios.**

RESQNET is a simulation-based disaster-response platform designed to study how multiple autonomous drone agents can coordinate search operations when communication networks become unreliable or fail.

The project explores centralized, decentralized, and hybrid coordination strategies under simulated disaster conditions. By combining multi-agent simulation, communication-failure modelling, search-area prioritization, and computer-vision-based candidate detections, RESQNET aims to evaluate mission continuity, search efficiency, and recovery performance in challenging environments.

**Project:** DEXATHON 2026  
**Status:** Under Development  
**Category:** Multi-Agent Systems · Disaster Response · Simulation · Computer Vision

---

## 1. Problem Statement

During disasters, communication infrastructure may become unreliable or unavailable, making coordinated search operations difficult. Drone teams can experience incomplete area coverage, duplicated assignments, delayed recovery, and inconsistent mission states.

Centralized coordination provides unified control but can become vulnerable when the controller or communication network fails. Decentralized coordination offers greater local autonomy but introduces challenges in task allocation, coordination, and state consistency.

RESQNET addresses these challenges by providing a simulation environment to implement, compare, and evaluate centralized, decentralized, and hybrid drone-coordination strategies under controlled failure scenarios.

## 2. Our Solution

RESQNET combines a multi-agent simulation engine with adaptive coordination logic and disaster-area assessment.

The platform is designed to:

- Simulate multiple drones searching a grid-based disaster environment.
- Allocate search tasks and track mission progress.
- Model communication degradation, network interruptions, and controller failures.
- Evaluate coordination strategies under identical simulation conditions.
- Prioritize search sectors using disaster-area features and risk indicators.
- Integrate computer-vision outputs as potential person or obstacle detections.
- Measure coverage, task completion, recovery time, coordination conflicts, and communication overhead.

The initial implementation focuses on simulation and measurable evaluation rather than physical drone deployment.

## 3. Key Features

### Multi-Agent Drone Simulation
Represent each drone as an independent agent with its own position, operational state, assigned task, and coordination responsibilities.

### Three Coordination Strategies
- **Centralized:** A central mission planner assigns tasks and coordinates drone activity.
- **Decentralized:** Individual agents make local decisions and coordinate without depending entirely on a central controller.
- **Hybrid:** Centralized planning is combined with local autonomy and recovery mechanisms.

### Communication and Failure Simulation
Introduce controlled communication degradation, packet loss, latency, dead zones, and controller failures to study how each strategy responds.

### Disaster-Area Assessment
Visualize searched, unexplored, in-progress, blocked, and high-priority areas to make simulated mission progress easier to understand.

### Search-Sector Prioritization
Rank search areas using scenario features and risk indicators. Predicted priorities will be distinguishable from fixed scenario inputs.

### Computer-Vision Integration
Display candidate detections with their labels, confidence scores, bounding boxes, and verification status. A model prediction is not treated as a confirmed rescue.

### Performance Evaluation
Compare strategies using consistent scenarios, initial conditions, and failure settings to produce reproducible results.

## 4. System Architecture

The planned system follows a modular architecture.

```text
                RESQNET PLATFORM
                       |
          +------------+------------+
          |                         |
     React Frontend            FastAPI Backend
          |                         |
     Live Map UI           Scenario Management
     Mission Dashboard     Simulation Engine
     Metrics & Results     Coordination Engine
          |                         |
          +------------+------------+
                       |
             Multi-Agent Simulation
                       |
       +---------------+---------------+
       |               |               |
   Centralized     Decentralized      Hybrid
   Coordination    Coordination    Coordination
                       |
             Failure Injection
                       |
       +---------------+---------------+
       |               |               |
   Area Priority   Candidate CV     Mission Metrics
    Prediction      Detections      & Evaluation
```

The architecture is a development plan. Components will be integrated incrementally as their interfaces are established.

## 5. Technology Stack

The planned technology stack is:

| Component | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| UI styling | Tailwind CSS |
| Map visualization | Leaflet / React Leaflet |
| Charts | Recharts |
| Backend API | Python, FastAPI |
| Data validation | Pydantic |
| Simulation engine | Custom Python grid-based simulator |
| Computer vision | PyTorch and a compatible pretrained vision model |
| Priority prediction | Rule-based baseline, with ML evaluated where appropriate |
| Database | PostgreSQL; PostGIS if spatial database features are required |
| Testing | pytest and API integration tests |
| Version control | Git and GitHub |

Technology choices may be refined during implementation based on integration requirements and available development time.

## 6. Simulation Environment

The initial scenario dataset contains three prepared grid-based environments:

- **Earthquake:** Infrastructure damage, blocked areas, and communication dead zones.
- **Cyclone:** Restricted areas and disrupted communication conditions.
- **Flood:** Flood-related obstacles, restricted cells, and designated bridge locations.

Each scenario uses a 20 × 20 grid with defined base locations, search tasks, candidate detections, zone priorities, and initial communication parameters.

The scenario values are synthetic test parameters, not validated real-world disaster measurements. The simulator will use explicit rules to determine movement, task assignment, communication failures, recovery, and mission outcomes.

## 7. Evaluation Metrics

RESQNET is designed to compare coordination strategies using measurable outcomes.

| Metric | Purpose |
|---|---|
| Area coverage | Measures how much of the eligible search area has been searched |
| Task completion rate | Measures the proportion of assigned tasks completed |
| Recovery time | Measures the time needed to resume effective coordination after a failure |
| Duplicate assignments | Tracks conflicting or redundant task ownership |
| Communication overhead | Measures simulated communication activity |
| Safety violations | Counts explicitly defined simulated operational violations |
| State convergence | Measures how quickly agents reconcile mission state after connectivity returns |

Experiments will use comparable conditions and, where appropriate, repeated random seeds. Results will be reported from actual simulation runs rather than assumed improvements.

## 8. Development Roadmap

- [ ] Establish the repository structure and development workflow.
- [ ] Build the FastAPI backend skeleton and health-check endpoint.
- [ ] Validate and load the disaster scenario configuration files.
- [ ] Define drone, task, grid, and simulation data contracts.
- [ ] Implement grid movement, obstacles, and mission-state tracking.
- [ ] Implement centralized, decentralized, and hybrid coordination.
- [ ] Add communication degradation and failure injection.
- [ ] Integrate search-sector prioritization.
- [ ] Integrate computer-vision candidate detections.
- [ ] Build the frontend map and mission dashboard.
- [ ] Run comparative experiments and generate evaluation reports.
- [ ] Test end-to-end integration and document limitations.

## 9. Repository Structure

The repository is organized around independently developed modules.

```text
RESQNET/
├── frontend/                 # Web interface and map visualization
├── backend/                  # API, simulation and coordination
├── computer-vision/          # Vision model integration
├── priority-model/           # Search-sector prioritization
├── datasets/                 # Dataset documentation and permitted assets
├── scenarios/                # Disaster scenario configurations
├── docs/                     # Architecture and API contracts
├── tests/                    # Testing and evaluation support
├── .gitignore
└── README.md
```

The directory structure will evolve as the implementation progresses. Large datasets, generated artifacts, model weights, and sensitive configuration files should not be committed without checking repository policies and file-size constraints.

## 10. Team Collaboration

RESQNET is developed collaboratively using Git and GitHub.

The team uses separate working branches for:

- Backend and simulation
- Frontend and map visualization
- Computer vision
- Search-priority prediction
- Scenario data and dataset documentation
- Integration, testing, and evaluation

Changes are developed in feature branches and submitted through pull requests. The `main` branch is reserved for reviewed, integrated code.

Shared API schemas, scenario contracts, and module interfaces will be documented to reduce integration conflicts.

## 11. Expected Impact

RESQNET aims to provide a reproducible environment for understanding the strengths and limitations of different multi-agent coordination strategies during simulated disaster response.

Its expected contributions include:

- A controlled environment for testing communication and controller failures.
- Comparative evidence about mission continuity and recovery.
- Better visibility into search coverage and task-allocation conflicts.
- Integration of area-priority estimates and computer-vision candidate detections.
- A modular foundation for future research into resilient autonomous coordination
