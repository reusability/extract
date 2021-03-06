import setuptools

# open description
with open("README.md", "r", encoding="utf8") as readme_file:
    readme = readme_file.read()

# Gather requirements from requirements.txt
install_reqs = []
requirements_path = "requirements.txt"
with open(requirements_path, "r") as f:
    install_reqs += [
        s
        for s in [line.strip(" \n") for line in f]
        if not s.startswith("#") and s != ""
    ]
requirements = install_reqs
test_requirements = install_reqs

setuptools.setup(
    name="extract",
    version="0.0.1",
    author="lpfloyd",
    author_email="jeevan@arisaedo.org",
    description="BigQuery mining repository",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/reusability/extract",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    # tests_require=test_requirements,
)
