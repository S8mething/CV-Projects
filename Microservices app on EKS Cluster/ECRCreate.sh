#!/bin/bash

cd src
ECRNAME=($(dir))
for ecr in ${ECRNAME[@]}
do
  AWSECRCREATE=$(aws ecr create-repository \
    --repository-name $PROJECT_NAME/$ecr)
done