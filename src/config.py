import os

import yaml


class Config:
    def __init__(self):
        current_path = os.path.dirname(__file__)
        parent_path = os.path.dirname(current_path)
        yaml_path = os.path.join(parent_path, 'application.yaml')
        with open(yaml_path, 'r') as yaml_conf:
            conf = yaml.safe_load(yaml_conf)[os.environ.get('APP_ENV', 'local')]
        self._config = conf

        self.CLUSTER_HOST = self._config['CLUSTER']['HOST']
        self.CLUSTER_KUBE_CONFIG_PATH = self._config['CLUSTER']['KUBE_CONFIG_PATH']
        self.CLUSTER_VOLUME_NFS_SERVER = self._config['CLUSTER']['VOLUME_NFS_SERVER']
        self.CLUSTER_VOLUME_NFS_PATH = self._config['CLUSTER']['VOLUME_NFS_PATH']
        self.MINIO_ENDPOINT = self._config['MINIO']['ENDPOINT']
        self.MINIO_ACCESS_KEY = self._config['MINIO']['ACCESS_KEY']
        self.MINIO_SECRET_KEY = self._config['MINIO']['SECRET_KEY']
        self.MLFLOW_TRACKING_URI = self._config['MLFLOW']['TRACKING_URI']
        self.KUBEFLOW_PIPELINES_ENDPOINT = self._config['KUBEFLOW']['PIPELINES']['ENDPOINT']
        self.SQLALCHEMY_DATABASE_URL = self._config['DATABASE']['SQLALCHEMY_DATABASE_URL']

        self.SERVICE_CODE = 100
        pass
