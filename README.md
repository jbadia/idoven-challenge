# Backend Coding Challenge - Proposal

Thank you for the warm welcome and kind words! I'm thrilled to have successfully passed the previous steps and now take on this new challenge. 

## 1. Services

There are 3 main components. One API one RQ worker and a database to persist the ECGs. By design the number of endpoints has been limited to the ones required for the assingment. And the results are retrived directly from the RQ / redis

### app
Projects API and main component of the assignment, were we can perform the following tasks:
  - create users
  - process ECGs
  - get ECGs results

The enpoints are listed on section ***`3.`*** with examples

components used:
- Flask
- JSON Web Tokens (auth)
- Pony ORM 

### worker
RQ worker using a redis queue to enqueue tasks. The `modules` directory is shared with the api (app) and uses `Dask.array` instead of vanilla python or numpy as it can handle large amounts of data.

### redis
Required by RQ to queue jobs and retrieve the results.

### MySQL
SQL database used to persist data

### RQ Dashboard
Not required. Used to review the queue.

```config
URL: http://localhost:9181
user: rq
password: password
```  

## 2. Management
Although the services are handled with `docker-compose` and that should be enought to operate them. 

A `Makefile` has been included to simplify all the operations

Project build and start
```bash
  make run
```

Stop the service
```bash
  make stop
```

List running services
```bash
  make status
```

Run unit tests for metrics module
```bash
  make test-module
```

Create a ***admin/admin*** user with `admin` role
```bash
  make create-admin
```

## 3. Endpoints
Intead of defining the endpoints and parameter, a list of `HTTPie` commands is provided as it's self descriptive

### Request token
``` bash
http POST :8080/token user=admin password=1234

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Create user
```bash
http POST :8080/user user=user password=1234 roles:='["user", "admin"]' Authorization:'Bearer <access_token>'
```
> instead of forcing a role per user, as suggested, a multi role per user has been implemented. The role is optional, if not provided a regular user is created

### Process ECG
```bash
http POST :8080/ecg/process id=10 date='2023-07-30' leads:='[{"name": "I", "signal": [1,-1,1]}]' Authorization:'Bearer <access_token>'

{
    "id": "10",
    "status": "queued"
}
```

### Check ECG
```bash
http GET :8080/ecg/10 Authorization:'Bearer <access_token>'

{
    "id": "10",
    "leads": [
        {
            "I": {
                "zero_crossings": 2
            }
        }
    ],
    "status": "completed"
}
```

## 4. What's out and should be included
### JSON Schemas
The model-view should include JSON Schemas to validate the JSON data provided on the `POST` requests 

### Integration Tests
The API (app) and worker services should be adjusted to run the components internally to completely test the services.
- API: Redis, Mysql

Once again, thank you for the encouraging words and this opportunity.
