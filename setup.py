from setuptools import setup, find_packages

setup(
    name='kubemq_forwarder',
    version='0.1.0',
    py_modules=['app'],
    install_requires=[
        'kubemq',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'kubemq-forward=app:main'
        ]
    },
    description='Kubemq Event Forwarder to Queue',
    author='Automatic Setup',
    author_email='user@example.com',
    url='https://github.com/user/kubemq_py',
    license='MIT',
)
