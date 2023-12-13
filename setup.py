import os
from setuptools import setup
from os import getenv, path, walk


URL = "https://github.com/ravindukathri/ovos-rasa-skill"
SKILL_CLAZZ = "OVOSRasaSkill"  # needs to match __init__.py class name
PYPI_NAME = "ovos-rasa-skill"  # pip install PYPI_NAME 

# below derived from github url to ensure standard skill_id
SKILL_AUTHOR, SKILL_NAME = URL.split(".com/")[-1].split("/")
SKILL_PKG = SKILL_NAME.lower().replace('-', '_')
PLUGIN_ENTRY_POINT = f'{SKILL_NAME.lower()}.{SKILL_AUTHOR.lower()}={SKILL_PKG}:{SKILL_CLAZZ}'
BASE_PATH = path.abspath(path.dirname(__file__))


def find_resource_files():
    resource_base_dirs = ("locale")
    base_dir = path.dirname(__file__)
    package_data = ["*.json"]
    for res in resource_base_dirs:
        if path.isdir(path.join(base_dir, res)):
            for (directory, _, files) in walk(path.join(base_dir, res)):
                if files:
                    package_data.append(
                        path.join(directory.replace(base_dir, "").lstrip('/'),
                                  '*'))
#    print(package_data)
    return package_data


def get_requirements(requirements_filename: str):
    requirements_file = path.join(BASE_PATH, requirements_filename)
    with open(requirements_file, 'r', encoding='utf-8') as r:
        requirements = r.readlines()
    requirements = [r.strip() for r in requirements if r.strip()
                    and not r.strip().startswith("#")]

    for i in range(0, len(requirements)):
        r = requirements[i]
        if "@" in r:
            parts = [p.lower() if p.strip().startswith("git+http") else p
                     for p in r.split('@')]
            r = "@".join(parts)
        if getenv("GITHUB_TOKEN"):
            if "github.com" in r:
                requirements[i] = \
                    r.replace("github.com",
                              f"{getenv('GITHUB_TOKEN')}@github.com")
    return requirements
    

with open("README.md", "r") as f:
    long_description = f.read()

def get_version():
    """Find the version of the package"""
    # Define the version of your skill here
    return "0.1.0"

setup(
    name=PYPI_NAME,
    version=get_version(),
    description='OVOS Skill for Rasa Integration',
    url=URL,  # Replace with your repository URL
    package_dir={SKILL_PKG: ""},
    packages=[SKILL_PKG],
    package_data={SKILL_PKG:find_resource_files()},
    author='Your Name',
    author_email='your.email@example.com',
    license='Apache-2.0',
    zip_safe=True, #
    include_package_data=True,
    install_requires=get_requirements("requirements.txt"),
    long_description="An OVOS skill for integrating with Rasa using Socket.IO",
    long_description_content_type='text/markdown',
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)