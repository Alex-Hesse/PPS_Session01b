# HOW TO USE

## First Time in Repo

Choose split

    mkdir docs
    cd docs
    sphinx-quickstart
    sphinx-apidoc -o source/ ../
    
modify conf.py and index.rst to equal to these

    sphinx-build -b html source build


