from base import helper
from base import baseData

inner_service_url = baseData.agent_base_url + '/namespaces/namespace-test/innerservices'
outer_service_url = baseData.agent_base_url + '/namespaces/namespace-test/outerservices'

service_url = helper.get_collection_url('service')
service_body = {"name": "service-test", "serviceType": "nodeport", "exposedPorts": [{"name": "service-test", "port": 2, "targetPort": 1, "protocol": "tcp"}]}

ingress_url = helper.get_collection_url('ingress')
ingress_body = {"name": "ingress-test", "rules": [{"host": "ingress-testyqxzyxrv", "protocol": "tcp", "paths": [
    {"path": "/ingress-testakdjjhwuAgtWYXod", "serviceName": "service-test", "servicePort": 2}]}]}
