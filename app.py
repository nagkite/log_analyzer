from google.cloud import storage
from flask import Flask, request, render_template, jsonify
import os
import json
import vertexai
from vertexai.language_models import CodeChatModel

app = Flask(__name__)

# Configuration settings
class Config:
    PROJECT_ID = "mlproj1-403203"
    LOCATION = "us-central1"
    ALLOWED_EXTENSIONS = {'txt', 'json'}
    UPLOAD_FOLDER = "/tmp"  # Use the writable temp directory provided by Cloud Run
    GCS_BUCKET = "mlproj1"  # Your GCS bucket name

# Ensure the environment variable is set for Google Cloud credentials
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/loganalyzer/mlproj1-403203-c24f2a45ebd5.json'

# Initialize Vertex AI with the project and location
vertexai.init(project=Config.PROJECT_ID, location=Config.LOCATION)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Helper function to analyze error logs using CodeChatModel
def analyze_error_logs(file_path):
    analysis_results = []
    try:
        # Initialize the CodeChatModel
        chat_model = CodeChatModel.from_pretrained("codechat-bison")
        # Start a new chat session
        chat = chat_model.start_chat()
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Send each line to the model for analysis
                response = chat.send_message(f"analyze this -- {line.strip()}")
                analysis_results.append(response.text)
        
        # Convert the results to a JSON string
        results_json = json.dumps(analysis_results)
        return results_json
    except Exception as e:
        return json.dumps({"error": str(e)})

# Function to upload analysis results to GCS bucket
def upload_to_gcs(file_path, content):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(Config.GCS_BUCKET)
    blob = bucket.blob(f"analysis_results/{os.path.basename(file_path)}.json")
    blob.upload_from_string(content)

# Main route to handle file uploads and analysis
@app.route("/", methods=["GET", "POST"])
def handle_main_page():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        file = request.files.get("logFile")
        if file and allowed_file(file.filename):
            filename = file.filename
            # Save the file to the UPLOAD_FOLDER
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Analyze the error logs using the CodeChatModel
            analysis_results_json = analyze_error_logs(file_path)
            
            # Upload the results to GCS
            upload_to_gcs(file_path, analysis_results_json)
            
            # Clean up the temporary file
            os.remove(file_path)
            
            return jsonify(json.loads(analysis_results_json))
        else:
            return jsonify({"error": "Invalid file type or no file uploaded."}), 400

# Run the Flask application
if __name__ == "__main__":
    # Retrieve the port from the PORT environment variable set by Cloud Run
    port = int(os.environ.get('PORT', 8080))
    # Ensure the Flask app listens on all interfaces and the port defined by Cloud Run
    app.run(host='0.0.0.0', port=port, debug=True)
