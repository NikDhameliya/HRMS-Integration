### Get Employee List API Method

This API method is used to retrieve a paginated list of employees. It allows for filtering and retrieving specific information about employees, including their ID, name, email, position, and other personal details.

#### HTTP Request
`GET https://mycompany.hrmsystem.com/api/v1/employees?page={page_number}&per_page={number_of_items_per_page}`

#### Query Parameters
- `page`: The page number of the employee list (integer, optional, default=1)
- `per_page`: The number of items to display per page (integer, optional, default=5)

#### Headers
- `token`: API token for authentication (string, required)

#### Success Response
A successful response will return a JSON object containing the current page, data array with employee details, and pagination information.

- **Code**: 200
- **Content**: 



Sample request
=================
```python
import requests

url = "https://{my_company_domain}/api/v1/employees?page=1&per_page=5"

payload = {}
headers = {
  'token': '{api_token}'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```



Sample Payload
=================
```json
```json
{
    "result": {
        "current_page": 1,
        "data": [
            {
                "id": "ND",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "position": "CEO",
                "grade": "",
                "residence": "Country, City",
                "residence_comment": null,
                "country": "Молдова",
                "city": null,
                "phone": "1234567890",
                "skype": null,
                "linked_in": null,
                "telegram": null,
                "birth_date": "1982-08-11",
                "end_test": "2016-04-01",
                "fired_date": null,
                "start_date": "2016-04-01",
                "gender": 1,
                "additional_email": "alternate.email@example.com",
                "additional_phone": null,
                "relocate": false,
                "duties": null,
                "description": null,
                "additional_info": null,
                "team": [
                    {
                        "id": 2,
                        "name": "Management"
                    }
                ],
                "career": [
                    {
                        "start_date": "2021-04-08",
                        "end_date": null,
                        "test_period_start_date": null,
                        "test_period_end_date": null,
                        "company_name": "",
                        "department": null,
                        "position": "CEO&СТО",
                        "grade": "",
                        "place": "",
                        "team": "Management",
                        "comment": null
                    },
                    {
                        "start_date": "2021-03-29",
                        "end_date": null,
                        "test_period_start_date": null,
                        "test_period_end_date": null,
                        "company_name": "",
                        "department": null,
                        "position": "CEO&СТО",
                        "grade": "",
                        "place": "",
                        "team": "",
                        "comment": ""
                    }
                ],
                "contacts": [
                    {
                        "type_id": 2,
                        "type_name": "email",
                        "value": "alternate.email@example.com"
                    },
                    {
                        "type_id": 1,
                        "type_name": "phone",
                        "value": "1234567890"
                    }
                ],
                "languages": [],
                "educations": [],
                "skills": [],
                "awards": []
            },
            {
                "id": "7xl",
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "position": "HR Specialist",
                "grade": "",
                "residence": "Country, City, Address",
                "residence_comment": "Address details",
                "country": "Україна",
                "city": "Суми",
                "phone": "0987654321",
                "skype": null,
                "linked_in": null,
                "telegram": null,
                "birth_date": "1995-11-26",
                "end_test": "2021-03-11",
                "fired_date": null,
                "start_date": "2021-02-11",
                "gender": 2,
                "additional_email": null,
                "additional_phone": null,
                "relocate": false,
                "duties": null,
                "description": null,
                "additional_info": "Relative's contact phone number - 1231231234",
                "team": [
                    {
                        "id": 8,
                        "name": "HR/ Recruiting"
                    },
                    {
                        "id": 2,
                        "name": "Management"
                    }
                ],
                "career": [
                    {
                        "start_date": "2021-05-27",
                        "end_date": null,
                        "test_period_start_date": null,
                        "test_period_end_date": null,
                        "company_name": null,
                        "department": null,
                        "position": "HR Specialist/Recruiter",
                        "grade": "",
                        "place": null,
                        "team": "Management",
                        "comment": null
                    },
                    {
                        "start_date": "2021-04-08",
                        "end_date": null,
                        "test_period_start_date": null,
                        "test_period_end_date": null,
                        "company_name": null,
                        "department": null,
                        "position": "HR Specialist/Recruiter",
                        "grade": "",
                        "place": null,
                        "team": "HR/ Recruiting",
                        "comment": null
                    },
                    {
                        "start_date": "",
                        "end_date": null,
                        "test_period_start_date": null,
                        "test_period_end_date": null,
                        "company_name": null,
                        "department": null,
                        "position": "HR Specialist/Recruiter",
                        "grade": "",
                        "place": null,
                        "team": "HR/ Recruiting",
                        "comment": null
                    }
                ],
                "contacts": [
                    {
                        "type_id": 2,
                        "type_name": "email",
                        "value": "jane.smith@fakemail.com"
                    },
                    {
                        "type_id": 1,
                        "type_name": "phone",
                        "value": "9876543210"
                    }
                ],
                "languages": [],
                "educations": [],
                "skills": [],
                "awards": []
            },
            // other employees...
        ],
        "first_page_url": "https://mycompany.hrmsystem.com/api/v1/employees?page=1",
        "from": 1,
        "last_page": 19,
        "last_page_url": "https://mycompany.hrmsystem.com/api/v1/employees?page=19",
        "links": [
            {
                "url": null,
                "label": "&laquo; Поп.",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=5",
                "label": "5",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=6",
                "label": "6",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=7",
                "label": "7",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=8",
                "label": "8",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=9",
                "label": "9",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=10",
                "label": "10",
                "active": false
            },
            {
                "url": null,
                "label": "...",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=18",
                "label": "18",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=19",
                "label": "19",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/employees?page=2",
                "label": "Наст. &raquo;",
                "active": false
            }
        ],
        "next_page_url": "https://mycompany.hrmsystem.com/api/v1/employees?page=2",
        "path": "https://mycompany.hrmsystem.com/api/v1/employees",
        "per_page": 5,
        "prev_page_url": null,
        "to": 5,
        "total": 200
    },
    "error": false,
    "code": 200,
    "messages": []
}
```
