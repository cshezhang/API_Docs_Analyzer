import os
from subprocess import Popen, PIPE

current_env = os.environ.copy()


def shell_command(cmd):
    p = Popen(cmd.split(' '), env=current_env, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    return [p.returncode, stdout, stderr]
