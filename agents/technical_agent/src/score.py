# agents/technical_agent/src/score.py

def calculate_score(matched: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((matched / total) * 100, 2)
