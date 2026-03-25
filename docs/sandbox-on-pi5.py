# 26.07.2025
# workflow on raspberry pi5
# this is by session

# jean  filzenklaswilling
#
# cd sandbox                        // go where the project is
#
# python3.1x -m venv .venv          // if new venv required
#
# git pull                          // get all changes since last pull
# source .venv/bin/activate         // set virtual environment
# pip install -r requirements.txt   // install new libraries (no effect if there aren't)
# pytest                            // run all tests
#

# Upgrading python:
# 
# wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tar.xz
# tar -xf Python-3.13.0.tar.xz
# cd Python-3.13.0
#
# ./configure --enable-optimizations --with-ensurepip=install
# make -j4
#
# sudo make altinstall
#
# python3.13 --version
