from setuptools import setup, find_packages

setup(
    name='ghas',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask==0.12.2",
        "gunicorn==19.7.1",
        "PyGitHub==1.25.2"
    ]
)
