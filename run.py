""" Code to run the project """
#! /usr/bin/env python
from s3989748 import app

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
