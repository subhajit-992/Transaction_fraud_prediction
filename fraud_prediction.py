from creditcard.logger import logging
from creditcard.exception import CreditCardsException
from creditcard.pipeline.batch_prediction import CreditCardBatchPrediction
from flask import Flask, request, jsonify
import json
import pandas as pd


class MyFlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.prediction_results = {}

        @self.app.route('/predict', methods=['POST'])
        def predict():
            try:
                # Receive transaction data as JSON 
                transaction_data = request.get_json()
                #data = json.loads(transaction_data)
                df = pd.DataFrame(transaction_data, index=[0])

                # Perform fraud prediction (replace with your actual prediction logic)
                # For this example, we'll just return a random prediction (0 for legitimate, 1 for fraudulent)
                #prediction=0 if df.amount.values[0]<100 else 1
                credit_card_batch_prediction = CreditCardBatchPrediction(data=df)
                prediction = credit_card_batch_prediction.start_prediction()


                # Store the prediction result
                self.prediction_results[transaction_data.get('id')] = prediction

                # Return the prediction result
                return jsonify({"prediction": prediction})
        
            except Exception as e:
                return jsonify({"error":str(e)}), 500
            
        # Endpoint for retrieving prediction results
        @self.app.route('/get_prediction/<id>', methods=['GET'])
        def get_prediction(id):
            try:
                # Retrieve the prediction result for a specific transaction
                prediction = self.prediction_results.get('id', -1)  # -1 indicates no prediction available

                return jsonify({"prediction": prediction})

            except Exception as e:
                return jsonify({"error": str(e)}), 500
    def run(self):
        self.app.run(debug=True)


#if __name__ == '__main__':
    #app_1 = MyFlaskApp()
    #app_1.run()