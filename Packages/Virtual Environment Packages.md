## Conda Virtual Environment Packages

When creating the virtual environment ran into an issue of a package not being recognised when installing through 'conda install'. The below link suggested installing pip 
first through conda, navigate to virtual_portfolio_env/bin then using pip install yfinance. Now it was already a package installed in my conda application, just not 
explicitly in this virtual environment, therefore the last command I used was'conda install -n virtual_portfolio_env yfinance'

https://stackoverflow.com/questions/41060382/using-pip-to-install-packages-to-anaconda-environment

- updating virtual environment config.yaml afterwards

use https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

-