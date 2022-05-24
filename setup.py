import setuptools

setuptools.setup(
    name="normantle",
    packages=setuptools.find_packages(),
    version="1.0.0",
    author="LBlend",
    description="Semantle, på norsk!",
    url="https://github.com/LBlend/normantle",
    install_requires=["fastapi", "uvicorn[standard]", "gensim"],
    python_requires=">=3.10",
)
