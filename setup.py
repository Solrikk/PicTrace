from setuptools import setup, find_packages

setup(
    name='pictrace',
    version='1.0.12',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi>=0.106.0',
        'uvicorn>=0.24.0',
        'tensorflow>=2.16.1',
        'pillow>=9.0.0',
        'numpy>=1.21.0',
        'jinja2>=3.0.0',
        'python-multipart'
    ],
)
