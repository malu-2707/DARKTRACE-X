\# Autonomous SOC Agent



\## Overview



Autonomous SOC Agent is a security investigation backend designed to ingest SOC telemetry, investigate alerts, correlate evidence, calculate risk, make response decisions, verify actions, reassess incidents, and provide audit visibility.



\## Architecture



SOC Telemetry

↓

Alert Ingestion

↓

Trace ID

↓

Redis Stream

↓

Investigation Orchestrator

↓

Planner

↓

Evidence Selector

↓

Evidence Collection

↓

Evidence Store

↓

Correlation Engine

↓

Scoring Engine

↓

Decision Engine

↓

Risk / Policy Gate

↓

Auto Action / Approval

↓

Response Service

↓

Verification

↓

Reassessment

↓

Audit

↓

WebSocket / Dashboard



\## Technology Stack



\- Python

\- FastAPI

\- Redis Streams

\- SQLAlchemy

\- SQLite

\- Pydantic

\- JWT Authentication

\- WebSocket



\## Security Flow



1\. Alert is ingested.

2\. A Trace ID identifies the investigation.

3\. Alert data is processed through Redis Stream.

4\. Investigation is planned.

5\. Required evidence is selected and collected.

6\. Evidence is correlated.

7\. Risk score is calculated.

8\. Decision engine determines the response.

9\. Risk policy evaluates whether approval is required.

10\. Response is executed or waits for approval.

11\. Response is verified.

12\. Investigation is reassessed.

13\. Audit record is generated.

14\. Dashboard receives the investigation event through WebSocket.



\## Demo Scenario



SSH Brute Force

→ Successful Login

→ Suspicious Process

→ Outbound Connection

→ Risk Scoring

→ BLOCK\_IP Recommendation

→ Analyst Approval

→ Response

→ Verification

→ Audit

→ Dashboard



\## Running the Backend



```powershell

.\\venv\\Scripts\\python.exe -m uvicorn app.main:app --reload

