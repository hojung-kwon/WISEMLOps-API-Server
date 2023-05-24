import kserve

from src import app_config

kserve_client = kserve.KServeClient(config_file=app_config.CLUSTER_KUBE_CONFIG_PATH)
