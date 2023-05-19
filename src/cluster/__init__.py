from src.cluster.config import load_config
from src.cluster.service import ClusterService

load_config()
cluster_service = ClusterService()