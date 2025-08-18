# encoding: utf-8

"""
Test module for ``rcontainer.sif`` singularity build
or ``rcontainer`` dockerfile build

In case ``singularity`` is unavailable, the test function(s) should fall
back to ``docker``.
"""

import os
import subprocess
import tempfile


# Check that (1) singularity or apptainer executables exist,
# and (2) if not, check for docker.
# If neither are found, tests will fall back to plain python.
# This may be useful for testing on a local machine, but should
# be revised for the particular usecase.
cwd = os.getcwd()
try:
    pth = os.path.join('containers', 'rcontainer.sif')
    try:
        runtime = 'apptainer'
        out = subprocess.run(runtime, check=False)
    except FileNotFoundError:
        try:
            runtime = 'singularity'
            out = subprocess.run(runtime, check=False)
        except FileNotFoundError as exc:
            raise FileNotFoundError from exc
    PREFIX = f'{runtime} run {pth} Rscript'
    PREFIX_MOUNT = f'{runtime} run --home={cwd}:/home/ {pth} Rscript'
    PREFIX_CUSTOM_MOUNT = f'{runtime} run --home={cwd}:/home/ ' + \
        '{custom_mount}' + f'{pth} Rscript'
except FileNotFoundError:
    try:
        runtime = 'docker'
        out = subprocess.run(runtime, check=False)
        PREFIX = (f'{runtime} run ' +
                  'ghcr.io/espenhgn/rcontainer Rscript')
        PREFIX_MOUNT = (
            f'{runtime} run ' +
            f'--mount type=bind,source={cwd},target={cwd} ' +
            'ghcr.io/espenhgn/rcontainer Rscript')
        PREFIX_CUSTOM_MOUNT = (
            f'{runtime} run ' +
            f'--mount type=bind,source={cwd},target={cwd} ' +
            '{custom_mount} ' +
            'ghcr.io/espenhgn/rcontainer Rscript')
    except FileNotFoundError:
        # neither singularity nor docker found, fall back to plain python
        runtime = None
        PREFIX = 'Rscript'
        PREFIX_MOUNT = 'Rscript'
        PREFIX_CUSTOM_MOUNT = 'Rscript'


def test_assert():
    """dummy test that should pass"""
    assert True


def test_rcontainer_Rscript():
    """test that the Rscript installation works"""
    call = f'{PREFIX} --version'
    out = subprocess.run(call.split(' '))
    assert out.returncode == 0


def test_rcontainer_R_script():
    '''test that R can run a script'''
    cwd = os.getcwd() if runtime == 'docker' else '.'
    call = f'''{PREFIX_MOUNT} {cwd}/tests/extras/hello.R'''
    out = subprocess.run(call.split(' '), capture_output=True)
    assert out.returncode == 0


def test_rcontainer_R_script_from_tempdir():
    '''test that the tempdir is working'''
    with tempfile.TemporaryDirectory() as d:
        os.system(f'cp {cwd}/tests/extras/hello.R {d}/')
        if runtime == 'docker':
            custom_mount = f'--mount type=bind,source={d},target={d}'
        elif runtime in ['apptainer', 'singularity']:
            custom_mount = f'--bind {d}:{d} '
        else:
            custom_mount = ''
        call = f'{PREFIX_CUSTOM_MOUNT.format(custom_mount=custom_mount)} ' + \
            f'{d}/hello.R'
        out = subprocess.run(call, shell=True, check=False)
        assert out.returncode == 0


def test_r_R_packages():
    call = f'{PREFIX_MOUNT} {cwd}/tests/extras/r.R'
    out = subprocess.run(call.split(' '), check=False)
    assert out.returncode == 0
