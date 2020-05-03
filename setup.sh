#!/bin/bash
pip3 install -r requirements.txt
python3 lib/PyRep/setup.py install
python3 lib/RLBench/setup.py install
python3 lib/keras-rl2/setup.py install
