from setuptools import setup

setup(
    name='neby_code',
    version='1.0.0',
    description='Neby Code local workspace agent daemon',
    py_modules=['daemon', 'fsops', 'term', '__main__'],
    install_requires=[
        'websockets>=12.0',
    ],
    entry_points={
        'console_scripts': [
            'neby_code=daemon:main',
            'neby-code=daemon:main',
        ],
    },
    python_requires='>=3.8',
)
