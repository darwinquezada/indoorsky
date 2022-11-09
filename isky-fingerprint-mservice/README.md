# Environment Microservice
For learning how to use insky.cloud, see its documentation: https://insky.cloud/

| IndoorSky        | [![pub package](https://img.shields.io/badge/indoorSky-v1.0.0%20Beta-green)](https://insky.cloud/)|
| ---------------- | --------------------------------------------------------------------------------------------------- |
    .
    ├── application                                 # Contains the microservice code                              
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
    │   ├── scripts
    │   │   └── initialization.py                   # Database initialization
    ├── certs                                       # TLS certificates     
    ├── .env                                        # Environement setup
    ├── .flaskenv                                   # Flask environment variable
    ├── config.py                                   # Configuration file
    ├── docker-compose.yml                          # YAML file to configure the application's services
    ├── Dockerfile                                  # Commands to assemble the image
    ├── requirements.txt                            # Requirements to run the microservice (Python libraries)
    ├── run.py                                      # Core file, run the microservice
    ├── pyproject.toml                              # Pytest options
    ├── pytest.ini                                  # Pytest configuration file
    ├── boot.sh                                     # Gunicorn boot config
    └── README.md                                   # Readme please

# Installation

The following steps detail how to install or deploy the microservices developed in indoor positioning platform.

### Set up ports

In order to change the ports to access each microservice, `docker-compose.yml` and/or `run.py` files have to be modified. 
The default ports are in the rang of `5000`.

`docker-compose.yml` file:
```yml
ports:
    - "5000:5000"
```

`run.py` file:
```python
app.run(host='0.0.0.0', port=5000)
```

**_NOTE:_**
The port can be only changed in the `docker-compose.yml` file and mapping to the application port.


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