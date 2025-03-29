# import requests
import os 
from dotenv import load_dotenv
load_dotenv()
from config import settings

# url = "http://localhost:8000/user/download?cmd=whoami"

# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpb24iLCJleHAiOjE3NDMxNzUwNDJ9.fHyL6UyPChjQW9ZyOyA64vmQs1yhtt7MGR8AYe3gmwQ"
# }

# response = requests.get(url=url, headers=headers)

# print(response.status_code)
# print(response.text)


# name = os.getenv('THE_NAME')
name = settings.THE_NAME

print(f'{name} awd ')