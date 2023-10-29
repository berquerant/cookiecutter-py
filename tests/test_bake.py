import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

from cookiecutter.main import cookiecutter


@contextmanager
def cd(p: Path):
    now = Path.cwd()
    try:
        os.chdir(str(p))
        yield
    finally:
        os.chdir(str(now))


def bake(template: str, output_dir: str, *args, **kwargs):
    cookiecutter(
        template=template,
        output_dir=output_dir,
        no_input=True,
        *args,
        **kwargs,
    )


def run(
    cmd: str | list[str], pwd: Path, *args, **kwargs
) -> subprocess.CompletedProcess:
    with cd(pwd):
        return subprocess.run(cmd, check=True, *args, **kwargs)


def check_result(pwd: Path):
    run(["pipenv", "install", "--dev"], pwd)
    scripts = ["ci", "install", "dist"]
    for x in scripts:
        run(["pipenv", "run", x], pwd)


def test_bake_and_make_default():
    template = str(Path(__file__).parent.parent)
    with TemporaryDirectory() as tdir:
        bake(template=template, output_dir=tdir)
        check_result(Path(tdir) / "python_project_template")
