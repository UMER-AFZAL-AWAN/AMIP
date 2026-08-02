# Changelog

All notable changes to the AI Market Intelligence Platform will be documented in this file.

## [0.1.0] - 2026-08-02

### Added
- Initial project structure and documentation system
- Docker Compose configuration for PostgreSQL and pgAdmin
- Database migration scripts (initial schema)
- .NET 8 backend solution with Clean Architecture
  - Domain models for market data, features, predictions
  - Binance REST API connector for historical data
  - Binance WebSocket connector for real-time data
  - Data validation pipeline
  - PostgreSQL repository layer with EF Core
  - Feature storage service
  - Orchestration service
  - ASP.NET Core API endpoints
- Python ML pipeline
  - Feature engineering system (price, trend, momentum, volatility, volume, market structure, time)
  - Baseline models (Logistic Regression, Random Forest, XGBoost, LightGBM)
  - Market regime classifier
  - Pattern discovery engine (embeddings, clustering, similarity search)
  - Advanced prediction models (LSTM, Transformer)
  - Backtesting framework with walk-forward testing
  - Self-evaluation and model monitoring system
  - ONNX export pipeline
  - Experiment tracking system
- React + Vite frontend dashboard
  - Market state visualization
  - Prediction display with confidence intervals
  - Model performance charts
  - Regime classification view
  - Pattern similarity visualization
- Complete documentation suite
  - Architecture documentation
  - Decision records
  - Research journal template
  - Model card templates
