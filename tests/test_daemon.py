
"""Unit test for ../dameon.py"""
from ..slips import *
import os
import argparse
import subprocess
import time
import pytest

IS_IN_A_DOCKER_CONTAINER = os.environ.get('IS_IN_A_DOCKER_CONTAINER', False)


def do_nothing(*args):
    """Used to override the print function because using
     the self.print causes broken pipes"""
    pass


# Main Class tests


def create_main_instance():
    """returns an instance of Main() class in slips.py"""
    main = Main(testing=True)
    main.input_information = 'test.pcap'
    main.input_type = 'pcap'
    main.line_type = False
    return main


# Daemon tests
@pytest.mark.skipif(
    os.geteuid() != 0, reason='supported only with root priveledges'
)
def create_Daemon_instance():
    """returns an instance of Daemon() class in slips.py"""
    slips = create_main_instance()
    # since we wont becalling __main__ we need to setup the args manually
    slips.args = argparse.Namespace(
        blocking=False,
        clearcache=False,
        config='slips.conf',
        debug=None,
        filepath='dataset/hide-and-seek-short.pcap',
        gui=False,
        interactive=False,
        interface=None,
        nologfiles=True,
        output='output/',
        pcapfilter=None,
        restartdaemon=False,
        stopdaemon=False,
        verbose=None,
    )
    return Daemon(slips)


# @pytest.mark.skipif(
#     os.geteuid() != 0, reason='supported only with root priveledges'
# )
def test_setup_std_streams():
    daemon = create_Daemon_instance()
    os.system('./slips.py -f dataset/hide-and-seek-short.pcap -D')
    # __init__ calls read_configuration which calls setup_std_streams
    # we need to make sure that all files are there
    assert os.path.exists(daemon.logsfile)
    assert os.path.exists(daemon.stdout)
    assert os.path.exists(daemon.stderr)
    assert os.path.exists(daemon.stdin)
    assert os.path.exists(daemon.pidfile)
    # make sure the files aren't empty
    used_files = f'Logsfile: {daemon.logsfile}\n' \
                 f'pidfile:{daemon.pidfile}\n' \
                 f'stdin : {daemon.stdin}\n' \
                 f'stdout: {daemon.stdout}\n' \
                 f'stderr: {daemon.stderr}\n'
    with open(daemon.logsfile, 'r') as logsfile:
        # make sure used file are logged
        assert used_files in logsfile.read()
    # stop the daemon
    os.system('sudo ./slips.py -S')

#
# @pytest.mark.skipif(
#     os.geteuid() != 0, reason='supported only with root priveledges'
# )
def test_pidfile():
    """tests creating, writing to and deleting pidfile"""
    # run slips in a parallel process
    cmd = './slips.py -c slips.conf -f dataset/hide-and-seek-short.pcap -D'
    subprocess.Popen([cmd], shell=True, stdin=None, stdout=None, stderr=None)
    # wait until the pid is written to the file
    time.sleep(2)
    # this instance is just to get the pidfile, we're not starting the daemon again
    daemon = create_Daemon_instance()
    # make sure there's a pid in pidfile
    assert os.stat(daemon.pidfile).st_size > 0
    # # wait for slips to finish
    # time.sleep(30)
    # stop slips
    os.system('sudo ./slips.py -S')
    # make sure the pidfile is deleted after slips is finished
    assert not os.path.exists(daemon.pidfile)


# @pytest.mark.skipif(
#     os.geteuid() != 0, reason='supported only with root priveledges'
# )
def test_print():
    daemon = create_Daemon_instance()
    daemon.print('Test')
    with open(daemon.logsfile, 'r') as f:
        assert 'Test' in f.read()


# @pytest.mark.skipif(
#     os.geteuid() != 0, reason='supported only with root priveledges'
# )
def test_stop():
    """tests if the daemon is successfully killed after running the daemon stop function"""
    # run slips in a parallel process
    cmd = (
        'sudo ./slips.py -c slips.conf  -f dataset/hide-and-seek-short.pcap'
    )
    subprocess.Popen([cmd], shell=True, stdin=None, stdout=None, stderr=None)
    # wait until the pid is written to the file
    time.sleep(2)
    # this instance is just to get the pidfile, we're not starting the daemon again
    daemon = create_Daemon_instance()
    # get the pid of the daemon
    with open(daemon.pidfile, 'r') as f:
        pid = int(f.read())
    # run the daemon stop function
    os.system('sudo ./slips.py -S')
    # assert that pid is not there after stopping
    process_killed = False
    try:
        os.kill(pid, 0)
        process_killed = True
    except OSError as e:
        if str(e).find('No such process') > 0:
            # some error occured
            process_killed = True
    assert process_killed
