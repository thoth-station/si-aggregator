#!/usr/bin/env python3
# si-aggregator
# Copyright(C) 2020 Kevin Postlethwait.
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This file contains functions which aggregate results from thoth security indicators."""

from typing import Dict
from typing import Any

LOW_CON_WEIGHT = 0.25
MED_CON_WEIGHT = 0.5
HI_CON_WEIGHT = 1

LOW_SEV_WEIGHT = 1
MED_SEV_WEIGHT = 10
HI_SEV_WEIGHT = 100


def sample_aggregator(si_bandit_results: Dict[str, Any], si_cloc_results: Dict[str, Any], **kwargs) -> float:
    """Run an example of an aggregator using results from si-cloc and si-bandit."""
    cloc_python = si_cloc_results["result"]["Python"]["code"]
    metrics = si_bandit_results["result"]["metrics"]
    score = 0
    for k, v in metrics:
        sev = (
            LOW_SEV_WEIGHT * v["SEVERITY.LOW"]
            + MED_SEV_WEIGHT * v["SEVERITY.MEDIUM"]
            + HI_SEV_WEIGHT * v["SEVERITY.HIGH"]
        )
        con = (
            LOW_CON_WEIGHT * v["CONFIDENCE.LOW"]
            + MED_SEV_WEIGHT * v["CONFIDENCE.MEDIUM"]
            + HI_CON_WEIGHT * v["CONFIDENCE.HIGH"]
        )
        tot = v["SEVERITY.LOW"] + v["SEVERITY.MEDIUM"] + v["SEVERITY.HIGH"]
        if not tot == 0:
            score = score + (sev * con) / tot

    score = score / (cloc_python * 10)

    return score
