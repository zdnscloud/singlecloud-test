from base import helper
from base import baseData
from case import baseCase
from case import dataAgent as testData


class TestAgent(baseCase.BaseCase):

    def test_inner_service(self):
        helper.get_response('post', testData.service_url, testData.service_body)
        inner_service = helper.get_response('get', testData.inner_service_url)
        self.assertEqual(baseData.status_ok, inner_service.status)
        self.assertTrue(inner_service.response['data'])

    def test_outer_service(self):
        helper.get_response('post', testData.service_url, testData.service_body)
        helper.get_response('post', testData.ingress_url, testData.ingress_body)
        outer_service = helper.get_response('get', testData.outer_service_url)
        self.assertEqual(baseData.status_ok, outer_service.status)
        self.assertTrue(outer_service.response['data'])
        inner_service = helper.get_response('get', testData.inner_service_url)
        self.assertFalse(inner_service.response['data'])
