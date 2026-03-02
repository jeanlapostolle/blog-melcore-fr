import os
import shutil
from pathlib import Path


def copy_static(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def write_html(build_path, html):
    os.makedirs(build_path.parent, exist_ok=True)
    with open(build_path, "w+") as f:
        f.write(html)
