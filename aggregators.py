from typing import Dict
from typing import Any

LOW_CON_WEIGHT = 0.25
MED_CON_WEIGHT = 0.5
HI_CON_WEIGHT = 1

LOW_SEV_WEIGHT = 1
MED_SEV_WEIGHT = 10
HI_SEV_WEIGHT = 100

def sample_aggregator(si_bandit_results: Dict[str, Any], si_cloc_results: Dict[str, Any], *) -> float:
    cloc_python = si_cloc_results["result"]["Python"]["code"]
    metrics = si_bandit_results["result"]["metrics"]
    score = 0
    for k, v in metrics:
        sev = LOW_SEV_WEIGHT*v["SEVERITY.LOW"] + MED_SEV_WEIGHT*v["SEVERITY.MEDIUM"] + HI_SEV_WEIGHT*v["SEVERITY.HIGH"]
        con = LOW_CON_WEIGHT*v["CONFIDENCE.LOW"] + MED_SEV_WEIGHT*v["CONFIDENCE.MEDIUM"] + HI_CON_WEIGHT*v["CONFIDENCE.HIGH"]
        tot = v["SEVERITY.LOW"] + v["SEVERITY.MEDIUM"] + v["SEVERITY.HIGH"]
        if not tot == 0:
            score = score + (sev * con)/tot
    
    score = score/(cloc_python * 10)

    return score