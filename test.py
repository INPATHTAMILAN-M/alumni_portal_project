import requests

url = "http://127.0.0.1:8000/update_event/37/"

# Your payload data without the file (non-file fields)
payload = {
    "title": "special function alumni 1",
    "category": 1,
    "start_date": "2024-10-25",
    "start_time": "15:00:00",
    "venue": "Main Hall",
    "address": "123 Main St",
    "link": "http://example.com",
    "is_public": True,
    "need_registration": True,
    "registration_close_date": "2024-10-20",
    "description": "This is a special function alumni.",
    "instructions": "Please arrive 30 minutes early.waiting....",
    "event_question": [
        {
            "question": "Accommodation details",
            "help_text": "Please let us know number of people you will require accommodation for, leave empty if none.",
            "options": "",
            "is_faq": True
        },
        {
            "question": "Food preferences",
            "help_text": "Choose an option of your food preference ",
            "options": "Veg, Non-Veg",
            "is_faq": False
        },
        {
            "question": "Your choice",
            "help_text": "If T-shirt, please select a size that fits you",
            "options": "S,M,L,XL,XXL",
            "is_faq": True
        }
    ]
}

# Open the file for sending
with open(r'C:\Users\ADMIN\Pictures\33.jpg', 'rb') as file:
    files = {
        'event_wallpaper': ('33.jpg', file, 'image/jpg')  # File in multipart/form-data
    }

    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzMzA5NzgyLCJpYXQiOjE3MzMzMDM3ODIsImp0aSI6IjUzZWI4ZjdlZTQ1NjRkYzI5MWY4YzUzNzVjN2JjMjBkIiwidXNlcl9pZCI6Mn0.RpVDj5gSOtDb5Ssh69VsLEbjf-5wEKt_6KA1cz-1h74'
    }

    # Send the POST request with the file
    response = requests.post(url, headers=headers, data=payload, files=files)

# Print the response text
print(response.status_code)
