# My Bits - Server

Setting up your virtual environment
```
sudo pip install virtualenv
mkdir ~/Virtualenvs
cd ~/Virtualenvs
virtualenv mybits
```

Starting the server
```
git clone git@github.com:raccoonz-ninja/my-bits-server.git
cd my-bits-server
source ~/Virtualenvs/mybits/bin/activate # Activate the virtual environment
pip install -r requirements.txt # Install the required dependencies
python -m app.db.core.init # Initialize the database
python main.py # Starts the server
```

Add this to your .bash_profile to never forget your virtual environment
```
# pip should only run if there is a virtualenv currently activated
export PIP_REQUIRE_VIRTUALENV=true
```

Runs on Python 2.7.10

The default configuration lives in [config.json](config.json)
