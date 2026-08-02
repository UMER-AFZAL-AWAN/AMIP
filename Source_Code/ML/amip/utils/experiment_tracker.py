from typing import Dict, Any
import datetime
import json

class ExperimentTracker:
    def __init__(self):
        # In a real scenario, this would write to the DB.
        self.experiments = []
        
    def log_experiment(self, model_name: str, parameters: Dict[str, Any], metrics: Dict[str, float]) -> int:
        exp = {
            'id': len(self.experiments) + 1,
            'timestamp': datetime.datetime.now().isoformat(),
            'model': model_name,
            'parameters': parameters,
            'metrics': metrics
        }
        self.experiments.append(exp)
        # Placeholder for DB insert
        # print(f"Logged experiment: {json.dumps(exp)}")
        return exp['id']
