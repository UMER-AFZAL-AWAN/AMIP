# AI Market Intelligence Platform (AMIP)

An autonomous artificial intelligence system capable of understanding financial markets through historical experience and real-time observation.

## Project Vision

The system learns market behavior from historical data, discovers hidden patterns, understands different market regimes, identifies similarities between current and historical situations, classifies current market conditions, predicts future probabilities, quantifies uncertainty, evaluates its own mistakes, and improves through continuous learning.

## Architecture Overview

```
                    Market Intelligence Platform

                         User Interface (React Dashboard)
                               |
                     Decision & Analytics Layer (.NET 8 API)
                               |
               AI Intelligence Orchestration Layer (.NET 8)
                               |
         ------------------------------------------------
         |                     |                        |
  Market Classification   Prediction Engine     Pattern Discovery
   (Python/ONNX)          (Python/ONNX)          (Python/ONNX)
         |                     |                        |
         ------------------------------------------------
                               |
                      Feature Engineering Layer (Python)
                               |
                      Data Processing Layer (.NET 8)
                               |
         ------------------------------------------------
         |                     |                        |
  Historical Data        Real-Time Data          External Data
  (Binance REST)       (Binance WebSocket)      (Future)
         |                     |                        |
         ------------------------------------------------
                               |
                          Data Storage
                               |
                          PostgreSQL
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend Services | C# / .NET 8 |
| Database | PostgreSQL 16 |
| ML Training | Python 3.11+ / PyTorch |
| ML Baselines | Scikit-learn, XGBoost, LightGBM |
| Inference | ONNX Runtime |
| Frontend | React + Vite |
| Containerization | Docker Compose |

## Project Structure

```
AI-Market-Intelligence-Platform/
├── Project_Context/          # Project state, tasks, handoffs
├── Documentation/            # Architecture docs, research journal
├── Conversation_Logs/        # Session recordings
├── User_Requirements/        # Requirements tracking
├── Decisions/                # Architecture decision records
├── Research/                 # Research notes and papers
├── Experiments/              # ML experiment tracking
├── Source_Code/              # All application source code
│   ├── Backend/              # .NET 8 solution
│   ├── ML/                   # Python ML pipeline
│   └── Frontend/             # React dashboard
├── Database/                 # Schemas, migrations, seeds
├── Models/                   # ML model artifacts
├── Data/                     # Raw, processed, feature data
├── Dependencies/             # Project-local dependencies
├── Tools/                    # Utility scripts
├── Scripts/                  # Build & deployment scripts
├── Tests/                    # Test suites
└── Deployment/               # Docker & deployment configs
```

## Quick Start

### Prerequisites
- .NET 8 SDK
- Python 3.11+
- Docker & Docker Compose
- Node.js 18+

### 1. Start Infrastructure
```bash
cd Deployment
docker-compose up -d
```

### 2. Run Database Migrations
```bash
cd Source_Code/Backend
dotnet ef database update
```

### 3. Start Backend
```bash
cd Source_Code/Backend/AMIP.Api
dotnet run
```

### 4. Start Frontend
```bash
cd Source_Code/Frontend
npm install
npm run dev
```

### 5. Run ML Pipeline
```bash
cd Source_Code/ML
pip install -r requirements.txt
python -m amip.pipeline.run
```

## Development Phases

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 0 | Project Foundation | ✅ Complete |
| Phase 1 | Market Data Infrastructure | 🔨 Building |
| Phase 2 | Data Engineering Pipeline | 🔨 Building |
| Phase 3 | Feature Engineering Platform | 🔨 Building |
| Phase 4 | Baseline Intelligence Models | 🔨 Building |
| Phase 5 | Market Regime Intelligence | 🔨 Building |
| Phase 6 | Pattern Discovery System | 🔨 Building |
| Phase 7 | Advanced Prediction Models | 🔨 Building |
| Phase 8 | Backtesting Framework | 🔨 Building |
| Phase 9 | Decision Intelligence | 🔨 Building |
| Phase 10 | Real-Time Intelligence | 🔨 Building |
| Phase 11 | Continuous Learning | 🔨 Building |

## License

Private — All rights reserved.
