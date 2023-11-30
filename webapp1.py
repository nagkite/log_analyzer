import os
import vertexai
from vertexai import language_models

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/neosu/webapp3/mlproj1-403203-c24f2a45ebd5.json'

# Initialize Vertex AI.

vertexai.init(project="mlproj1-403203", location="us-central1")

# Load the CodeChatModel model from Vertex AI.

chat_model = language_models.CodeChatModel.from_pretrained("codechat-bison")

# Start a chat with the model.

chat = chat_model.start_chat()

# Define the message you want to send.

message = """select * **from table A  and Table B -correct this"""

# Send the message to the model.

response = chat.send_message(message)

# Print the response from the model.

print(f"Response from Model: \n{response.text}")
