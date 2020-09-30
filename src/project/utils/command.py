from src.utils import Subprocess


def command_git_tag(name, output_directory, github, extension):
    git = "git -C {}/{} tag > {}/{}".format(
        output_directory, github, output_directory, name
    )
    return git + extension  # noqa: F401


def command_git_tag_checkout(output_directory, github, tag):
    return "git -C {}/{} checkout tags/{}".format(output_directory, github, tag)


def command_touch(name, output_directory, extension):
    # create empty txt file to store unmatched tags
    Subprocess("touch {}/{}".format(output_directory, name) + extension).Run()
