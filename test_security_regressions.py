import json
from pathlib import Path


ROOT = Path(__file__).parent


def test_tls_verification_defaults_to_enabled():
    manifest = json.loads((ROOT / "bmcremedy.json").read_text())
    source = (ROOT / "bmcremedy_connector.py").read_text()

    assert manifest["configuration"]["verify_server_cert"]["default"] is True
    assert "BMCREMEDY_CONFIG_SERVER_CERT, True" in source
    assert "BMCREMEDY_CONFIG_SERVER_CERT, False" not in source
