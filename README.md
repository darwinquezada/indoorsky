<br />
<p align="center"> 
  <h3 align="center">Cloud-based Indoor Positioning Platform</h3>
</p>

```
                         ______                     
 _________        .---"""      """---.              
:______.-':      :  .--------------.  :             
| ______  |      | :                : |             
|:______B:|      | |  A-WEAR:       | |             
|:______B:|      | |                | |             
|:______B:|      | |  Loading...    | |             
|         |      | |                | |             
|:_____:  |      | |                | |             
|    ==   |      | :                : |             
|       O |      :  '--------------'  :             
|       o |      :'---...______...---'              
|       o |-._.-i___/'             \._              
|'-.____o_|   '-.   '-...______...-'  `-._          
:_________:      `.____________________   `-.___.-. 
                 .'.eeeeeeeeeeeeeeeeee.'.      :___:
               .'.eeeeeeeeeeeeeeeeeeeeee.'.         
              :____________________________:

```


<!-- ABOUT THE PROJECT -->
## About The Project

In order to provide a flexible, reusable, and scalable cloud-based indoor positioning platform, we propose a new architecture for indoor positioning and location platforms. The proposed architecture is designed with reference to the guidelines provided in the available standards for indoor positioning, mapping, and software. This platform is designed to have independent services which can be deployed and used with other systems. For instance, some components can be reused in contact-tracing applications, autonomous navigation, and indoor parking, among others. It will reduce the development and deployment time of other systems in a similar way to the services provided by open-source platforms. The platform also takes into account standards, protocols, data pre-processing, accuracy, and positioning technologies.

Developed by: Darwin Quezada

### Built With

This application has been developed using:
* [Python](https://www.python.org/)


<!-- structure -->
## Getting Started
    .
    ├── application                                 # Contains the microservice code
    │   ├── algorithms                              # * algorithms used in the ms                    
    │   ├── core                                    # Util resources
    │   │   ├── decorators
    │   │   │   └── jwt_managet.py                  # API authetication using JWT
    │   │   ├── exceptions
    │   │   │   ├── exceptions.py                   # API exceptions
    │   │   │   └── collection_exceptions.py        # DB - collections exception             
    │   ├── data                                    # Data layer
    │   │   ├── datasource
    │   │   │   ├── datasource.py                   # Datasource abstract class
    │   │   │   └── datasource_impl.py              # Datasource Implementation
    │   │   ├── model
    │   │   │   └── <name>_model.py                 # Model's name
    │   │   ├── repository
    │   │   │   └── repository_impl.py              # Implementation repository
    │   ├── domain                                  # Domain layer
    │   │   ├── entity
    │   │   │   └── <name>_entity.py                # Entity
    │   │   ├── repository
    │   │   │   └── <name>_repository.py            # Model's name
    │   │   ├── use_cases                           # Specific use cases
    │   │   │   ├── create_use_case.py
    │   │   │   ├── get_use_case.py
    │   │   │   ├── delete_use_case.py
    │   │   │   └── update_use_case.py              
    │   ├── presentation                            # Presentation layer
    │   │   ├── data_injection
    │   │   │   └── injection_container.py      
    │   │   ├── endpoints                           # API endpoints
    │   │   │   └── <name>_endpoint.py
    │   │   ├── req_body                            # Request body
    │   │   │   └── <name>_body.py      
    │   ├── scripts                                 # General scripts (DB initializations, etc.)     
    ├── .env                                        # Environement setup
    ├── .flaskenv                                   # Flask environment variable
    ├── confing.py                                  # Configuration file
    ├── docker-compose.yml                          # YAML file to configure the application's services
    ├── Dockerfile                                  # Commands to assemble the image
    ├── requirements.txt                            # Requirements (Python libraries)
    ├── pyproject.toml                              # Pytest configuration 
    ├── pytest.ini                                  # Pytest ini 
    ├── run.py                                      # Core file, run the microservice
    └── README.md                                   # Readme please


For learning how to use insky.cloud, see its documentation: https://insky.cloud/

| IndoorSky        | [![pub package](https://img.shields.io/badge/indoorSky-v1.0.0.0%20Beta-green)](https://insky.cloud/)|


# Environment Set up

Steps to setup the environment, and API gateway.

The cloud-based indoor positioning platform is composed of several microservices that can be deployed independently using docker containers. These microservices can be accessed through the URI of each microservice or by using an API gateway. 
To deploy the microservices, it is necessary to have a container which will contain each microservice. This procedure shows how to setup the environment using [Docker ecosystem](https://www.docker.com/).

## Docker

Please follow the guidelines provided by [Docker](https://docs.docker.com/) to set up your docker environment.

## Databases

This project use two primary databases commonly used for real-time applications. The user (developer) is free to change the datase according to his/her criteria. The database can be changed in the `.env` file and the new methods implemented in the `data` layer --> `datasource_impl.py`.

```
.
    ├── application                                 # Contains the microservice code                              
    │   ├── data                                    # Data layer
    │   │   ├── datasource
    │   │   │   ├── datasource.py                   # Datasource abstract class
    │   │   │   └── datasource_impl.py              # Datasource Implementation
```

### RethinkDB

The vast majority of the microservices developed here are connected to `RethinDB`. 

```shell
$ docker run -d -P --name rethink1 rethinkdb
```
More information in [RethinDB](https://rethinkdb.com/).

### Appwrite

Apprwrite backend is mainly used to manage the users' registration, authetication and store the files, such as machine learning models.

```shell
docker run -it --rm \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    --volume "$(pwd)"/appwrite:/usr/src/code/appwrite:rw \
    --entrypoint="install" \
    appwrite/appwrite:1.0.1
```
More information in [Appwrite](https://appwrite.io/).

## Kong Gateway

This project uses an open-source gateway, namely Kong.

1. Create a docker network

```shell
$ docker network create kong-isky-net
```

2. Start a postgres container.

```shell
$ docker run -d --name kong-database \
  --network=kong-isky-net \
  -p 5432:5432 \
  -e "POSTGRES_USER=kong" \
  -e "POSTGRES_DB=kong" \
  -e "POSTGRES_PASSWORD=password" \
  postgres:9.6
```

3. Kong database.

```shell
$ docker run --rm --network=kong-isky-net \
  -e "KONG_DATABASE=postgres" \
  -e "KONG_PG_HOST=kong-database" \
  -e "KONG_PG_PASSWORD=password" \
 kong:3.0.0-alpine kong migrations bootstrap
```

4. Start the Kong Gateway container.

```shell
$ docker run -d --name kong-gateway \
  --network=kong-isky-net \
  -e "KONG_DATABASE=postgres" \
  -e "KONG_PG_HOST=kong-database" \
  -e "KONG_PG_USER=kong" \
  -e "KONG_PG_PASSWORD=password" \
  -e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
  -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
  -e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
  -e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
  -e "KONG_ADMIN_LISTEN=0.0.0.0:8001, 0.0.0.0:8444 ssl" \
  -p 8000:8000 \
  -p 8443:8443 \
  -p 127.0.0.1:8001:8001 \
  -p 127.0.0.1:8444:8444 \
  kong:3.0.0-alpine
```

# Installation

The following steps detail how to install or deploy the microservices developed in indoor positioning platform.

### Set up ports

In order to change the ports to access each microservice, `docker-compose.yml` and/or `run.py` files have to be modified. The default ports are in the rang of `5000`.

`docker-compose.yml` file:
```yml
ports:
    - "5000:5000"
```

`run.py` file:
```python
app.run(host='0.0.0.0', port=5000)
```

---
**_NOTE:_**

The port can be only changed in the `docker-compose.yml` file and mapping to the application port.

---

### Docker network

By defauld the docker network is `kong-isky-net`, but it can be changed in each microservice.

Create network:
```shell
$ docker network create kong-isky-net
```

### Build and run microservices with Compose

Inside of each microservice:

Build and run:
```shell
$ docker-compose build
$ docker-compose up -d
```

## Full Deployment

In order to deploy all microservices provided within this platform, it is necessary to have installed [Kong gateway](https://konghq.com/install#kong-community) and run the `deployment.sh` file.

Build and run:
```shell
$ chmod +x deployment.sh
$ sh deployment.sh
```
---
**_NOTE:_**
If the ports were changed in the docker files, please change them accordingly in the deployment file.
```shell
$ curl -i -X POST http://localhost:8001/services/ --data "name=building" --data "url=http://localhost:5000/“
```
---

