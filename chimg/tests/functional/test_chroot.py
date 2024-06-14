#  SPDX-FileCopyrightText: 2024 Thomas Bechtold <thomasbechtold@jpberlin.de>
#  SPDX-License-Identifier: GPL-3.0-or-later

import os
import pathlib
import pytest
import subprocess
from functools import partial
from chimg import chroot
from chimg import context


curdir = pathlib.Path(__file__).parent.resolve()


def _check_file_exists(file_path: pathlib.Path, chroot_path: pathlib.Path):
    """
    check that a given file exists
    """
    assert os.path.exists(chroot_path / file_path)


def _check_deb_installed(deb_name: str, chroot_path: pathlib.Path):
    """
    check that a given deb package is installed
    """
    res = subprocess.run(["/usr/sbin/chroot", chroot_path.as_posix(), "dpkg-query", "-W", deb_name])
    assert res.returncode == 0, f"deb package {deb_name} is not installed"


@pytest.mark.parametrize(
    "config_path,checks",
    [
        [
            "configs/kernel-only.yaml",
            [
                (partial(_check_file_exists, pathlib.Path("/boot/vmlinuz"))),
                (partial(_check_deb_installed, "linux-aws")),
            ],
        ],
    ],
)
@pytest.mark.realchroot
def test_config(chroot_mmdebstrap_dir, config_path, checks):
    """
    Test different configuration examples from the functional/configs directory
    """
    ctx = context.Context(conf_path=curdir / config_path, chroot_path=chroot_mmdebstrap_dir)
    cr = chroot.Chroot(ctx)
    cr.apply()
    # do checks
    for check in checks:
        check(chroot_mmdebstrap_dir)
