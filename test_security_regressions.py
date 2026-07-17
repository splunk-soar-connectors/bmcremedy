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
            if "onclick=\"context_menu" in line:
                assert "|escapejs }}" in line, f"unescaped context-menu value in {template.name}"
