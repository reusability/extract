import subprocess


class Subprocess:
    def __init__(self, command, **kwargs):
        _args = ""
        for key, val in kwargs.items():
            _args += key + val + " "

        self.command = command + _args

    def run(self, capture_output=False):
        subprocess.run(self.command, shell=True, capture_output=capture_output)


def make_dir(path: str):
    sub = Subprocess("mkdir {}".format(path))
    sub.run()


def copy_files(source: str, target: str, dir=False):

    if not dir:
        sub = Subprocess("mv {} {}".format(source, target))
    else:
        sub = Subprocess("mv -r {} {}".format(source, target))
    sub.run()


def remove_dir(path: str):
    sub = Subprocess("rm -r {}".format(path))
    sub.run()
