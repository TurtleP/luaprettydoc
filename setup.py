from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

__version = None
__description = None
with open('luaprettydoc/__init__.py', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = eval(line.split('=')[1])
        elif line.startswith('__description__'):
            __description = eval(line.split('=')[1])

setup(
    name='luaprettydoc',
    version=version,
    author='TurtleP',
    author_email='jpostelnek@outlook.com',
    license='MIT',
    url='https://github.com/TurtleP/luaprettydoc',
    python_requires='>=3.8.0',
    description=__description,
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=[],
    packages=find_packages(),
    package_data={},
    entry_points={'console_scripts': [
        'luaprettydoc=luaprettydoc.__main__:main']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux'
    ]
)
