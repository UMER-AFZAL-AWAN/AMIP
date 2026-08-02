# Getting Started

## Prerequisites
- Docker & Docker Compose
- .NET 8 SDK
- Python 3.10+
- Node.js 20+

## Setup Steps
1. Clone the repository.
2. Run `docker-compose up -d` to start the PostgreSQL database and other infrastructural dependencies.
3. In the backend directory, run `dotnet restore` and `dotnet run`.
4. In the frontend directory, run `npm install` and `npm run dev`.
5. For the ML service, create a virtual environment, install requirements, and run the Python service.
