
# RESQNET — Backend Module

## Overview
The RESQNET backend is designed to connect the mission-control dashboard with disaster scenarios, drone coordination logic, and computer-vision detection results.

## Core Responsibilities
- Provide API endpoints for disaster scenarios and mission data.
- Process and manage drone task assignments and search progress.
- Support area prioritization using scenario priority, deadlines, and detection evidence.
- Receive person-detection results from the computer-vision module.
- Support synchronization and recovery of unfinished tasks during communication failures.

## Technology Stack
- Python
- FastAPI (planned API integration)
- JSON-based scenario data
- REST API architecture

## Integration Workflow
1. Receive scenario and mission requests from the frontend.
2. Process scenario information and coordination rules.
3. Connect detection results to the relevant drone and search area.
4. Update task status and provide responses to the frontend.

## Development Status
The backend API and computer-vision integration are intended to connect the individual modules into a unified disaster-response simulation. Features should be marked as implemented only after they have been tested.

## Objective
Build a modular backend that supports resilient multi-drone coordination and reliable information exchange during disaster-response simulations.
