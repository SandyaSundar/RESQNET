# RESQNET — Integration Testing Framework

## Overview
The integration-testing module validates the interaction between the RESQNET frontend, backend APIs, computer-vision predictions, and drone coordination logic. Its primary goal is to ensure that information flows correctly between modules and that failures are handled consistently during disaster-response simulations.

## Testing Objectives
- Validate communication between frontend and backend.
- Verify scenario JSON loading and API response formats.
- Confirm that detection results are linked to the correct drone and search area.
- Test area-priority updates when new detection evidence becomes available.
- Verify task assignment, completion tracking, and unfinished-task reassignment.
- Evaluate system behaviour during communication loss and reconnection.

## Major Test Scenarios

### 1. API Integration
Check valid requests, response structures, error handling, and scenario-data consistency.

### 2. Computer-Vision Integration
Verify that detected-person records, confidence scores, bounding-box coordinates, and verification statuses are transferred correctly.

### 3. Priority Integration
Confirm that changes in detection evidence, task deadlines, and search progress produce the expected priority updates.

### 4. Communication-Failure Testing
Simulate communication interruptions and verify that unfinished tasks are retained and handled according to the coordination rules.

### 5. End-to-End Testing
Select a disaster-affected area in the frontend, process its image, pass the resulting detections through the backend, and verify that the updated information appears in the mission-control interface.

## Testing Methodology
Perform unit tests for individual components, API tests for service communication, and end-to-end tests for complete workflows. Record test inputs, expected outputs, actual outputs, and failures.

## Success Criteria
- Correct transfer of scenario and detection data.
- Consistent priority calculations across modules.
- Correct association of detections with drones and areas.
- Reliable handling of incomplete tasks during simulated failures.
- No silent loss of mission state during synchronization.

## Objective
Establish a verifiable integration workflow that improves the reliability and consistency of the RESQNET system.
