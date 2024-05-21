### Get Department List API Method

This API method is used to retrieve a paginated list of departments. It allows for retrieving specific information about departments, including their ID, type, name, number of members, and other relevant details.

#### HTTP Request
`GET https://mycompany.hrmsystem.com/api/v1/departments?page={page_number}&per_page={number_of_items_per_page}`

#### Query Parameters
- `page`: The page number of the department list (integer, optional, default=1)
- `per_page`: The number of items to display per page (integer, optional, default=5)

#### Headers
- `token`: API token for authentication (string, required)

#### Success Response
A successful response will return a JSON object containing the current page, data array with department details, and pagination information.

- **Code**: 200
- **Content**: 

Sample request
=================
```python
import requests

url = "https://{my_company_domain}/api/v1/departments?page=1&per_page=5"

payload = {}
headers = {
  'token': '{api_token}'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

Sample Response
===============
```json
{
    "result": {
        "current_page": 1,
        "data": [
            {
                "id": 2,
                "type": 1,
                "name": "Management",
                "number_of_members": 4,
                "number_of_members_with_subteams": 4,
                "team_leader_id": null,
                "hr_ids": [
                    "7xl"
                ],
                "managers": [
                    "ND"
                ],
                "subteams": [],
                "parent_id": null
            },
            {
                "id": 5,
                "type": 1,
                "name": "Sales Team",
                "number_of_members": 5,
                "number_of_members_with_subteams": 5,
                "team_leader_id": "lXEQ",
                "hr_ids": [
                    "7xl"
                ],
                "managers": [
                    "ND",
                    "lXEQ"
                ],
                "subteams": [],
                "parent_id": null
            },
            {
                "id": 26,
                "type": 1,
                "name": "DELIVERY",
                "number_of_members": 1,
                "number_of_members_with_subteams": 29,
                "team_leader_id": null,
                "hr_ids": [
                    "7xl"
                ],
                "managers": [],
                "subteams": [
                    7,
                    12,
                    21,
                    22,
                    24,
                    27,
                    28,
                    35,
                    39,
                    40,
                    41,
                    42
                ],
                "parent_id": null
            },            
            {
                "id": 6,
                "type": 1,
                "name": "Training Camp",
                "number_of_members": 0,
                "number_of_members_with_subteams": 0,
                "team_leader_id": null,
                "hr_ids": [
                    "7xl"
                ],
                "managers": [
                    "d82"
                ],
                "subteams": [],
                "parent_id": null
            },
            {
                "id": 7,
                "type": 1,
                "name": "Project ABC",
                "number_of_members": 7,
                "number_of_members_with_subteams": 7,
                "team_leader_id": null,
                "hr_ids": [
                    "7xl"
                ],
                "managers": [
                    "Oox"
                ],
                "subteams": [],
                "parent_id": 26
            },
            {
                "id": 8,
                "type": 1,
                "name": "HR/ Recruiting",
                "number_of_members": 2,
                "number_of_members_with_subteams": 2,
                "team_leader_id": "7xl",
                "hr_ids": [
                    "7xl"
                ],
                "managers": [
                    "ND",
                    "7xl"
                ],
                "subteams": [],
                "parent_id": null
            }
        ],
        "first_page_url": "https://mycompany.hrmsystem.com/api/v1/departments?page=1",
        "from": 1,
        "last_page": 5,
        "last_page_url": "https://mycompany.hrmsystem.com/api/v1/departments?page=5",
        "links": [
            {
                "url": null,
                "label": "&laquo; Prev.",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=5",
                "label": "5",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=2",
                "label": "Next. &raquo;",
                "active": false
            }
        ],
        "next_page_url": "https://mycompany.hrmsystem.com/api/v1/departments?page=2",
        "path": "https://mycompany.hrmsystem.com/api/v1/departments",
        "per_page": 5,
        "prev_page_url": null,
        "to": 5,
        "total": 21
    },
    "error": false,
    "code": 200,
    "messages": []
}
```


