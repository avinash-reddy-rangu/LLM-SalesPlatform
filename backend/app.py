from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pymongo
from datetime import datetime
import uuid
from bcrypt import hashpw, gensalt, checkpw
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

# MongoDB configuration
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sdh"]
file_collection = db["files"]
user_collection = db["users"]
prompt_collection = db["prompts"]

# Upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def save_file(file):
    filename = secure_filename(file.filename)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_id + "_" + filename)

    file.save(file_path)

    file_data = {
        "file_id": file_id,
        "file_path": file_path,
        "file_name": str(filename),
        "created_timestamp": datetime.utcnow(),
        "is_deleted": False
    }

    file_collection.insert_one(file_data)
    if '_id' in file_data:
        del file_data['_id']
    return file_data


@app.route('/upload', methods=['POST'])
@swag_from({
    'tags': ['File Operations'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'The file to upload'
        }
    ],
    'responses': {
        '201': {
            'description': 'File uploaded successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'file_id': {'type': 'string'},
                    'file_path': {'type': 'string'},
                    'file_name': {'type': 'string'},
                    'created_timestamp': {'type': 'string'},
                    'is_deleted': {'type': 'boolean'}
                }
            }
        }
    }
})
def upload_file():
    """
    Upload a single file
    ---
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_data = save_file(file)

    return jsonify(file_data), 201


@app.route('/upload/multi', methods=['POST'])
@swag_from({
    'tags': ['File Operations'],
    'parameters': [
        {
            'name': 'files',
            'in': 'formData',
            'type': 'array',
            'items': {
                'type': 'file'
            },
            'required': True,
            'description': 'The files to upload'
        }
    ],
    'responses': {
        '201': {
            'description': 'Files uploaded successfully',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'file_id': {'type': 'string'},
                        'file_path': {'type': 'string'},
                        'file_name': {'type': 'string'},
                        'created_timestamp': {'type': 'string'},
                        'is_deleted': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def upload_multiple_files():
    """
    Upload multiple files
    ---
    """
    if 'files' not in request.files:
        return jsonify({"error": "No files part in the request"}), 400

    files = request.files.getlist('files')

    if not files:
        return jsonify({"error": "No selected files"}), 400

    file_data_list = []

    for file in files:
        if file and file.filename != '':
            file_data = save_file(file)
            file_data_list.append(file_data)

    return jsonify(file_data_list), 201


@app.route('/files', methods=['GET'])
@swag_from({
    'tags': ['File Operations'],
    'responses': {
        '200': {
            'description': 'List of all files',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'file_id': {'type': 'string'},
                        'file_path': {'type': 'string'},
                        'file_name': {'type': 'string'},
                        'created_timestamp': {'type': 'string'},
                        'is_deleted': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def get_files():
    """
    Get all files
    ---
    """
    files = file_collection.find({"is_deleted": False})
    file_list = []

    for file in files:
        file['_id'] = str(file['_id'])  # Convert ObjectId to string for JSON serialization
        file_list.append(file)

    return jsonify(file_list), 200


@app.route('/signup', methods=['POST'])
@swag_from({
    'tags': ['User Operations'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'name': {'type': 'string'},
                    'role': {'type': 'string'},
                    'branch': {'type': 'string'},
                    'age': {'type': 'integer'},
                    'password': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'User created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'banker_id': {'type': 'string'}
                }
            }
        },
        '400': {
            'description': 'User already exists or missing required fields'
        }
    }
})
def signup():
    """
    Signup a new user
    ---
    """
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    role = data.get('role')
    branch = data.get('branch')
    age = data.get('age')
    password = data.get('password')

    if not all([email, name, role, branch, age, password]):
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = user_collection.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    banker_id = str(uuid.uuid4())

    user_data = {
        "banker_id": banker_id,
        "email": email,
        "name": name,
        "role": role,
        "branch": branch,
        "age": age,
        "password": hashed_password,
        "created_timestamp": datetime.utcnow()
    }

    user_collection.insert_one(user_data)

    return jsonify({"message": "User created successfully", "banker_id": banker_id}), 201


@app.route('/signin', methods=['POST'])
@swag_from({
    'tags': ['User Operations'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'banker_id': {'type': 'string'},
                    'name': {'type': 'string'}
                }
            }
        },
        '400': {
            'description': 'Missing email or password'
        },
        '401': {
            'description': 'Invalid email or password'
        }
    }
})
def signin():
    """
    Sign in a user
    ---
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    user = user_collection.find_one({"email": email})
    if not user or not checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "banker_id": user['banker_id'], "name": user['name']}), 200


@app.route('/banker/<banker_id>', methods=['GET'])
@swag_from({
    'tags': ['User Operations'],
    'parameters': [
        {
            'name': 'banker_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The ID of the banker to retrieve'
        }
    ],
    'responses': {
        '200': {
            'description': 'Banker details retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'banker_id': {'type': 'string'},
                    'email': {'type': 'string'},
                    'name': {'type': 'string'},
                    'role': {'type': 'string'},
                    'branch': {'type': 'string'},
                    'age': {'type': 'integer'},
                    'created_timestamp': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'Banker not found'
        }
    }
})
def get_banker(banker_id):
    """
    Get banker details by ID
    ---
    """
    user = user_collection.find_one({"banker_id": banker_id})

    if not user:
        return jsonify({"error": "Banker not found"}), 404

    user['_id'] = str(user['_id'])  # Convert ObjectId to string for JSON serialization
    user.pop('password', None)  # Remove password field from the response

    return jsonify(user), 200


@app.route('/prompt', methods=['POST'])
@swag_from({
    'tags': ['Prompt Operations'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'role': {'type': 'string'},
                    'tone': {'type': 'string'},
                    'instructions': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Prompt saved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'prompt_id': {'type': 'string'}
                }
            }
        },
        '400': {
            'description': 'Missing required fields'
        }
    }
})
def save_prompt():
    """
    Save a new prompt
    ---
    """
    data = request.get_json()
    role = data.get('role')
    tone = data.get('tone')
    instructions = data.get('instructions')

    if not all([role, tone, instructions]):
        return jsonify({"error": "Missing required fields"}), 400

    prompt_id = str(uuid.uuid4())

    prompt_data = {
        "prompt_id": prompt_id,
        "role": role,
        "tone": tone,
        "instructions": instructions,
        "created_timestamp": datetime.utcnow()
    }

    prompt_collection.insert_one(prompt_data)

    return jsonify({"message": "Prompt saved successfully", "prompt_id": prompt_id}), 201


@app.route('/prompt/<prompt_id>', methods=['GET'])
@swag_from({
    'tags': ['Prompt Operations'],
    'parameters': [
        {
            'name': 'prompt_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The ID of the prompt to retrieve'
        }
    ],
    'responses': {
        '200': {
            'description': 'Prompt details retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'prompt_id': {'type': 'string'},
                    'role': {'type': 'string'},
                    'tone': {'type': 'string'},
                    'instructions': {'type': 'string'},
                    'created_timestamp': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'Prompt not found'
        }
    }
})
def get_prompt(prompt_id):
    """
    Get prompt details by ID
    ---
    """
    prompt = prompt_collection.find_one({"prompt_id": prompt_id})

    if not prompt:
        return jsonify({"error": "Prompt not found"}), 404

    prompt['_id'] = str(prompt['_id'])  # Convert ObjectId to string for JSON serialization

    return jsonify(prompt), 200


@app.route('/prompts', methods=['GET'])
@swag_from({
    'tags': ['Prompt Operations'],
    'responses': {
        '200': {
            'description': 'List of all prompts',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'prompt_id': {'type': 'string'},
                        'role': {'type': 'string'},
                        'tone': {'type': 'string'},
                        'instructions': {'type': 'string'},
                        'created_timestamp': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_all_prompts():
    """
    Get all prompts
    ---
    """
    prompts = prompt_collection.find()
    prompt_list = []

    for prompt in prompts:
        prompt['_id'] = str(prompt['_id'])  # Convert ObjectId to string for JSON serialization
        prompt_list.append(prompt)

    return jsonify(prompt_list), 200


if __name__ == '__main__':
    app.run(debug=True)
