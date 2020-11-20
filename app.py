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

"""This is the main script of si-cloc which counts lines of code."""

import click

import logging
from typing import Optional, Dict, Any
import json
from datetime import datetime
import os

from thoth.analyzer import print_command_result
from thoth.common import init_logging
from thoth.analyzer import __version__ as __analyzer__version__
from thoth.common import __version__ as __common__version__
from thoth.report_processing import __version__ as __report_processing__version__

import aggregators

init_logging()

__version__ = "0.1.6"
__title__ = "si-aggregator"


__service_version__ = (
    f"{__version__}+"
    f"analyzer.{__analyzer__version__}.common.{__common__version__}."
    f"report_processing.{__report_processing__version__}"
)

_LOGGER = logging.getLogger(__title__)
_LOGGER.info("SI Aggregator v%s", __service_version__)


def _gen_metadata_on_err() -> Dict[str, Any]:
    to_ret = dict()
    to_ret["document_id"] = os.getenv("THOTH_DOCUMENT_ID",)  # fail here, we need a document ID to sync properly
    to_ret["datetime"] = str(datetime.utcnow())
    return to_ret


@click.command()
@click.pass_context
@click.option(
    "--output",
    "-o",
    type=str,
    default="-",
    envvar="THOTH_SI_AGGREGATOR_OUTPUT",
    help="Output file to store results to (WARNING: if nothing is provided it prints only) .",
)
@click.option(
    "--package-name",
    "-n",
    required=True,
    type=str,
    envvar="THOTH_SI_AGGREGATOR_PACKAGE_NAME",
    help="Name of package bandit is being run on.",
)
@click.option(
    "--package-version",
    type=str,
    required=True,
    envvar="THOTH_SI_AGGREGATOR_PACKAGE_VERSION",
    help="Version to be evaluated.",
)
@click.option(
    "--package-index",
    type=str,
    default="https://pypi.org/simple",
    envvar="THOTH_SI_AGGREGATOR_PACKAGE_INDEX",
    help="Which index is used to find package.",
)
@click.option(
    "--si-bandit-results",
    type=str,
    required=True,
    envvar="THOTH_SI_AGGREGATOR_SI_BANDIT_RESULTS",
    help="Output from si-bandit to be used.",
)
@click.option(
    "--si-cloc-results",
    type=str,
    required=True,
    envvar="THOTH_SI_AGGREGATOR_SI_CLOC_RESULTS",
    help="Output from si-cloc to be used.",
)
@click.option(
    "--aggregation-func",
    type=str,
    required=True,
    envvar="THOTH_SI_AGGREGATOR_FUNCTION",
    help="Function name to be used as aggregation function.",
)
@click.option("--no-pretty", is_flag=True, help="Do not print results nicely.")
def si_aggregator(
    click_ctx,
    output: Optional[str],
    package_name: str,
    package_version: Optional[str],
    package_index: Optional[str],
    si_bandit_results: str,
    si_cloc_results: str,
    aggregation_func: str,
    no_pretty: bool,
) -> None:
    """Run the cli for si-aggregator."""
    agg_func = getattr(aggregators, aggregation_func)
    if agg_func is None:
        raise NotImplementedError(f"{aggregation_func} aggregation function not implemented yet.")

    with open(si_bandit_results, "r") as f:
        si_bandit_results = json.load(f)
    with open(si_cloc_results, "r") as f:
        si_cloc_results = json.load(f)

    out = agg_func(si_bandit_results=si_bandit_results, si_cloc_results=si_cloc_results)

    if out.get("error", False):
        out["metadata"] = _gen_metadata_on_err()

    out["bandit_results"] = si_bandit_results
    out["cloc_results"] = si_cloc_results

    print_command_result(
        click_ctx=click_ctx,
        result=out,
        analyzer=__title__,
        analyzer_version=__version__,
        output=output,
        duration=None,
        pretty=not no_pretty,
    )


__name__ == "__main__" and si_aggregator()
