# skserve - A Flask API wrapper for deploying sklearn models

#### Created by Adam Grbac.

This package uses Flask to create an easy frame to deploy existing Machine Learning models created in scikit-learn, and expose them via a RESTful API.

The main object of this package is the ModelServer class, which is a subclass of the Flask class, and can therefore be treated & customised the same way as a regular Flask server instance.

### Usage

#### Basic

To use this package, start by creating a scikit-learn model (or a model type that has a similar predict / predict_proba API to that of sklearn).

Once the model is trained, use the dump() function from the joblib module to save the model as a file.

One you have a model file that you would like to deploy e.g. A simple logistic regression model with 7 inputs - logreg.model, the following code is an example of a barebones deployment:

```
from skserve import ModelServer
from joblib import load

model = load('logreg.model')

app = ModelServer(model=model)

if __name__ == "__main__":
    app.run()
```

This code will start a Flask API on 127.0.0.1:5000 with the following routes:

* '/' : The root of the server will return a small welcome message and can be used to test connectivity.
* '/help': The help route packages up and documentation supplied to the API i.e. An input data dictionary & any Docstrings that exist in the pre/post processing functions.
* '/predict': The predict route invokes the predict method of the model being deployed by being sent a POST request. The request should include data as a JSON object with the feature names and values.
* '/predict_proba': The predict_proba route invokes the predict_proba method of the model being deployed by being sent a POST request. The request should include data as a JSON object with the feature names and values.

To solicit a prediction from the model, we send a POST request to the /predict route with a JSON object as data, which contains the 7 required fields:

```
curl -d {"""Age""":42,"""Fare""":52.00,"""Sex""":"""male""","""Parch""":2,"""Pclass""":1,"""SibSp""":2} -H "Content-Type: application/json" 127.0.0.1:5000/predict
```

#### Advanced

The ModelServer class can also be initialised with other parameters:

* pre : A preprocessing function which takes a pandas DataFrame of the data passed in with the POST request and should return a similar DataFrame that the model can accept.
* post : A postprocessing function which takes the results of model scoring (a list) and will be returned as the "scores" element of a JSON object as a response to the initiating POST request.
* data_dict : A dictionary that maps feature names to descriptions of the features. This dictionary is used as part of the /help route (for users information) as well as ordering the data for the model (so POST data does not need to be in order).

The Host and Port of the server can also be changed by passing host & port parameters to the run() function.

An example of the above extensions to the base functionality is shown below:

```
from skserve import ModelServer
from joblib import load

model = load('logreg.model')

data_dict = {"Pclass":"Passenger Class",
            "Age":"Passenger Age",
            "Fare":"Fare Paid",
            "Parch":"Parents / Children",
            "SibSp":"Siblings",
            "Sex":"Gender Code - 0: Male - 1: Female"}

def pre_process(data):
    """Pre-Processor:
    
    This should show up on the help page.
	
	The function changes the string into a Binary value."""
    data["Sex"] = data["Sex"].apply(lambda x: 0 if x == "male" else 1)
    return data
    
def post_process(data):
    """Post-Processer:
    
    This should also show up on the help page.
	
	This function takes the scores, and shifts from 0 <-> 1 to -1 <-> 1"""
    return(data*2 - 1)
    
app = ModelServer(model=model,
                  pre=pre_process,
                  post=post_process,
                  data_dict=data_dict)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1337)
```


These changes will also make an impact on the page returned on the /help route e.g.:

```
SSSSS K   K SSSSS EEEEE RRRRR V   V EEEEE
S     K  K  S     E     R   R V   V E
SSSSS KKK   SSSSS EEEEE RRRRR V   V EEEEE
    S K  K      S E     R RR   V V  E
SSSSS K   K SSSSS EEEEE R   R   V   EEEEE

This model API can be used to predict outputs (Regression + Classification) or probabilities (Classification).

These are accessed by sending a POST request to <host>/predict or <host>/predict_proba respectively.

The input data should be a JSON object with the following fields:

Pclass: Passenger Class
Age: Passenger Age
Fare: Fare Paid
Parch: Parents / Children
SibSp: Siblings
Sex: Gender Code - 0: Male - 1: Female

The data sent will be pre-processed using a pre-defined function:

Pre-Processor:

    This should show up on the help page
The model results will be post-processed using a pre-defined function:

Post-Processer:

    This should also show up on the help page
```