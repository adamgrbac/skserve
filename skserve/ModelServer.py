from flask import Flask, request, jsonify
import pandas as pd

class ModelServer(Flask):
    def __init__(self,model,pre=lambda x: x,post=lambda x: x):
        # Initialise App with __name__ parameter
        super().__init__(__name__)
        
        self.model = model
        self.pre_process = pre
        self.post_process = post
        
        ### Add Routes
        # Index
        self.add_url_rule('/',view_func=self.hello)
        # Predict
        self.add_url_rule('/predict',view_func=self.predict, methods=['POST'])
    
    def hello(self):
        return "Welcome to ModelServer!"
        
    def predict(self):
        data = request.get_json()
        df = pd.DataFrame(data,index=[0])
        
        # Pre-process data as required
        pre_data = self.pre_process(df)
        
        # Run prediction
        res = self.model.predict(pre_data)
        
        # Post-process prediction as required
        post_res = self.post_process(res)
        
        return jsonify(str(post_res))
        