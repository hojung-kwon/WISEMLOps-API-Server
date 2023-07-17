import os
import re
import string

from jinja2 import FileSystemLoader, Environment

from src.pipeline_generator.utils import get_pipeline_generator_path


def get_template():
    template_path = os.path.join(get_pipeline_generator_path(), "template")
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
    template = template_env.get_template("ml_pipeline_template.jinja2", parent=template_path)

    return template


def get_env_variables():
    env_variables = {
        'AWS_ENDPOINT_URL': {
            'value': 'http://minio-service.kubeflow.svc.cluster.local:9000'
        },
        'MLFLOW_S3_ENDPOINT_URL': {
            'value': 'http://minio-service.kubeflow.svc.cluster.local:9000'
        },
        'MLFLOW_TRACKING_URI': {
            'value': 'http://mlflow-server-service.mlflow-system.svc.cluster.local:5000'
        },
        'EXPERIMENT_NAME': {
            'value': 'yswhan-dtc-sample'
        },
        'MODEL_NAME': {
            'value': 'yswhan-dtc-sample'
        },
        'MLFLOW_BUCKET_NAME': {
            'value': 'mlflow'
        },
        'AWS_ACCESS_KEY_ID': {
            'value_from': "client.V1EnvVarSource(secret_key_ref=client.V1SecretKeySelector(name='minio30creds', key='AWS_ACCESS_KEY_ID'))"
        },
        'AWS_SECRET_ACCESS_KEY': {
            'value_from': "client.V1EnvVarSource(secret_key_ref=client.V1SecretKeySelector(name='minio30creds', key='AWS_SECRET_ACCESS_KEY'))"
        },
    }
    return env_variables
