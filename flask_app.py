import random
from flask import Flask, request, jsonify, send_file, url_for, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug.utils import secure_filename
import json
import os
from tester import identify_face
from config import TRAINING_IMAGES_FOLDER, TEST_DATA_FOLDER, OUTPUT_FOLDER, ENV
from data_augmentation import create_augmented_images


app = Flask(__name__)
CORS(app)

# localhost
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), TRAINING_IMAGES_FOLDER)




# Hosting
# app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'face_recognition/training_images')
engine = create_engine('sqlite:///mydb.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    contact = Column(String)
    course = Column(String)
    section = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'contact': self.contact,
            'course': self.course,
            'section': self.section,
            'date_created': self.date_created
        }
    

class StudentsImages(Base):
    __tablename__ = 'students_images'
    id = Column(Integer, primary_key=True)
    studentID = Column(Integer)
    filename = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)



Base.metadata.create_all(engine)


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # If the object is a SQLAlchemy class, return a dictionary of its properties
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # Check if the field value can be converted to JSON
                    fields[field] = data
                except TypeError:
                    if isinstance(data, datetime):
                        fields[field] = data.isoformat()
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)

REQUIRED_FIELDS = ['name', 'email', 'contact', 'course','section']

@app.route('/')
def index():
    return 'Hello, World!'

from sqlalchemy import func

@app.route('/students', methods=['GET'])
def get_all_students():
    """_summary_

    Returns:
        students: object
        
        {
            "students": [
                		{
                            "contact": "1234567890",
                            "course": "B.Tech",
                            "date_created": "Sat, 18 Feb 2023 04:04:39 GMT",
                            "email": "example@email.com",
                            "id": 1,
                            "image": "http://localhost:5000/static/training_images/1/28519elon7.jpg",
                            "name": "Ellon Musk",
                            "section": "A"
                        }
            ]
        }
        
    """
    session = Session()
    students = session.query(Students, func.min(StudentsImages.id).label('id'))\
        .outerjoin(StudentsImages, Students.id == StudentsImages.studentID)\
        .group_by(Students.id).all()
    # The above query retrieves all students, and the minimum image ID for each student, using a left outer join
    # on the Students and StudentsImages tables. We group the result by the student ID.

    results = []
    for student, image_id in students:
        student_dict = student.__dict__
        if image_id:
            image = session.query(StudentsImages).filter_by(id=image_id).one()
            student_dict['image'] = image.filename
        else:
            student_dict['image'] = None
        results.append(student_dict)
    
    for item in results:
        # delete the _sa_instance_state key
        del item['_sa_instance_state']
        
        if item['image'] is not None:
            item['image'] = url_for('get_training_image',id=item['id'], filename=item['image'], _external=True)
    
    return jsonify({'students': results}), 200




@app.route('/students', methods=['POST'])
def add_students():
    """
    Accepts a JSON object with the following fields:

    {
        "name": "John Doe",
        "email":"example@email.com",
        "contact":"1234567890",
        "course":"B.Tech",
        "section":"A"
    }
    Returns:
        _type_: _description_
    """
    data = request.get_json()

    # Check if data contains all data required
    if all(field in data for field in REQUIRED_FIELDS):
        session = Session()
        new_student = Students(name=data['name'], email=data['email'], contact=data['contact'], course=data['course'], section=data['section'])
        session.add(new_student)
        session.commit()
        return jsonify({'success': 'Student added successfully!'}), 200

    else:
        missing_keys = [key for key in REQUIRED_FIELDS if key not in data]
        error_msg = f"Missing required keys: {', '.join(missing_keys)}"
        return jsonify({'error': 'Missing data!', "msg":error_msg}), 400

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    session = Session()
    student = session.query(Students).filter(Students.id==id).first()
    if student is None:
        return jsonify({'error': 'Student not found!'}), 404
    return json.dumps(student, cls=AlchemyEncoder)

# Delete a student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    session = Session()
    student = session.query(Students).filter(Students.id==id).first()
    if student is None:
        return jsonify({'error': 'Student not found!',"studentID":id}), 404
    session.delete(student)
    session.commit()
    return jsonify({'success': 'Student deleted successfully!',"studentID":id}), 200


@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    session = Session()
    student = session.query(Students).filter(Students.id==id).first()

    if student is None:
        return jsonify({'error': 'Student not found!',"studentID": id}), 404

    data = request.json
    if 'name' in data:
        student.name = data['name']
    if 'email' in data:
        student.email = data['email']
    if 'contact' in data:
        student.contact = data['contact']
    if 'course' in data:
        student.course = data['course']
    if 'section' in data:
        student.section = data['section']

    session.commit()

    updated_student = session.query(Students).filter(Students.id==id).first()
    return json.dumps(updated_student, cls=AlchemyEncoder)

@app.route('/students/<int:id>/images', methods=['GET'])
def get_student_images(id):
    session = Session()
    student_images = session.query(StudentsImages).filter_by(studentID=id).all()
    if not student_images:
        return jsonify({'error': 'No images found for student ID'}), 404

    image_files = []
    for image in student_images:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], str(image.studentID), image.filename)
        if os.path.isfile(image_path):
            image_files.append(image_path)

    if not image_files:
        return jsonify({'error': 'Images not found on server'}), 404

    # If only one image is found, return it as an attachment
    # if len(image_files) == 1:
    #     return send_file(image_files[0], as_attachment=True)

    # If multiple images are found, return them as part of the response
    response_data = []
    base_url = request.host_url

    for image_path in image_files:
        filename = os.path.basename(image_path)
        
        if (ENV == 'development'):
            url = url_for('static', filename='training_images/' + str(id) + '/' + filename)
        else:
            url = url_for('static', filename= str(id) + '/' + filename)
        
        response_data.append({
            'filename': filename,
            'data': base_url + url
        })

    print(response_data)
    return json.dumps(response_data, cls=AlchemyEncoder)
    # Return the images as attachments

@app.route('/training_images', methods=['GET'])
def get_all_training_images():
    session = Session()
    student_images = session.query(StudentsImages).all()
    return json.dumps(student_images, cls=AlchemyEncoder)

@app.route('/student/training_images/<int:id>', methods=['GET'])
def get_training_image_student(id):
    session = Session()

    training_images = session.query(StudentsImages).filter(StudentsImages.id==id).all()
    response_data = []
    base_url = request.host_url
    for image in training_images:
        print(image.filename)
        # filename = os.path.basename(image.filename)

        # if (ENV == 'development'):
        #     url = os.path.join(app.config['UPLOAD_FOLDER'], str(image.studentID), image.filename)
        # else:
        #     url = url_for('static', filename= str(id) + '/' + image.filename)
        
        filename = os.path.basename(image.filename)
        
        if (ENV == 'development'):
            url = url_for('static', filename='training_images/' + str(id) + '/' + filename)
        else:
            url = url_for('static', filename= str(id) + '/' + filename)
        # Convert to string the image.date_created
        
        
           
        print(image.date_created)
        response_data.append({
            'id': image.id,
            'name': image.filename,
            'filename': image.filename,
            'date_created': str(image.date_created),
            'studentID': image.studentID,
            'url':base_url + url
        })

    return json.dumps(response_data, cls=AlchemyEncoder)

@app.route('/upload/<int:id>', methods=['POST'])
def upload_images(id):
    session = Session()
    student = session.query(Students).filter(Students.id==id).first()

    if student is None:
        return jsonify({'error': 'Student not found!', 'studentID': id}), 404

    if 'images' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    images = request.files.getlist('images')

    folder_path = os.path.join(TRAINING_IMAGES_FOLDER, str(id))

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for image in images:
        # Check the image size
        if len(image.read()) > 1024 * 1024:  # 1MB in bytes
            return jsonify({'error': 'Image size must be 1MB or less!'}), 400
        image.seek(0)  # Reset the file pointer to the beginning

        # Save the image to the folder
        randomID = random.randint(1,100000)
        filename = secure_filename(str(randomID)+(image.filename))
        filepath = os.path.join(folder_path, filename)
        image.save(filepath)

        create_augmented_images(filepath,folder_path,randomID)

        # Save the image to the database
        new_image = StudentsImages(studentID=id, filename=filename)
        session.add(new_image)
        session.commit()

    return jsonify({'success': 'Images uploaded successfully!', 'studentID': id}), 200


@app.route('/recognize', methods=['POST'])
def recognize():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    image = request.files['image']

    # Check if test-data is available if not create it
    if not os.path.exists(TEST_DATA_FOLDER):
        os.makedirs(TEST_DATA_FOLDER)

    # Save the image to the folder
    randomID = random.randint(1,100000)
    filename = secure_filename(str(randomID)+'.jpg')
    filepath = os.path.join(TEST_DATA_FOLDER, filename)
    image.save(filepath)


    session = Session()
    list_of_students = session.query(Students).all()
    # Create an Array with Student Names Output 
    student_obj = {0:'Elon Musk'}
    
    for each_student in list_of_students:
        print(each_student)
        student_obj[each_student.id] = each_student.name
        
        
    # Recognize the student
    output, label = identify_face(filepath, student_obj)
    output_obj = {}
    output_obj['url'] = url_for('get_output_image', filename=output, _external=True)
    output_obj['label'] = label
    
    
    # Get student details from database key = label
    
    session = Session()
    student = session.query(Students).filter(Students.id==label).first()
    student_obj = {
        'id': student.id,
        'name': student.name,
        'email': student.email,
        'contact': student.contact,
        'course': student.course,
        'section': student.section,
        'date_created': student.date_created,
    }
    
    return jsonify({'success': 'Image recognized successfully!', 'output': output_obj, 'student':student_obj}), 200

@app.route('/static/get_output/<filename>')
def get_output_image(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/static/training_images/<int:id>/<filename>')
def get_training_image(id, filename):
    os.path.join(TRAINING_IMAGES_FOLDER, str(id))
    return send_from_directory(os.path.join(TRAINING_IMAGES_FOLDER, str(id)), filename)

if __name__ == '__main__':
    app.run(debug=True)