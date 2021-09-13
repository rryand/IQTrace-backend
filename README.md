# IQTrace - Backend

The backend that powers IQTrace, a contact-tracing application for mobile.

# Testing

Testing is powered by `pytest`. To run tests issue the command below:
```
python3 -m pytest tests/
```

# Installation

Make sure you have setup a virtual environment.

1. Install GNU compiler tools and GDB.
```
sudo apt-get install build-essential gdb
```

2. Install the header files and static libraries for python dev.
```
sudo apt-get install python-dev
sudo apt-get install python3-dev
```

3. Install packages from requirements.txt.
```
pip install -r /path/to/requirements.txt
```
