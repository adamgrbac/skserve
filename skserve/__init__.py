"""
skserve
=======

This package implements the ModelServer class, which extends the Flask
class from flask with the specific purpose of serving a pickled sklearn
model through a RESTful API.

See the ModelServer.py docstring for specific documentation of
parameters and methods of the ModelServer class.

Example usage of the package & class:

    >>> from skserve import ModelServer
    >>> from joblib import load
    >>> 
    >>> model = load("path/to/model.pkl")
    >>> server = ModelServer(model)
    >>>
    >>> if __name__ == "__main__":
    >>>     server.run()
    
The above example takes a model file, pickled using joblib.dump(), and
serves it as a RESTful API on 127.0.0.1:5000 (by default).

The class implements a default route that serves up a lite welcome page
as well as a "predict" route that can be POSTed to in order to solicit 
a prediction from the model.

The API accepts a JSON data packet and returns an array with as many 
output elements as the model predicts for e.g. 1 for a simple
classification problem.
"""
from skserve.ModelServer import ModelServer