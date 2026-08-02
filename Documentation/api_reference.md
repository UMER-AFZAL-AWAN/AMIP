# API Reference

## Endpoints

### GET /api/v1/health
Returns system health status.
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-08-02T12:00:00Z"
}
```

### POST /api/v1/analysis
Triggers a new market analysis job.
**Request:**
```json
{
  "market": "tech",
  "parameters": {}
}
```
