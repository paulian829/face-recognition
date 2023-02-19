# face-recognition

# Endpoints

## Students

1. GET /students
get all students

```
{
	"students": [
		{
			"contact": "1234567890",
			"course": "B.Tech",
			"date_created": "Sun, 19 Feb 2023 08:40:47 GMT",
			"email": "example@email.com",
			"id": 1,
			"image": null,
			"name": "John Doe",
			"section": "A"
		}
	]
}
```

2. POST /students
add a new student to the list

input 
```
    {
        "name": "John Doe",
        "email":"example@email.com",
        "contact":"1234567890",
        "course":"B.Tech",
        "section":"A"
    }
```

result
```
{
	"success": "Student added successfully!"
}
```

3. PUT /students/<student id>
Update the student details

input
```
    {
        "name": "Elon Musk",
        "email":"example@email.com",
        "contact":"1234567890",
        "course":"B.Tech",
        "section":"A"
    }
```

output
```
{
    {
	"contact": "1234567890",
	"course": "B.Tech",
	"date_created": "2023-02-19T08:40:47.299280",
	"email": "example@email.com",
	"id": 1,
	"name": "Elon Musk",
	"registry": null,
	"section": "A",
	"to_dict": null
    }
}
```

4. DELETE /students/<student id>

output
```
{
	"studentID": 2,
	"success": "Student deleted successfully!"
}
```

## Training Images

1. GET /training_images
Get all the images uploaded
output
```
[
	{
		"date_created": "2023-02-19T08:49:04.461436",
		"filename": "91661elon5.jpg",
		"id": 1,
		"registry": null,
		"studentID": 1
	},
	{
		"date_created": "2023-02-19T08:49:11.037260",
		"filename": "37522elon7.jpg",
		"id": 2,
		"registry": null,
		"studentID": 1
	}
]

```

2. GET student/training_images/<image id>
Get the image id

output
```
[
	{
		"id": 1,
		"name": "91661elon5.jpg",
		"filename": "91661elon5.jpg",
		"date_created": "2023-02-19 08:49:04.461436",
		"studentID": 1,
		"url": "http://localhost:5000//static/training_images/1/91661elon5.jpg"
	}
]
```

3. GET students/<student id>/images
   Get all the images under the student id

output
```
[
	{
		"filename": "91661elon5.jpg",
		"data": "http://localhost:5000//static/training_images/1/91661elon5.jpg"
	},
	{
		"filename": "37522elon7.jpg",
		"data": "http://localhost:5000//static/training_images/1/37522elon7.jpg"
	}
]

```

4. POST /upload/<student id>
   Send images and upload it under the student ID, use file transfer and name it as `images`

```
{
	"studentID": 1,
	"success": "Images uploaded successfully!"
}
```

## Recognize

1. POST /recognize
   Send image and apply face recognition, use name `image`

```
{
	"output": {
		"label": 1,
		"url": "http://localhost:5000/static/get_output/55880.jpg"
	},
	"student": {
		"contact": "1234567890",
		"course": "B.Tech",
		"date_created": "Sun, 19 Feb 2023 08:40:47 GMT",
		"email": "example@email.com",
		"id": 1,
		"name": "Elon Musk",
		"section": "A"
	},
	"success": "Image recognized successfully!"
}
```
