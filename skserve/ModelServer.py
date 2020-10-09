from flask import Flask, request, jsonify
import pandas as pd


class ModelServer(Flask):
    def __init__(self,
                 model,
                 pre=lambda x: x,
                 post=lambda x: x,
                 data_dict=None):
        """ 
        __init__ function:
        
        This initialises the Flask server using the parent init
        function, with the __name__ parameter as recommended in the
        flask documentation.
        
        The function also sets the appropriate class members and adds
        the routes for root, predict & predict_proba paths.
        
        Inputs:
        
        model: The sklearn model file, usually loaded using joblib.load()
        pre: A function that is applied to the incoming data from POST
             requests. N.B. (1) The data will be structured as a Pandas
             DataFrame and should be treated as such (2) Any re-ordering
             of features will need to be corrected as part of this 
             function to ensure the final order is the same as the model
             being used.
        post: A function that is applied to the predictions of the model.
              N.B. (1) The predictions will be in the form of a list. (2)
              The post function is applied to both class predictions AND
              probabilities.
        data_dict: A dictionary that should map the input fields for the
                   model (in the correct order) to a description of the 
                   field (optional: for documentation and help purposes)
        """
        
        super().__init__(__name__)
        
        # Check that model class has a predict methods
        if "predict" not in dir(model):
            raise Exception('Error: Model is missing predict method')
        
        # Set class attributes
        self.model = model
        self.pre_process = pre
        self.post_process = post
        self.data_dict = data_dict

        # Add Default Routes
        
        # Index
        self.add_url_rule('/', view_func=self.hello)
        
        # Predict
        self.add_url_rule('/predict', view_func=self.predict, methods=['POST'])
        
        # Predict Probabilities (for Classification)
        if "predict_proba" in dir(model):
            self.add_url_rule('/predict_proba', view_func=self.predict_proba, methods=['POST'])
            
        # Help
        self.add_url_rule('/help', view_func=self.help)
            
        # Register Custom Error Handler
        self.register_error_handler(404, self.handle_404)
    
    @staticmethod
    def hello():
        """Hello!
        
        A simple function that returns a text blurb when the user sends
        a GET request to the root '/'."""
        return "Welcome to ModelServer! Servings up models in a Flask since 2020."
        
    def predict(self):
        """Predict

        This function takes the data from a POST request (in JSON format)
        and:

        1) Runs it through the pre-processing function (if supplied)
        2) Runs the pre-processed data through the model
        3) Runs and returns the predictions through the post-processing 
           function (if supplied)"""

        data = request.get_json()

        # If data dictionary exists, use keys to order columns of POST data
        if self.data_dict is None:
            df = pd.DataFrame(data, index=[0])
        else:
            df = pd.DataFrame(data, index=[0], columns=self.data_dict.keys())
            
        # Pre-process data as required
        pre_data = self.pre_process(df)
        
        # Run prediction
        res = self.model.predict(pre_data)
        
        # Post-process prediction as required
        post_res = self.post_process(res)
        
        return jsonify(scores=post_res[0].tolist())
    
    def predict_proba(self):
        """Predict Probabilities

        This function takes the data from a POST request (in JSON format)
        and:

        1) Runs it through the pre-processing function (if supplied)
        2) Runs the pre-processed data through the model
        3) Runs and returns the proba scores through the post-processing 
           function (if supplied)"""
        data = request.get_json()
        
        # If data dictionary exists, use keys to order columns of POST data
        if self.data_dict is None:
            df = pd.DataFrame(data, index=[0])
        else:
            df = pd.DataFrame(data, index=[0], columns=self.data_dict.keys())
        
        # Pre-process data as required
        pre_data = self.pre_process(df)
        
        # Run prediction
        res = self.model.predict_proba(pre_data)
        
        # Post-process prediction as required
        post_res = self.post_process(res)
        
        return jsonify(scores=post_res[0].tolist())

    def help(self):
        """Help
        
        This function defines the contents of the /help route of the server.
        
        The page will contain the input data dictionary (if supplied), 
        the docstring for the preprocessing function (if supplied) and the
        docstring for the preprocessing function (if supplied)."""
        
        help_string = """\
SSSSS K   K SSSSS EEEEE RRRRR V   V EEEEE
S     K  K  S     E     R   R V   V E
SSSSS KKK   SSSSS EEEEE RRRRR V   V EEEEE
    S K  K      S E     R RR   V V  E
SSSSS K   K SSSSS EEEEE R   R   V   EEEEE"""
        help_string += """\n\nThis model API can be used to predict outputs (Regression + Classification) or\
probabilities (Classification).

These are accessed by sending a POST request to <host>/predict or <host>/predict_proba respectively."""
        if self.data_dict is not None:
            help_string += "\n\nThe input data should be a JSON object with the following fields:\n\n"
            for k, v in self.data_dict.items():
                help_string += k + ": " + v + "\n"
        if self.pre_process.__doc__ is not None:
            help_string += "\nThe data sent will be pre-processed using a pre-defined function:\n\n"
            help_string += self.pre_process.__doc__
        if self.post_process.__doc__ is not None:
            help_string += "\nThe model results will be post-processed using a pre-defined function:\n\n"
            help_string += self.post_process.__doc__
        return help_string, 200, {"Content-Type": "text/html"}

    def handle_404(self, e):
        """Handle 404
        
        This function constructs a default response to 404 errors"""
        return "Uh-oh... this page doesn't exist!", 404
