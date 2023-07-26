from setuptools import setup

from proxy import __version__

setup(
    name='proxy-demo',
    version='.'.join(map(str, __version__)),
    description='Proxy demo app',
    long_description='Proxy demo app',
    author='Sergey Zezyulin',
    author_email='zezyulinsv@yandex.ru',
    maintainer='Sergey Zezyulin',
    url='https://gitlab.com/zezyulinsv/proxy-demo',
    license='Other/Proprietary License',
    packages=['proxy-demo'],
    include_package_data=True,
    scripts=['bin/proxy-demo'],
    install_requires=['Flask', 'python_magic'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Flask',
        'Intended Audience :: Customer Service',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
    ],
    python_requires='>=3.6'
)
