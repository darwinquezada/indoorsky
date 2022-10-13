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
    ├── .env                                        # Environement setup
    ├── .flaskenv                                   # Flask environment variable
    ├── .conf                                       # Configuration file
    ├── docker-compose.yml                          # YAML file to configure the application's services
    ├── Dockerfile                                  # Commands to assemble the image
    ├── requirements.txt                            # Requirements to run the microservice (Python libraries)
    ├── run.py                                      # Core file, run the microservice
    └── README.md                                   # Readme please
