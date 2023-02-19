# face-recognition

# Endpoints

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