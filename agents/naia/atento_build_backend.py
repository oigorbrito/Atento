from __future__ import annotations

import zipfile
from pathlib import Path

NAME = "atento-naia"
VERSION = "0.0.0"


def _dist_info() -> str:
    return f"{NAME.replace('-', '_')}-{VERSION}.dist-info"


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    wheel_dir = Path(wheel_directory)
    wheel_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{NAME.replace('-', '_')}-{VERSION}-py3-none-any.whl"
    target = wheel_dir / filename
    dist_info = _dist_info()
    with zipfile.ZipFile(target, "w") as zf:
        for path in Path("atento_naia").rglob("*.py"):
            zf.write(path, path.as_posix())
        zf.writestr(
            f"{dist_info}/METADATA",
            "Metadata-Version: 2.1\n"
            f"Name: {NAME}\n"
            f"Version: {VERSION}\n",
        )
        zf.writestr(
            f"{dist_info}/WHEEL",
            "Wheel-Version: 1.0\nGenerator: atento-topology-probe\n"
            "Root-Is-Purelib: true\nTag: py3-none-any\n",
        )
        zf.writestr(f"{dist_info}/RECORD", "")
    return filename
