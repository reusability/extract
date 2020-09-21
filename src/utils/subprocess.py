import subprocess


class Subprocess:
    def __init__(self, command, **kwargs):
        _args = ""
        for key, val in kwargs.items():
            _args += key + val + " "

        self.command = command + _args

    def Run(self, capture_output=False):
        subprocess.run(self.command, shell=True, capture_output=capture_output)


def make_dir(path: str):
    sub = Subprocess("mkdir {}".format(path))
    sub.Run()


def copy_files(source: str, target: str, dir=False):
    if not dir:
        sub = Subprocess("mv {} {}".format(source, target))
    else:
        sub = Subprocess("mv -r {} {}".format(source, target))
    sub.Run()


def remove_dir(path: str):
    Subprocess("sudo chmod 777 .").Run()
    sub = Subprocess("sudo rm -rf {}".format(path))
    sub.Run()
