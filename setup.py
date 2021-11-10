from pathlib import Path

from setuptools import find_packages, setup

__package = Path().cwd()
__package_name = __package.name

__read_me = __package / "README.md"
__metadata = (__package / __package_name) / "__init__.py"

__package_info = dict({"version": "", "description": "", "readme": ""})


def read_metadata_info():
    if __read_me.exists():
        with __read_me.open(encoding="utf-8") as file:
            __package_info["readme"] = file.read()

    if __metadata.exists():
        with __metadata.open(encoding="utf-8") as file:
            data = dict(x.split(" = ") for x in file.read().splitlines())

            if "__version__" in data:
                __package_info["version"] = eval(data["__version__"])

            if "__description__" in data:
                __package_info["description"] = eval(data["__description__"])


read_metadata_info()

setup(
    name='luaprettydoc',
    version=__package_info["version"],
    author='TurtleP',
    author_email='jpostelnek@outlook.com',
    license='MIT',
    url='https://github.com/TurtleP/luaprettydoc',
    python_requires='>=3.8.0',
    description=__package_info["description"],
    long_description=__package_info["readme"],
    long_description_content_type='text/markdown',
    install_requires=["toml", "pyyaml"],
    packages=find_packages(),
    package_data={"data": ["*"]},
    entry_points={'console_scripts': [
        'luaprettydoc=luaprettydoc.__main__:main']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux'
    ]
)
