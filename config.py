import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
ENV = os.getenv('ENV', 'development')
TRAINING_IMAGES_FOLDER = os.getenv('TRAINING_IMAGES_FOLDER', 'training_images')
TEST_DATA_FOLDER = os.getenv("TEST_DATA_FOLDER", "test-data")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "output")
HAARCASCADES_FOLDER = os.getenv('HAARCASCADES_FOLDER', 'Haarcascades/haarcascade_frontalface_default.xml')

# debug = os.getenv('DEBUG')

