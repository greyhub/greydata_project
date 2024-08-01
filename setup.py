from setuptools import setup, find_packages
import os


def get_version(package):
    with open(os.path.join(package, '__init__.py')) as f:
        for line in f:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Version not found.")


setup(
    name='greydata',
    version=get_version('greydata'),
    author='Grey Ng',
    author_email='luongnv.grey@gmail.com',
    description='Library for data analyst',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://greyhub.github.io/',
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=[
        # Danh sách các thư viện phụ thuộc nếu có
    ],
    entry_points={
        'console_scripts': [
            'greydata=greydata.cli:main',
        ],
    },
    keywords='data processing analysis',
    license='MIT',
    project_urls={
        'Documentation': 'https://greyhub.github.io/',
        'Source': 'https://github.com/username/greydata',
        'Tracker': 'https://github.com/username/greydata/issues',
    },
)
