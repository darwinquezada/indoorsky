#!/bin/bash
cat << EOF
#############################################################
#   Welcome to indoorsky.cloud configuration file!          #
#   License CC by 4.0                                       #
#   Version 1.0.0 Beta                                      #
#############################################################
EOF

PS3='Please, enter the type of environment: '
options=("development" "production" "test" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "development")
            break
            ;;
        "production")
            break
            ;;
        "test")
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done

read -p "IndoorSky host [localhost]: " host
host_system=${host:-localhost}
read -p "RethinkDB host [localhost]: " host
rethindb_host=${host:-localhost}
read -p "RethinkDB port [28015]: " port
rethindb_port=${port:-28015}
read -p "Appwrite host [localhost]: " host
appwrite_host=${host:-localhost}
read -p "Appwrite port [80]: " port
appwrite_port=${port:-80}
read -p "Appwrite project ID [none]: " id
appwrite_project_id=${id:-none}
read -p "Appwrite endpoint [$appwrite_host:$appwrite_port/api/v1]: " endpoint
appwrite_endpoint=${endpoint:-$appwrite_host:$appwrite_port/api/v1}
read -p "Appwrite API key [none]: " id
appwrite_api_key=${id}

isky_dirs=( $(find ./ -type d -name "isky-*" 2>/dev/null) )

# Setting up environment variables
echo "Setting up environment variables..."
for dir in "${isky_dirs[@]}"; do
  cd "$dir"
  sed -i -e "s|^CONFIGURATION_SETUP=.*$|CONFIGURATION_SETUP='$opt'|g" .env
  sed -i -e "s|^AUTHENDPOINT=.*$|AUTHENDPOINT='$host_system'|g" .env
  sed -i -e "s|^RDB_HOST=.*$|RDB_HOST='$rethindb_host'|g" .env
  sed -i -e "s|^RDB_PORT=.*$|RDB_PORT='$rethindb_port'|g" .env

  sed -i -e "s|^APPWRITEENDPOINT=.*$|APPWRITEENDPOINT='$appwrite_endpoint'|g" .env
  sed -i -e "s|^APPWRITEPROJECTID=.*$|APPWRITEPROJECTID='$appwrite_project_id'|g" .env
  sed -i -e "s|^APPWRITEAPIKEY=.*$|APPWRITEAPIKEY='$appwrite_api_key'|g" .env

  cd ..
done

# Deploying microservices ...
echo "Deploying microservices ..."

if ! command -v docker &> /dev/null
then
    echo "Docker could not be found"
    exit
fi

if ! command -v docker-compose &> /dev/null
then
    echo "Docker compose could not be found"
    exit
else
    for dir in "${isky_dirs[@]}"; do
        cd "$dir"
        echo "Deploying $dir ..."
        docker-compose build --no-cache
        docker-compose up -d
        cd ..
done
fi

echo "Configuration completed!"