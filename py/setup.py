from setuptools import setup
import versioneer
import os
os.environ["mater_base"] = os.path.abspath(os.path.pardir)

setup(name='mater',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      packages=['mater'],
      package_dir={'mater': 'mater'},
      scripts=[],
      setup_requires=["cffi>=1.12.0",
                      "versioneer==0.18"],
      cffi_modules=["mater/build_shimmer4py.py:ffibuilder"],
      install_requires=["cffi>=1.12.0",
                        "docopt>=0.6.2",
                        "numpy>=1.16.2",
                        "vcfpy==0.12.1",
                        "ncls==0.0.52",
                        "pysam==0.15.3",
                        "networkx>=2.4",
                        "intervaltree==3.0.2"])
