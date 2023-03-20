{% if cookiecutter.project_category == "Command-Line" -%}
import os
import subprocess
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def cd(p: Path):
    now = Path.cwd()
    try:
        os.chdir(str(p))
        yield
    finally:
        os.chdir(str(now))


def run(cmd: str | list[str], dir: Path, *args, **kwargs) -> subprocess.CompletedProcess:
    with cd(dir):
        return subprocess.run(cmd, check=True, *args, **kwargs)


def test_e2e():
    pwd = Path.cwd()
    run(["pipenv", "run", "dist"], pwd)
    run(
        [
            "pip",
            "install",
            "dist/{{ cookiecutter.project_slug }}-{{ cookiecutter.version }}.tar.gz",
        ],
        pwd,
    )
    r = run(
        ["python", "-m", "{{ cookiecutter.project_slug }}.cli"],
        pwd,
        text=True,
        capture_output=True,
    )
    want = "Please implement {{ cookiecutter.project_slug }}.cli.main\n"
    assert want == r.stdout
{%- endif %}


def test_sample():
    pass
