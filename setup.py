# setup.py

from setuptools import setup, find_packages



deps = [
    "openai"
]

setup(
    name="cli-gpt",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=deps,
    entry_points={
        'console_scripts': [
            'cli-gpt = cli-gpt.main:main',
            'ask = cli-gpt.main:main'
        ]
    },
)


