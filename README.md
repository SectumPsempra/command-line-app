# Pre-requisites
* Python 3.8/3.9
* Pip

# How to run the code

I have provided scripts to execute the code. 

Use `run.sh` if you are Linux/Unix/macOS Operating systems and `run.bat` if you are on Windows.  Both the files run the commands silently and prints only output from the input file `sample_input/input1.txt`. You are supposed to add the input commands in the file from the appropriate problem statement. 

Internally both the scripts run the following commands 

* `pip install -r requirements.txt` - This will install the dependencies mentioned in the requirement.file
* `python3 -m geektrust sample_input/input1.txt` - This will run the solution passing in the sample input file as the command line argument

# Running the code for multiple test cases

Please fill `input1.txt` and `input2.txt` with the input commands and use those files in `run.bat` or `run.sh`. Replace `python3 -m geektrust sample_input/input1.txt` with `python3 -m geektrust sample_input/input2.txt` to run the test case from the second file. 

# How to execute the unit tests

`python3 -m unittest` will execute the unit test cases when running from the main app folder.

# Coverage

To get coverage on the unit tests, please run the following command from the main app folder:

`python3 -m coverage run -m unittest`</br></br>
`python3 -m coverage report -m`
    
</br>
    
    Name                  Stmts   Miss  Cover   Missing
    ---------------------------------------------------
    config/__init__.py        0      0   100%
    config/config.py          7      0   100%
    src/__init__.py           0      0   100%
    src/add.py               14      0   100%
    src/allot.py             27      0   100%
    src/cancel.py            19      0   100%
    src/constants.py         22      0   100%
    src/register.py          27      0   100%
    tests/__init__.py         0      0   100%
    tests/test.py           134      8    94%   118, 137, 145, 150-151, 170, 181, 184
    utils/__init__.py         0      0   100%
    utils/exceptions.py       4      0   100%
    utils/utils.py           73     19    74%   15-16, 27-28, 36, 50, 80-92, 95-96
    ---------------------------------------------------
    TOTAL                   327     27    92%


# Author

You can find this code on my github <a href="https://github.com/SectumPsempra/command-line-app">repository</a> as well.
