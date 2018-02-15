from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['numpy', 'scipy', 'pillow']
FOUND_PACKAGES = find_packages()
IGNORE_PACKAGES = ['tests']
KEEP_PACKAGES = [i_pack for i_pack in FOUND_PACKAGES if i_pack not in IGNORE_PACKAGES]

setup(name='unet',
      version='0.1',
      description='Sample function related to the unet',
      url='https://github.com/Dammi87/unet_weight',
      author='Adam Fjeldsted',
      author_email='87dammi@gmail.com',
      license='MIT',
      packages=KEEP_PACKAGES,
      install_requires=REQUIRED_PACKAGES,
      zip_safe=False)
