from kubernetes import client


class ClusterException(client.ApiException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
