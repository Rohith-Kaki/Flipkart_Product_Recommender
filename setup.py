from setuptools import find_packages, setup

with open ('requirements.txt', "r") as f:
    requirements = f.read().splitlines()

setup(
    name="flipkart_product_recommendation",
    version=0.1,
    author="rohithKaki",
    packages=find_packages(),
    install_requires=requirements,
)