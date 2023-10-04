import os
import re
import string

from jinja2 import FileSystemLoader, Environment

from src import app_config
from src.workflow_generator_module.utils import get_workflow_generator_path

MODULE_CODE = 106


def get_template(template_type: str):
    template_path = os.path.join(get_workflow_generator_path(), "template")
    template_loader = FileSystemLoader(template_path)
    template_env = Environment(loader=template_loader)
    # Add filter that produces a Python-safe variable name
    template_env.filters["python_safe"] = lambda x: re.sub(r"[" + re.escape(string.punctuation) + "\\s]", "_", x)
    # Add filter that escapes the " character in strings
    template_env.filters["string_delimiter_safe"] = lambda x: re.sub('"', '\\"', x)
    # Add filter that converts a value to a python variable value (e.g. puts quotes around strings)
    template_env.filters["param_val_to_python_var"] = (
        lambda p: "None" if p.value is None else (f'"{p.value}"' if p.input_type.base_type == "String" else p.value)
    )
    template = template_env.get_template(template_type + "_template.jinja2", parent=template_path)

    return template


def get_mlflow_s3_endpoint_url():
    return app_config.MINIO_ENDPOINT


def get_aws_access_key_id():
    return app_config.MINIO_ACCESS_KEY


def get_aws_secret_access_key():
    return app_config.MINIO_SECRET_KEY


def get_mlflow_tracking_uri():
    return app_config.MLFLOW_TRACKING_URI
