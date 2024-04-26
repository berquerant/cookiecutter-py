import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import glob
import yaml

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
        print(f"[run] {cmd}")
        return subprocess.run(cmd, check=True, *args, **kwargs)


def check_result(pwd: Path):
    run(["pipenv", "install", "--dev"], pwd)
    run(["pipenv", "check"], pwd)
    scripts = ["ci", "install", "dist"]
    for x in scripts:
        run(["pipenv", "run", x], pwd)

    with cd(pwd):
        print("[check] all cookiecutter has been replaced")
        r = subprocess.run(
            ["git", "grep", "cookiecutter"], capture_output=True, text=True
        )
        assert len(r.stdout) == 0
        print("[check] valid yaml")
        for yaml_file in glob.glob(".github/**/*.yml", recursive=True):
            with open(yaml_file) as f:
                print(f"[yaml] {yaml_file}")
                yaml.safe_load(f)


def test_bake_and_make_default():
    template = str(Path(__file__).parent.parent)
    with TemporaryDirectory() as tdir:
        bake(template=template, output_dir=tdir)
        check_result(Path(tdir) / "python_project_template")
