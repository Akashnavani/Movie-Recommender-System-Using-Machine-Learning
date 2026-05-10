from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

REPO_NAME = "Movie-Recommender-System-Using-Machine-Learning"
AUTHOR_USER_NAME = "Akashnavani"

LIST_OF_REQUIREMENTS = [
    "streamlit",
    "pandas",
    "numpy",
    "scikit-learn",
    "requests",
    "nltk"
]

setup(
    name="movie-recommender-system",
    version="0.0.1",
    author="Akash Navani",
    author_email="akashnavani25@gmail.com",
    description="Movie Recommender System using Machine Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Akashnavani/Movie-Recommender-System-Using-Machine-Learning",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.8",
    install_requires=LIST_OF_REQUIREMENTS
)