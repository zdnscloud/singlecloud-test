from base import baseCase
from base import helper


class BaseCase(baseCase.BaseCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        helper.delete_namespace_without_warning()
        helper.create_namespace()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
