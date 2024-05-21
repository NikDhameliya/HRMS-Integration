### Get Out-of-Office Records API Method

This API method is used to retrieve a paginated list of out-of-office records. It allows for retrieving specific information about employees' out-of-office statuses, including vacations, sick leaves, business trips, and other relevant details.

#### HTTP Request
`GET https://mycompany.hrmsystem.com/api/v1/out-off-office?page={page_number}&per_page={number_of_items_per_page}`

#### Query Parameters
- `page`: The page number of the out-of-office records list (integer, optional, default=1)
- `per_page`: The number of items to display per page (integer, optional, default=5)

#### Headers
- `token`: API token for authentication (string, required)

#### Success Response
A successful response will return a JSON object containing the current page, data array with out-of-office records, and pagination information.

- **Code**: 200
- **Content**: 

Sample request
=================
```python
import requests

url = "https://{my_company_domain}/api/v1/out-off-office?page=1&per_page=20&additional_info=true"

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
                "id": "ND",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "end_test": "2016-04-01",
                "fired_date": null,
                "business_trip": [],
                "home_work": [],
                "sick_leave": [],
                "documented_sick_leave": [],
                "vacation": [                 
                    {
                        "date": "2023-02-09",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-02-08",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-02-07",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-02-06",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    }
                ],
                "unpaid_vacation": [],
                "overtime": [],
                "weekend_work": [
                    {
                        "date": "2021-06-27",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2021-04-17",
                        "is_full_day": false,
                        "from": "10:00",
                        "to": "16:00",
                        "used_minutes": 360
                    }
                ],
                "night_shift": [],
                "day_transfer": []
            },
            {
                "id": "7xl",
                "name": "Helen Aoe",
                "email": "helen.aoe@example.com",
                "end_test": "2021-03-11",
                "fired_date": null,
                "business_trip": [],
                "home_work": [
                    {
                        "date": "2021-09-06",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2021-08-02",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    }
                ],
                "sick_leave": [
                    {
                        "date": "2022-03-30",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2022-02-21",
                        "is_full_day": false,
                        "from": "14:30",
                        "to": "15:30",
                        "used_minutes": 60
                    },
                    {
                        "date": "2022-02-18",
                        "is_full_day": false,
                        "from": "11:30",
                        "to": "18:00",
                        "used_minutes": 390
                    },
                    {
                        "date": "2022-02-17",
                        "is_full_day": false,
                        "from": "09:00",
                        "to": "11:30",
                        "used_minutes": 150
                    },
                    {
                        "date": "2022-02-16",
                        "is_full_day": false,
                        "from": "14:30",
                        "to": "15:30",
                        "used_minutes": 60
                    },
                    {
                        "date": "2021-11-05",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    }
                ],
                "documented_sick_leave": [],
                "vacation": [
                    {
                        "date": "2024-03-25",
                        "is_full_day": false,
                        "from": "14:00",
                        "to": "18:00",
                        "used_minutes": 240
                    },
                    {
                        "date": "2024-02-23",
                        "is_full_day": false,
                        "from": "14:00",
                        "to": "18:00",
                        "used_minutes": 240
                    },
                    {
                        "date": "2023-12-29",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-12-28",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-12-21",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                ],
                "unpaid_vacation": [],
                "overtime": [
                    {
                        "date": "2022-06-08",
                        "is_full_day": false,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    }
                ],
                "weekend_work": [],
                "night_shift": [],
                "day_transfer": [
                    {
                        "start": {
                            "date": "2021-07-28",
                            "is_full_day": false,
                            "from": "16:30",
                            "to": "18:00",
                            "used_minutes": 90
                        },
                        "end": {
                            "date": "2021-07-27",
                            "is_full_day": false,
                            "from": "18:00",
                            "to": "19:30",
                            "used_minutes": 90
                        }
                    }
                ]
            },
            {
                "id": "RLp",
                "name": "Dennis Smith",
                "email": "dennis.smith@example.com",
                "end_test": "2021-12-19",
                "fired_date": null,
                "business_trip": [],
                "home_work": [],
                "sick_leave": [],
                "documented_sick_leave": [],
                "vacation": [
                    {
                        "date": "2023-12-22",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-11-10",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-11-09",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-11-08",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-04-18",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-04-17",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-04-16",
                        "is_full_day": true,
                        "from": null,
                        "to": null,
                        "used_minutes": 0
                    },
                ],
                "unpaid_vacation": [],
                "overtime": [],
                "weekend_work": [],
                "night_shift": [],
                "day_transfer": []
            },
        ],
        "first_page_url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=1",
        "from": 1,
        "last_page": 19,
        "last_page_url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=19",
        "links": [
            {
                "url": null,
                "label": "&laquo; Prev.",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=5",
                "label": "5",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=6",
                "label": "6",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=7",
                "label": "7",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=8",
                "label": "8",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=9",
                "label": "9",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=10",
                "label": "10",
                "active": false
            },
            {
                "url": null,
                "label": "...",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=18",
                "label": "18",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=19",
                "label": "19",
                "active": false
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=2",
                "label": "Next. &raquo;",
                "active": false
            }
        ],
        "next_page_url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=2",
        "path": "https://mycompany.hrmsystem.com/api/v1/out-off-office",
        "per_page": 5,
        "prev_page_url": null,
        "to": 5,
        "total": 94
    },
    "error": false,
    "code": 200,
    "messages": []
}
```