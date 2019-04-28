from base import helper
from base import baseData
from case import baseCase
from case import dataDeployment as testData


class TestDeployment(baseCase.BaseCase):

    def test_update_replicas(self):
        post_deployment = helper.get_response('post', testData.deployment_collection_url, testData.deployment_post_body)
        self.assertEqual(baseData.status_created, post_deployment.status)
        put_deployment = helper.get_response('put', testData.deployment_url, testData.deployment_put_body)
        self.assertEqual(baseData.status_ok, put_deployment.status)
        get_deployment = helper.get_response('get', testData.deployment_url)
        self.assertEqual(baseData.status_ok, get_deployment.status)
        self.assertEqual(testData.put_replicas, get_deployment.response['replicas'])
