#!/bin/bash
TASK_NAME=taskname
SERVICE_NAME=servicename
IMAGE_NAME=imagename
CLUSTER_NAME=clustername
REGION=Region
VERSION=Version
ACCOUNT_NUMBER=accnumber
DESIRED_COUNT=desiredcount

NEW_IMAGE=$ACCOUNT_NUMBER.dkr.ecr.$REGION.amazonaws.com/$IMAGE_NAME:$VERSION
TASK_DEFINITION=$(aws ecs describe-task-definition --task-definition "$TASK_NAME" --region "$REGION")
NEW_TASK_DEFINITION=$(echo $TASK_DEFINITION | jq --arg IMAGE "$NEW_IMAGE" '.taskDefinition | .containerDefinitions[0].image = $IMAGE | del(.taskDefinitionArn) | del(.revision) | del(.status) | del(.requiresAttributes) | del(.compatibilities) | del(.registeredAt) | del(.registeredBy)')
NEW_REVISION=$(aws ecs register-task-definition --region "$REGION" --cli-input-json "$NEW_TASK_DEFINITION")
NEW_REVISION_DATA=$(echo $NEW_REVISION | jq '.taskDefinition.revision')


IMAGE_COMPARISON=$(echo $(aws ecs describe-task-definition --task-definition "$IMAGE_NAME") | jq -r '.taskDefinition.containerDefinitions[].image' |  sed "s|$ACCOUNT_NUMBER.dkr.ecr.$REGION.amazonaws.com/$IMAGE_NAME:||")

if [ "$IMAGE_COMPARISON" == "$VERSION" ]
then
      NEW_SERVICE=$(aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --task-definition $TASK_NAME --desired-count "$DESIRED_COUNT" --force-new-deployment)
      echo "done"
      echo "$TASK_NAME, Revision: $NEW_REVISION_DATA"
      aws sns publish --topic-arn arn:aws:sns:"$REGION":"$ACCOUNT_NUMBER":Jenkins-Success --message "$IMAGE_NAME:$VERSION deploymentOn $CLUSTER_NAME Cluster $SERVICE_NAME SUCCESS"
      exit 0
else
      aws sns publish --topic-arn arn:aws:sns::$REGION:$ACCOUNT_NUMBER:Jenkins-Failure --message "$IMAGE_NAME:$VERSION deploymentOn $CLUSTER_NAME Cluster $SERVICE_NAME FAILURE"
      exit 1
fi

