# 🏛️ Nagrik-AI | Intelligent Civic Grievance Portal

> An automated municipal grievance intake and triage platform that routes citizen reports to local governance departments in real time.

---

## 🎯 Problem Statement

Municipal bodies face severe operational bottlenecks in citizen grievance redressal:

1. **Resolution Latency:** Manual ticket triaging delays complaint routing by 48–72 hours, slowing municipal emergency response.
2. **Misclassification & Routing Errors:** Vague citizen reports lead to tickets bouncing between departments (e.g., Public Works vs. Sanitation).
3. **Lack of Operational Visibility:** Municipal leadership lacks unified real-time telemetry to track departmental SLAs, resolution times, and regional issue hotspots.
4. **Poor Citizen Transparency:** Citizens receive minimal feedback or tracking visibility once a grievance is logged.

---

## 💡 The Solution

**Nagrik-AI** streamlines municipal redressal by embedding AI intelligence into the intake and routing pipeline:

* **Automated AI Triage:** Uses natural language processing to evaluate incoming complaints and automatically extract `category`, `priority`, `department`, and `confidence score`.
* **API-Driven Citizen Portal:** A clean, responsive intake dashboard allowing citizens to submit complaints and track live resolution statuses.
* **Backend Dispatch Pipeline:** Synchronizes structured complaint payloads directly to a Flask API and SQLite database for department dispatch.
* **System Telemetry:** Live analytics visualization breaking down complaint volumes by department and emergency priority levels.

---

## 🔄 Data Architecture & Processing Flow

```text
[ Citizen Portal (UI) ]
         │
         │  POST /complaints { citizen_name, citizen_email, complaint_text }
         ▼
[ Flask API Backend ] ──► [ Gemini AI Engine ]
         │                        │
         │ (Store & Query)        │ (Triage Metadata)
         ▼                        ▼
[ SQLite Database ] ◄───── [ Categorized Payload ]
