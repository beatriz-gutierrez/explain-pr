import os
import subprocess
import sys

CODE_SOURCE_PATH = os.path.join("explain_pr")


def test_mypy_compliance() -> None:

    mypy_location = "which mypy"  # Unix-like OS
    if os.name == "nt":  # Windows OS
        mypy_location = "where mypy"

    mypy_binary = (
        subprocess.check_output(mypy_location, shell=True, stderr=sys.stderr).decode("ascii").replace("\n", "")
    )

    FILES_PATH = " ".join(
        [
            CODE_SOURCE_PATH,
        ]
    )
    MYPY = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "mypy.ini",
    )

    result = subprocess.call(
        f"{mypy_binary} --config-file={MYPY} --explicit-package-bases {FILES_PATH}",
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    assert result == 0
