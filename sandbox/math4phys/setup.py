from setuptools import setup

setup(
    name="math4phys",
    version="0.1.0",
    packages=["math4phys"],
    # Package will be created from current dir                                                                                                    
    package_dir={"math4phys": "."},
    # Current dir becomes the package                                                                                                     
    install_requires=["sympy"],
)
