from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import os
import subprocess

# Recover the gcc compiler path
gcc_output = subprocess.Popen(['gcc', '-print-libgcc-file-name'],
                              stdout=subprocess.PIPE).communicate()[0]
gcc_path = os.path.normpath(os.path.dirname(gcc_output.decode('utf-8')))

# Recover the CLASS version from common.h
version = None
with open(os.path.join('..', 'include', 'common.h'), 'r') as v_file:
    for line in v_file:
        if "_VERSION_" in line:
            # Extract version, removing the " and the v
            version = line.split()[-1].strip('"v')
            break

if version is None:
    raise RuntimeError("Could not find version in common.h")

# Define the Cython extension module
extensions = [
    Extension("classy", ["classy.pyx"],
              include_dirs=[np.get_include(), "../include"],
              libraries=["class"],
              library_dirs=["../", gcc_path],
              extra_link_args=['-lgomp'])
]

# Use cythonize on the defined extensions
setup(
    name='classy',
    version=version,
    description='Python interface to the Cosmological Boltzmann code CLASS',
    url='http://www.class-code.net',
    ext_modules=cythonize(extensions, language_level="3"),
    data_files=[('bbn', ['../bbn/sBBN.dat'])]
)
