# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.
#
# This source code is licensed under the BSD license found in the
# LICENSE file in the root directory of this source tree.
import subprocess
from pathlib import Path

# TODO: consolidate with the code in build_conda.py
THIS_PATH = Path(__file__).resolve()
version = (THIS_PATH.parents[1] / "version.txt").read_text().strip()


def is_exact_version() -> bool:
    """
    Return whether we are at an exact version (namely the version variable).
    """
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--exact-match", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:  # no tag
        return False

    if not tag.startswith("v"):
        return False

    assert (
        version == tag[1:]
    ), f"The version in version.txt ({version}) does not match the given tag ({tag})"
    return True


def get_dev_version() -> str:
    num_commits = subprocess.check_output(
        ["git", "rev-list", "--count", "HEAD"], text=True
    ).strip()
    return f"{version}.dev{num_commits}"


if __name__ == "__main__":
    if is_exact_version():
        print(version, end="")
    else:
        print(get_dev_version(), end="")
