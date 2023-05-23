from kubernetes import client
from src import app_config
from src.cluster.models import \
    Volume, VolumeClaim, \
    ConfigMap, Secret, \
    Container, ContainerVolume, ContainerVolumeType, \
    Pod, Deployment, \
    Service, Ingress, Metadata


class ClientFactory:

    @staticmethod
    def create_client():
        return client.CoreV1Api()

    @staticmethod
    def create_deployment_client():
        return client.AppsV1Api()

    @staticmethod
    def create_networking_api():
        return client.NetworkingV1Api()


class ClientTemplateFactory:

    @staticmethod
    def build_metadata(metadata: Metadata):
        return client.V1ObjectMeta(
            name=metadata.name,
            labels=metadata.labels,
            annotations=metadata.annotations
        )

    @staticmethod
    def build_namespace(metadata: Metadata):
        return client.V1Namespace(
            metadata=ClientTemplateFactory.build_metadata(metadata)
        )

    @staticmethod
    def build_nfs_volume():
        nfs_server, nfs_path = app_config.get_nfs_config()
        return client.V1NFSVolumeSource(
            server=nfs_server,
            path=nfs_path,
            read_only=False
        )

    @staticmethod
    def build_pv(pv: Volume):
        _volume = client.V1PersistentVolume(
            metadata=client.V1ObjectMeta(name=pv.name),
            spec=client.V1PersistentVolumeSpec(
                capacity={'storage': pv.storage_size},
                volume_mode=pv.volume_mode,
                access_modes=[pv.access_mode],
                storage_class_name=pv.storage_class,
                persistent_volume_reclaim_policy=pv.policy,
            )
        )
        if pv.volume_type == 'nfs':
            _volume.spec.nfs = ClientTemplateFactory.build_nfs_volume()
        return _volume

    @staticmethod
    def build_pvc(pvc: VolumeClaim):
        _claim = client.V1PersistentVolumeClaim(
            metadata=client.V1ObjectMeta(name=pvc.name),
            spec=client.V1PersistentVolumeClaimSpec(
                storage_class_name=pvc.storage_class,
                resources=client.V1ResourceRequirements(
                    requests={'storage': pvc.storage_size}
                ),
                access_modes=[pvc.access_mode],
            )
        )
        return _claim

    @staticmethod
    def build_configmap(config_map: ConfigMap):
        return client.V1ConfigMap(
            metadata=ClientTemplateFactory.build_metadata(config_map.metadata),
            data=config_map.data
        )

    @staticmethod
    def build_secret(secret: Secret):
        return client.V1Secret(
            metadata=ClientTemplateFactory.build_metadata(secret.metadata),
            data=secret.data,
            type=secret.type
        )

    @staticmethod
    def build_container(container: Container):
        return client.V1Container(
            name=container.name,
            image=container.image,
            image_pull_policy=container.image_pull_policy,
            args=container.args,
            env=[client.V1EnvVar(name=key, value=value) for key, value in container.env.items()],
            resources=client.V1ResourceRequirements(
                requests={
                    'cpu': container.cpu,
                    'memory': container.memory,
                    'nvidia.com/gpu': container.gpu
                },
                limits={
                    'cpu': container.cpu,
                    'memory': container.memory,
                    'nvidia.com/gpu': container.gpu
                }
            ),
            volume_mounts=[
                client.V1VolumeMount(
                    name=volume_mount.name,
                    mount_path=volume_mount.mount_path
                ) for volume_mount in container.volume_mounts
            ],
        )

    @staticmethod
    def build_container_volume(container_volume: ContainerVolume):
        volume = client.V1Volume(name=container_volume.name)

        if container_volume.type == ContainerVolumeType.PersistentVolumeClaim:
            volume.persistent_volume_claim = \
                client.V1PersistentVolumeClaimVolumeSource(claim_name=container_volume.type_name)
        if container_volume.type == ContainerVolumeType.Secret:
            volume.secret = client.V1SecretVolumeSource(secret_name=container_volume.type_name)
        if container_volume.type == ContainerVolumeType.ConfigMap:
            volume.config_map = client.V1ConfigMapVolumeSource(name=container_volume.type_name)
        if container_volume.type == ContainerVolumeType.EmptyDir:
            volume.empty_dir = client.V1EmptyDirVolumeSource(medium=container_volume.type_name)
        return volume

    @staticmethod
    def build_image_pull_secrets(secrets: list):
        if secrets is None:
            return None
        return [client.V1LocalObjectReference(name=item) for item in secrets]

    @staticmethod
    def build_pod(pod: Pod):
        return client.V1Pod(
            metadata=ClientTemplateFactory.build_metadata(pod.metadata),
            spec=client.V1PodSpec(
                containers=[ClientTemplateFactory.build_container(container) for container in pod.containers],
                image_pull_secrets=ClientTemplateFactory.build_image_pull_secrets(pod.image_pull_secrets),
                volumes=[ClientTemplateFactory.build_container_volume(volume) for volume in pod.volumes],
                service_account_name=pod.service_account_name
            )
        )

    @staticmethod
    def build_deployment(deployment: Deployment):
        deployment.metadata.labels['app'] = deployment.metadata.name
        deployment.template_pod.metadata.labels['app'] = deployment.metadata.name
        return client.V1Deployment(
            metadata=ClientTemplateFactory.build_metadata(deployment.metadata),
            spec=client.V1DeploymentSpec(
                replicas=deployment.replicas,
                selector=client.V1LabelSelector(
                    match_labels=deployment.metadata.labels
                ),
                template=ClientTemplateFactory.build_pod(deployment.template_pod)
            )
        )

    @staticmethod
    def build_service(service: Service):
        return client.V1Service(
            metadata=ClientTemplateFactory.build_metadata(service.metadata),
            spec=client.V1ServiceSpec(
                type=service.type.value,
                selector=service.selectors,
                ports=[client.V1ServicePort(
                    name=port.name,
                    port=port.port,
                    target_port=port.target_port,
                    node_port=port.node_port,
                    protocol=port.protocol
                ) for port in service.ports]
            )
        )

    @staticmethod
    def build_ingress(ingress: Ingress):
        ingress.metadata.annotations.update({
            'nginx.ingress.kubernetes.io/rewrite-target': '/'
        })
        return client.V1Ingress(
            metadata=ClientTemplateFactory.build_metadata(ingress.metadata),
            spec=client.V1IngressSpec(
                ingress_class_name=ingress.ingress_class_name,
                rules=[client.V1IngressRule(
                    host=rule.host,
                    http=client.V1HTTPIngressRuleValue(
                        paths=[client.V1HTTPIngressPath(
                            path=path_item.path,
                            path_type=path_item.path_type,
                            backend=client.V1IngressBackend(
                                service=client.V1IngressServiceBackend(
                                    name=path_item.service_name,
                                    port=client.V1ServiceBackendPort(
                                        number=path_item.service_port
                                    )
                                )
                            )
                        ) for path_item in rule.paths]
                    )
                ) for rule in ingress.rules]
            )
        )


