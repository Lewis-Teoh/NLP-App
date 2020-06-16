import json

from flask import Flask, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

class ModelPredictions(Resource):
    def post(self, param_a):
        try:
            ### INTEGRATION ###
            rdata = [{}]
            response = app.response_class(
                    response=json.dumps(rdata),
                    status=200,
                    mimetype='application/json'
                )
            return response
        except Exception as e:
            print(str(e))
            return Response(status=501)
    
    def get(self):
        try:
            return ("HELLO WORLD")
        except Exception as e:
            print(str(e))
            return Response(status=500)

api.add_resource(ModelPredictions, '/')

if __name__ == "__main__":
    app.run(debug=True)