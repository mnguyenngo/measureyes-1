#!/bin/bash

# Script to run VidFaceDetection.py

# PREREQUISITES:
#    1. AWS Account and AWS IAM user
#    2. Python 3.6+ with argparse package installed.
#    3. AWS CLI and boto3 package installed and configured with permissions (access keys) for IAM USER
#    4. Configuration of IAM USER permissions per https://docs.aws.amazon.com/rekognition/latest/dg/api-video-roles.html
#        NOTE Role ARN (Amazon Resource Number)
#    5. AWS Collection for indexing vectorized facial data. 
#        Create via $ aws rekogntion create-collection --create-collection <coll name>. NOTE Collection Name
#    6. AWS S3 Bucket containing target videos for analysis
#    7. AWS SNS Topic, SQS service configured per https://docs.aws.amazon.com/rekognition/latest/dg/video-analyzing-with-sqs.html
#        NOTE SQS URL and Topic ARN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    CAUTION: FOR SECURITY, DO NOT PUBLISH OR DISTRIBUTE THIS SCRIPT WITH SPECIFIC URLs OR ARNs (API KEYS).
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 

# INSTRUCTIONS:
#    1. Substitute parameters generated in prerequisites above where indicated below in each of the export statements.
#        CAUTION: ONCE AGAIN, DO NOT DISTRIBUTE THIS SCRIPT (ON GITHUB, FOR EXAMPLE) WITH SPECIFIC URL OR ARNs. 
#        RECOMMENDED: If copied into a local git repo, add this file to .gitignore
#    2. In bash terminal shell:  $ source run_rek.sh


export BUCKET="<name of AWS S3 bucket>"
export VIDEO="<S3 path/file (NOT including bucket name)>"
export FACE_COLLECTION="<name of AWS collection>"
export ROLE_ARN="<DO NOT DISTRIBUTE/PUBLISH: Amazon Resource Number for IAM role provisioned with Rekognition and SQS permissions>"
export QUEUE_URL="<DO NOT DISTRIBUTE/PUBLISH: URL to AWS SQS Queue>"
export TOPIC_ARN="<DO NOT DISTRIBUTE/PUBLISH: ARN for AWS Topic to recieve status messages from Rekognition>"
export JOB_TAG="<Name for job to report to AWS Simple Notification Service>"


# echo "~~~~~~~~~~~~~~~~~~~~~"
# echo "The following variables have been set in the current terminal shell:"
# echo "\$BUCKET: $BUCKET"
# echo "\$VIDEO: $VIDEO"
# echo "\$FACE_COLLECTION: $FACE_COLLECTION"
# echo "\$ROLE_ARN: $ROLE_ARN"
# echo "\$QUEUE_URL: $QUEUE_URL"
# echo "\$TOPIC_ARN: $TOPIC_ARN"
# echo "\$JOB_TAG: $JOB_TAG"
# echo "~~~~~~~~~~~~~~~~~~~~~"


# Execute VidFaceDetection.py with variables defined above
python VidFaceDetection.py \
	--bucket $BUCKET \
	--video $VIDEO \
	--collection $FACE_COLLECTION \
	--role $ROLE_ARN \
	--sqs $QUEUE_URL \
	--topic $TOPIC_ARN \
	--jobtag $JOB_TAG
