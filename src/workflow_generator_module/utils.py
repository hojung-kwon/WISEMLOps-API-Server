import os
import random
import string


def get_workflow_name(name: str):
    if name is None or len(name.strip()) < 1:
        return make_workflow_name()
    return name


def make_workflow_name():
    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(12)))
    return result_str


def get_workflow_generator_path():
    return os.path.dirname(__file__)
