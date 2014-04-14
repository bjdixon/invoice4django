from setuptools import setup, find_packages
import invoice4django

setup(
    name='invoice4django',
	#version=invoice4django.__version__,
    description='Simple invoice app for Django',
    long_description='\n'.join((
        open('README.md').read(),
        open('CHANGES.md').read(),
    )),
    author='Brian Dixon',
    author_email='bjdixon@gmail.com',
    maintainer='Brian Dixon',
    url='https://github.com/bjdixon/invoice4django/',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3.3',
        "License :: OSI Approved :: MIT License",
    ],
    tests_require=["Django>=1.5", "webtest>=2.0.6", "django-webtest>=1.7"],
    include_package_data=True,
    test_suite='runtests.main',
)
