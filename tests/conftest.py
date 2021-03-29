from sys import version_info

def pytest_ignore_collect(path, config):
    if 'py3_9' in str(path):
        if version_info < (3, 9, 0):
            return True
    
    if 'py3_$' in str(path):
        if version_info >= (3, 9, 0):
            return True
    