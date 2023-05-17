from pydantic import BaseModel


class PersistentVolume(BaseModel):
    name: str
    size: str = '3Gi'
    volume_mode: str = 'Filesystem'
    access_mode: str = 'ReadWriteOnce'
    storage_class: str = 'default-storage-class'
    policy: str = 'Delete'
    volume_type: str = 'nfs'
