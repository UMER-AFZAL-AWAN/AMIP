# Project State
Date: 2026-08-02

## Current Phase Summary
- Phase 0 (Planning & Setup): Complete
- Phase 1 (Backend Core): Initialized
- Phase 2 (Data Pipeline): Initialized
- Phase 3 (Frontend & AI): Initialized

## Technology Stack
- Backend: .NET 8 (C#)
- Database: PostgreSQL
- Machine Learning: Python, PyTorch
- Inference: ONNX Runtime
- Frontend: React + Vite
- Containerization: Docker Compose

## Architecture Overview
Clean Architecture for the Backend, connected to a PostgreSQL database. ML services run in isolated Python processes/containers communicating via gRPC or REST. Cross-platform inference is handled via ONNX Runtime for edge capabilities. Frontend is a lightweight SPA using React.
