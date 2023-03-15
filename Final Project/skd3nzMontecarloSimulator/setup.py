from setuptools import setup

setup(
    name='Monte Carlo Simulator',
    version='1.0.0',
    url='https://github.com/SirishKDesai/FinalProject',
    author='Sirish K Desai',
    author_email='skdn3z@virginia.edu',
    description='MonteCarlo Simulator ',
    packages= ["MonteCarlo", "MontecarloTests"],    
    install_requires=['numpy >= 1.11.1', 'matplotlib >= 1.5.1'],
)