from setuptools import setup, Extension

setup(
    name='mykmeanssp',
    version='1.0',
    description='K-means++ C extension',
    ext_modules=[
        Extension(
            'mykmeanssp', 
            sources=['kmeansmodule.c'] 
        )
    ]
)