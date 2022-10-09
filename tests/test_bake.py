import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Union

from cookiecutter.utils import rmtree


@contextmanager
def cd(p: Path):
    now = Path.cwd()
    try:
        os.chdir(str(p))
        yield
    finally:
        os.chdir(str(now))


@contextmanager
def bake(cookies, *args, **kwrags):
    r = cookies.bake(*args, **kwrags)
    try:
        yield r
    finally:
        rmtree(str(r.project_path))


def run(
    cmd: Union[str, list[str]], dir: Path, *args, **kwargs
) -> subprocess.CompletedProcess:
    with cd(dir):
        return subprocess.run(cmd, check=True, *args, **kwargs)


def test_bake_and_make(cookies):
    with bake(cookies) as result:
        assert result.exit_code == 0
        assert result.exception is None
        assert result.project_path.is_dir()
        assert result.project_path.name == "python_project_template"
        run(["make", "init"], result.project_path)
        run(["make", "test"], result.project_path)
        run(["make", "dist"], result.project_path)
