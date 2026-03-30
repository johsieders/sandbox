# 25.03.2026
# workflow on raspberry pi5
# this is by session

# jean  filzenklaswilling
#
# cd sandbox                        // go where the project is
#
# python3.12 -m venv .venv          // if new venv required
#
# git pull                          // get all changes since last pull
# source .venv/bin/activate         // set virtual environment
# pip install -r requirements.txt   // install new libraries (no effect if there aren't)
# pytest                            // run all tests
#

# Upgrading python:
"""
wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tar.xz
tar -xf Python-3.12.3.tar.xz
cd Python-3.12.3

./configure --enable-optimizations --with-ensurepip=install
make -j4

sudo make altinstall

python3.12 --version
"""source .venv
