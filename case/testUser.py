from base import helper
from base import toolkit
from base import baseData
from case import baseCase
from case import dataUser as testData


class TestUser(baseCase.BaseCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        helper.delete_namespace_without_warning()
        helper.create_namespace()

    def setUp(self):
        try:
            helper.get_response('delete', testData.user_url)
        except:
            pass

    def test_admin_user_login(self):
        helper.save_token()
        token = helper.get_token_by_file()
        self.assertIn(testData.token_prefix, token)

    def test_user_create(self):
        response = helper.get_response('post', testData.user_collection_url, testData.create_user)
        self.assertEqual(baseData.status_created, response.status)
        self.assertEqual(testData.project, response.response['projects'])

    def test_normal_user_login(self):
        self.test_user_create()
        token = helper.get_token_by_login(testData.user, testData.password)
        self.assertIn(testData.token_prefix, token)

    def test_normal_user_update_by_admin(self):
        self.test_user_create()
        token_test = helper.get_token_by_login(testData.user, testData.password)
        deployments_test = helper.get_response('get', testData.deployment_url_test, token=token_test)
        deployments_test_422 = helper.get_response('get', testData.deployment_url_extra, token=token_test)
        self.assertEqual(baseData.status_ok, deployments_test.status)
        self.assertEqual(baseData.status_forbidden, deployments_test_422.status)
        helper.get_response('put', testData.user_url, testData.update_user)
        token_extra = helper.get_token_by_login(testData.user, testData.password)
        deployments_extra = helper.get_response('get', testData.deployment_url_extra, token=token_extra)
        deployments_extra_422 = helper.get_response('get', testData.deployment_url_test, token=token_extra)
        self.assertEqual(baseData.status_ok, deployments_extra.status)
        self.assertEqual(baseData.status_forbidden, deployments_extra_422.status)

    def test_user_delete(self):
        self.test_user_create()
        login_status = helper.user_login_status(testData.user, testData.password)
        self.assertEqual(baseData.status_ok, login_status)
        delete_user = helper.get_response('delete', testData.user_url)
        self.assertEqual(baseData.status_no_content, delete_user.status)
        relogin_status = helper.user_login_status(testData.user, testData.password)
        self.assertEqual(baseData.status_forbidden, relogin_status)

    def test_user_get(self):
        self.test_user_create()
        user = helper.get_response('get', testData.user_url)
        self.assertEqual(baseData.status_ok, user.status)
        self.assertEqual(testData.project, user.response['projects'])

    def test_user_get_list(self):
        self.test_user_create()
        user = helper.get_response('get', testData.user_collection_url)
        self.assertEqual(baseData.status_ok, user.status)
        self.assertIsNotNone(user.response['data'])

    def test_user_privilege(self):
        """Test with script/resource_field_validate"""
        pass

    def test_use_wrong_token(self):
        deployments_test = helper.get_response('get', testData.deployment_url_test, token=toolkit.gen_random_str())
        self.assertEqual(baseData.status_forbidden, deployments_test.status)

    def test_normal_user_reset_password(self):
        self.test_user_create()
        token = helper.get_token_by_login(testData.user, testData.password)
        helper.get_response('post', testData.reset_password_url, testData.reset_password, token)
        reset_token = helper.get_token_by_login(testData.user, testData.new_password)
        deployments_test = helper.get_response('get', testData.deployment_url_test, token=reset_token)
        self.assertEqual(baseData.status_ok, deployments_test.status)

    def test_normal_user_update_namespace(self):
        self.test_user_create()
        token_test = helper.get_token_by_login(testData.user, testData.password)
        response_test = helper.get_response('put', testData.user_url, testData.update_user, token_test)
        self.assertEqual(baseData.status_forbidden, response_test.status)

    def test_normal_user_own_multi_namespace(self):
        helper.get_response('post', testData.user_collection_url, testData.create_user_with_multi_namespace)
        token_test = helper.get_token_by_login(testData.user, testData.password)
        deployments_test = helper.get_response('get', testData.deployment_url_test, token=token_test)
        self.assertEqual(baseData.status_ok, deployments_test.status)
        deployments_extra = helper.get_response('get', testData.deployment_url_extra, token=token_test)
        self.assertEqual(baseData.status_ok, deployments_extra.status)

    def test_normal_user_own_all_namespaces(self):
        helper.get_response('post', testData.user_collection_url, testData.create_user_with_all_namespace)
        token_test = helper.get_token_by_login(testData.user, testData.password)
        deployments_test = helper.get_response('get', testData.deployment_url_test, token=token_test)
        self.assertEqual(baseData.status_ok, deployments_test.status)
        deployments_extra = helper.get_response('get', testData.deployment_url_extra, token=token_test)
        self.assertEqual(baseData.status_ok, deployments_extra.status)

    def test_admin_list_user(self):
        self.test_user_create()
        user_list = helper.get_response('get', testData.user_collection_url)
        self.assertEqual(baseData.status_ok, user_list.status)
        self.assertEqual(len(testData.admin_and_normal_user), len(user_list.response['data']))

    def test_normal_user_list_user(self):
        self.test_user_create()
        token_test = helper.get_token_by_login(testData.user, testData.password)
        user_list = helper.get_response('get', testData.user_collection_url, token=token_test)
        self.assertEqual(baseData.status_ok, user_list.status)
        self.assertEqual(len(testData.normal_user), len(user_list.response['data']))

    def test_admin_list_cluster(self):
        self.test_user_create()
        cluster_list = helper.get_response('get', testData.cluster_collection_url)
        self.assertEqual(baseData.status_ok, cluster_list.status)
        self.assertEqual(len(testData.all_cluster), len(cluster_list.response['data']))

    def test_normal_user_list_cluster(self):
        self.test_user_create()
        token_test = helper.get_token_by_login(testData.user, testData.password)
        cluster_list = helper.get_response('get', testData.cluster_collection_url, token=token_test)
        self.assertEqual(baseData.status_ok, cluster_list.status)
        self.assertEqual(len(testData.extra_cluster), len(cluster_list.response['data']))

    def test_admin_list_namespace(self):
        self.test_user_create()
        namespace_list = helper.get_response('get', testData.namespace_collection_url)
        self.assertEqual(baseData.status_ok, namespace_list.status)
        self.assertGreater(len(namespace_list.response['data']), testData.namespace_least_count)

    def test_normal_user_list_namespace(self):
        self.test_user_create()
        token_test = helper.get_token_by_login(testData.user, testData.password)
        namespace_list = helper.get_response('get', testData.namespace_collection_url, token=token_test)
        self.assertEqual(baseData.status_ok, namespace_list.status)
        self.assertLess(len(namespace_list.response['data']), testData.namespace_least_count)
