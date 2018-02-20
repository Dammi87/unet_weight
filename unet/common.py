import os


def listdir(dir_path):
    """Returns all files within directory, even for google buckets"""
    if 'gs://' in dir_path:
        result = os.popen('gsutil ls %s' % dir_path).read()
        files = result.split('\n')
    else:
        files = [os.path.join(dir_path, file) for file in os.listdir(dir_path)]

    return files[0:2]
