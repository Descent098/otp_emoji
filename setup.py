"""
Description:
    Contains all the configuration for the package on pip
"""
import setuptools

def get_content(*filename):
    """ Gets the content of a file and returns it as a string
    Args:
        filename(str): Name of file to pull content from
    Returns:
        str: Content from file
    """
    content = ""
    for current_file in filename:
        with open(current_file, encoding="utf8") as full_description:
            content += full_description.read()
    return content

setuptools.setup(
    name = "otp",
    version = "1.0.1", 
    author = "Kieran Wood", 
    author_email = "kieran@canadiancoding.ca",
    description = "Used to generate 🙊 one-time pads 🤐 exclusively in emojis.",
    long_description = get_content("README.md", "CHANGELOG.md"),
    long_description_content_type = "text/markdown",
    url = "https://github.com/Descent098/otp",
    include_package_data = True,
    install_requires=["docopt"],
    py_modules=["otp", "otp_emojis"],
    entry_points = { 
           'console_scripts': ['otp = otp:main']
       },
    extras_require = {
        "dev" : ["nox",    # Used to run automated processes
                 "pytest", # Used to run the test code in the tests directory
                 "pdoc3"], # Used to generate API documentation

    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)