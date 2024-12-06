from setuptools import setup, find_packages

setup(
    name="bitcoin_trading_analyzer",
    version="1.0.0",
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'PyQt5',
        'numpy',
        'pandas',
        'scikit-learn',
        'requests',
    ],
    package_dir={'': '.'}
)