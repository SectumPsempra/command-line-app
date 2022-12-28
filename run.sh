#!/bin/bash

pip3 install -r requirements.txt
python3 -m app sample_input/input1.txt
python3 -m unittest
python3 -m coverage run -m unittest
python3 -m coverage report -m