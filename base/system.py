def test_path():
    path = __file__
    path = path.replace('base/system.py', '')
    return path


TEST_PATH = test_path()
