from base import baseCase
from base import helper


class BaseCase(baseCase.BaseCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        helper.delete_namespace_without_warning()
        helper.create_namespace()

    def tearDown(self):
        super().tearDown()
