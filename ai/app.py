# app.py
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
# from flask_restx import Resource, Api, reqparse
from celery_worker import process_image
from io import BytesIO

app = Flask(__name__)
# api = Api(app)
app.config['DEBUG'] = False

@app.route('/')
def hello():
    return 'Hello'

@app.route('/image', methods=['GET', 'POST'])
def prediction():
    if (request.method == 'POST'):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"})
        
        file = request.files['file']
        # uuid = request.form['uuid']
        file_bytes = BytesIO(file.read()).getvalue()
        
        # celery worker
        process_image.delay(file_bytes)
        
        return "Image processing started"
    
    elif (request.method == 'GET'):
        return 'AI-server Connect'

# @app.route('/test')
# def index():
#     return 'Hello'

# @api.route('/test')
# class testAPI(Resource):
#     def get(self):
#         return jsonify({"result": "Connect!"})
    
#     def post(self):
#         if 'file' not in request.files:
#             return jsonify({"error": "No file part"})
        
#         file = request.files['file']
#         filename = secure_filename(file.filename)
#         file.save(filename)
        
#         # celery worker
#         task = process_image.delay(filename)
        
#         return jsonify({"result": "Image received", "task_id": str(task.id), "task_state": str(task.state)})

if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=5000)