# RESQNET — Disaster Area Priority Testing

## Overview
The priority-testing module evaluates how RESQNET ranks disaster-affected areas for search operations. It focuses on combining person-detection evidence, existing scenario priorities, task deadlines, and search progress to identify areas requiring urgent attention.

## Priority Evaluation Factors
- **Person-detection evidence:** Number and confidence of potential-person detections in an area.
- **Scenario priority:** Importance assigned to the area in the disaster scenario.
- **Task deadline:** Urgency based on the remaining time before a task deadline.
- **Search progress:** Whether the area is unsearched, partially searched, or completed.
- **Coordination status:** Whether a task is unassigned, in progress, or awaiting reassignment.

## Proposed Priority Scoring Model
A configurable weighted scoring model can be used to rank eligible areas:

\[
P_i = w_dD_i + w_sS_i + w_tT_i + w_pU_i
\]

Where:

- \(P_i\): Priority score of area \(i\).
- \(D_i\): Normalized person-detection evidence.
- \(S_i\): Normalized scenario priority.
- \(T_i\): Normalized deadline urgency.
- \(U_i\): Unsearched-area factor.
- \(w_d,w_s,w_t,w_p\): Weights assigned to each factor.

The weights should be selected and validated through simulation. Completed areas should normally be excluded from new search assignments, while battery limits, drone availability, obstacles, and no-fly zones must be checked before dispatch.

## Priority Testing Scenarios

### 1. Detection-Based Priority
Verify that credible potential-person detections increase an eligible area's priority according to the configured scoring rules.

### 2. Deadline-Based Priority
Check whether areas with more urgent deadlines receive higher priority when other conditions are comparable.

### 3. Search-Progress Validation
Ensure completed areas are not repeatedly assigned and unfinished areas remain eligible for consideration.

### 4. Conflicting Priorities
Test scenarios where one area has strong detection evidence and another has a more urgent deadline. Confirm that the configured weights produce the expected ranking.

### 5. Resource and Constraint Validation
Verify that high-priority areas are assigned only when a suitable drone and feasible route are available.

### 6. Communication-Failure Recovery
Confirm that unfinished high-priority tasks can be reconsidered after coordination interruptions without creating duplicate assignments.

## Evaluation Metrics
- Correctness of priority rankings.
- Number of duplicate assignments.
- Number of unfinished areas left unattended.
- Time taken to select the next eligible area.
- Search coverage and task completion rate.

## Expected Outcome
Priority testing should demonstrate that RESQNET ranks eligible disaster areas consistently, incorporates new detection evidence, and respects task status and operational constraints.

## Scope and Limitations
The scoring formula is a proposed rule-based approach. It must be implemented and tested against defined scenarios before its effectiveness can be claimed. A detection is only a potential sighting and does not confirm a survivor or determine rescue urgency by itself.
