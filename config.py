import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
TRAINING_IMAGES = os.getenv('TRAINING_IMAGES', 'training_images')
# debug = os.getenv('DEBUG')

