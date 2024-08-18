import pathlib
import setuptools

setuptools.setup(
    name="sqrl_python_interface",
    version="0.1.0",
    description="A python package that bridges the gap between the SQRL-TournamentRunner and various rocket league python bots",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="JoshyDev",
    project_urls= {
        "Source": "https://github.com/JoshyDevRL/sqrl_python_interface",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10",

)