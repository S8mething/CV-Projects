#!/bin/bash

cd src
servicename=($(dir))

for service in ${servicename[@]}
do
    image="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/$PROJECT_NAME/$service:$TAG"
    if [ $service == "cartservice" ]
    then
        (
            cd $service/src
            docker build -t "$image" .
            docker push "$image"
        )
    else
        (
        cd $service
        docker build -t "$image" .
        docker push "$image"
        )
    fi
done



