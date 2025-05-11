# Development Details

The `app` directory contains the source code for the application, and all the relevant env files are present in the root of the project directory. 

To start the application locally, setup a virtual environment using `python3 -m venv journee`. You can do this in the same directory as the project, the `.gitignore` fill is modified to ignore the virtual env. 

Once created the virtual environment activate it and follow as below

```bash
$ source journee/bin/activate
$ pip3 install -r requirements.txt
$ uvicorn main:app --app-dir app --port 8080 --host localhost
```

This will start the app at `http://localhost:8080/`

## App Directory Structure
The `app/main.py` is the entrypoint for the application. 
This is where the application starts and registers all the routes and handlers etc. 

The `app` directory has many subdirectories, each of which represent individual domains. 

```bash
app
├── auth            # Handle all authentication routes and logic here
|                   # Sign up, Sign in, Oauth2.0, JWT creation etc. 
|
|
├── common          # Any common code such as decorators, utils which can be used
|                   # across all domain specific code
|
├── conversations   # handle all CRUD Logic related conversations etc. 
|
├── hotspots        # handle logic related to hotspot metadata fetching, stuff like 
|                   # getting images / pictures, geocode (lat/long) any other details
|                   # etc
|
├── itinerary       # handle all CRUD logic and any other logic 
|                   # and routes (other than generation) related to itineraries
|
├── llm             # handle all logic for interacting with the LLM
|
├── main.py         # entry point
|
├── plan            # handle all logic and routes for planning /
|                   # generating the itinerary
|
├── routes.py       # collection of all routers
|
├── services        # common services 
|
└── users           # handle all CRUD logic related to user management
```

Almost all domains follow the same structure. 
- All services (business logic) is handled by service code present in `service/` directory
- All models, request models, DAO, DTO etc.. are under the `models` folder. All models are `pydantic` models which eases a lot of model specific handling like validation etc
- The main file in each domain would most likely be the `routes.py` file (if present) which exposes the routes of that domain. 

To understand easily from a microservices perspective, understand it this way

> Each domain is a microservice which has its routes and handlers and models and can be independenlty deployed and scaled. \
The `router.py` together with `main.py` is the API Gateway and routes request to appropriate domain / microservice. 

## Tips for development
1. The `release` branch is the deployment branch for this project. The deployment happens automatically when any code under the `app` directory is changed. This service is deployed on Render. Reach out to (Atharva) for credentials, as creating a team required pro subscription on render. 
2. While this is a monolith, think of each domain as a microservice, easier to map and design
3. If there is a domain which is user facing, for example `users` has `user_service`,and some other services might need to interact with it for some task, do not use the `users/services/user_service` directly. Instead create `users/services/user_internal_service` . The `user_service` should only handle public routes, all service to service calls are internal and should be handled by the internal service. Separation of concerns, as well as easy to scale. 
Ex: From a microservice POV, `user_internal_service` and `user_service` could be two separate lambdas, one serving `service-service` traffic other serving `frontend-service` traffic, thus completely separating out the tasks they specialise in. 
4. It is on me that the current code has bare bones documentation, while not enforced, if possible, please do add. I will keep on committing with documentation details. 
5. Try not to push directly to main branch and instead create a separate branch and create a pull request.
6. When code is in `main` branch, you might have to manually create a pull request to `release` branch from `main` branch. In case github says pull request failed or automatic merge not possible, locally checkout `release` branch, rebase with `main` and do a force push. Will need to fix this and can be done down the line. 