from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "pkc_cython",
        ["code/pkc_cython/pkc_cython.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]

setup(
    name='pkc',
    ext_modules=cythonize(ext_modules),
)