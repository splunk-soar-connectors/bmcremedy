# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
from pathlib import Path


ROOT = Path(__file__).parent


def test_tls_verification_defaults_to_enabled():
    manifest = json.loads((ROOT / "bmcremedy.json").read_text())
    source = (ROOT / "bmcremedy_connector.py").read_text()

    assert manifest["configuration"]["verify_server_cert"]["default"] is True
    assert "BMCREMEDY_CONFIG_SERVER_CERT, True" in source
    assert "BMCREMEDY_CONFIG_SERVER_CERT, False" not in source


def test_widget_context_menu_values_are_escaped_for_javascript():
    for template in ROOT.glob("bmcremedy_*.html"):
        for line in template.read_text().splitlines():
            if 'onclick="context_menu' in line:
                assert "|escapejs }}" in line, f"unescaped context-menu value in {template.name}"


def test_ticket_pagination_has_an_absolute_result_ceiling():
    source = (ROOT / "bmcremedy_connector.py").read_text()
    constants = (ROOT / "bmcremedy_consts.py").read_text()

    assert "BMCREMEDY_MAX_RESULTS = 10000" in constants
    assert "result_limit = min(max_results, consts.BMCREMEDY_MAX_RESULTS)" in source
    assert "items_list[:result_limit]" in source


def test_apppassword_is_removed_before_action_result_storage():
    source = (ROOT / "bmcremedy_connector.py").read_text()
    manifest = (ROOT / "bmcremedy.json").read_text()

    assert 'str(key).casefold() != "apppassword"' in source
    assert source.count("add_data(_redact_sensitive_fields(") == 2
    assert ".values.AppPassword" not in manifest
