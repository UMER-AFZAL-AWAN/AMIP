# System Architecture

## Overview
The AI Market Intelligence Platform (AMIP) is designed as a modular, scalable application for analyzing market trends using AI.

## Diagram
[Frontend (React/Vite)] <--> [API Gateway (.NET)] <--> [Backend Core (.NET)] <--> [PostgreSQL Database]
                                                        |
                                                        v
                                              [ML Service (Python/PyTorch/ONNX)]

## Components
1. **Frontend**: React SPA for user dashboard and data visualization.
2. **Backend**: .NET 8 Web API implementing Clean Architecture principles (Core, Infrastructure, Web).
3. **Database**: PostgreSQL for relational data storage (users, market data, analysis results).
4. **AI Module**: Python-based microservice for heavy training and inference, utilizing PyTorch and ONNX Runtime.

## Data Flow
User requests analysis -> Frontend calls API -> Backend validates and stores request -> Backend triggers ML Service -> ML Service processes data and returns results via ONNX -> Backend updates DB -> Frontend polls/receives update.

## Contracts
RESTful JSON APIs between Frontend and Backend. gRPC or HTTP for internal Backend <-> ML Service communication.
