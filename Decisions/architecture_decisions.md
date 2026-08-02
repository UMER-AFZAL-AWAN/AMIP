# Architecture Decision Records (ADRs)

## ADR-001: Clean Architecture for .NET Backend
- **Decision**: Adopt Clean Architecture.
- **Reason**: Separation of concerns, testability, and independence from frameworks.
- **Alternatives**: MVC monolithic approach, vertical slice architecture.
- **Trade-offs**: Higher initial complexity and boilerplate.
- **Date**: 2026-08-02
- **Impact**: Backend will be split into Core, Infrastructure, Application, and Web API projects.

## ADR-002: PostgreSQL as Primary Database
- **Decision**: Use PostgreSQL.
- **Reason**: Robust, open-source, excellent support for JSON and spatial data, widely adopted.
- **Alternatives**: SQL Server, MySQL, MongoDB.
- **Trade-offs**: Potential learning curve if team is heavily accustomed to SQL Server.
- **Date**: 2026-08-02
- **Impact**: EF Core will be configured with the Npgsql provider.

## ADR-003: Python/PyTorch for ML Pipeline
- **Decision**: Use Python and PyTorch for ML model development.
- **Reason**: Industry standard for deep learning, rich ecosystem.
- **Alternatives**: TensorFlow, scikit-learn only.
- **Trade-offs**: Requires maintaining a separate Python environment and microservice.
- **Date**: 2026-08-02
- **Impact**: CI/CD pipelines must support Python.

## ADR-004: ONNX Runtime for Cross-Platform Inference
- **Decision**: Export models to ONNX and run inference using ONNX Runtime.
- **Reason**: High performance, decoupled from training framework, allows running inference efficiently on different targets.
- **Alternatives**: TorchScript, PyTorch natively in prod.
- **Trade-offs**: Overhead of model conversion, potential unsupported operations during export.
- **Date**: 2026-08-02
- **Impact**: Model export step required in training pipeline.

## ADR-005: React + Vite for Frontend Dashboard
- **Decision**: Use React with Vite build tool.
- **Reason**: Fast development iteration, huge ecosystem, declarative UI.
- **Alternatives**: Angular, Vue, Next.js.
- **Trade-offs**: SPA SEO limitations (acceptable for a dashboard).
- **Date**: 2026-08-02
- **Impact**: Frontend will be built as an SPA and hosted via Nginx or standard static host.

## ADR-006: Docker Compose for Local Development
- **Decision**: Use Docker Compose to orchestrate local services.
- **Reason**: Replicable environments, easy onboarding.
- **Alternatives**: Local native installations, Kubernetes (minikube).
- **Trade-offs**: Overhead of Docker desktop resource usage.
- **Date**: 2026-08-02
- **Impact**: A `docker-compose.yml` must be maintained with all backing services.
