from base import helper
from copy import deepcopy

deployment_collection_url = helper.get_collection_url('deployment')
deployment_url = helper.get_resource_url('deployment')

deployment_post_body = {
    "name": "deployment-test",
    "replicas": 1,
    "containers": [{"name": "deployment-test", "image": "deployment-test"}]
}

put_replicas = 2
deployment_put_body = deepcopy(deployment_post_body)
deployment_put_body['replicas'] = put_replicas
