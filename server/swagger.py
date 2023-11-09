# from flask import Flask
# from flask_restful import Api, Resource
# from flasgger import Swagger

# app = Flask(__name__)
# api = Api(app)
# swagger = Swagger(app)

# # ... (rest of the code remains the same)


# class HelloWorld(Resource):
#     def get(self):
#         """
#         This endpoint returns a simple 'Hello, World!' message.
#         ---
#         responses:
#           200:
#             description: A simple 'Hello, World!' message.
#         """
#         return {'message': 'Hello, World!'}

# api.add_resource(HelloWorld, '/')

# if __name__ == '__main__':
#     app.run(debug=True)
