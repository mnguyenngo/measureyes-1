#!/bin/bash

# Script to run VidFaceDetection.py

# REQUIREMENTS:
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
#    1. Substitute parameters generated in prerequisites above in each of the Set-Variable statements where
#       indicated after the -Value tags.
#        CAUTION: ONCE AGAIN, DO NOT DISTRIBUTE THIS SCRIPT (ON GITHUB, FOR EXAMPLE) WITH SPECIFIC URL OR ARNs.
#        RECOMMENDED: If copied into a local git repo, add this file to .gitignore
#    2. In Powershell terminal:  $ .\run_rek.sh

# Set parameters in current only (i.e., local) Powershell terminal.
Set-Variable -Name "BUCKET" -Value "<name of AWS S3 bucket>"
Set-Variable -Name "VIDEO" -Value "<S3 path/file (NOT including bucket name)>"
Set-Variable -Name "FACE_COLLECTION" -Value "<name of AWS collection>"
Set-Variable -Name "ROLE_ARN" -Value "<DO NOT DISTRIBUTE/PUBLISH: Amazon Resource Number for IAM role provisioned with Rekognition and SQS permissions>"
Set-Variable -Name "QUEUE_URL" -Value "<DO NOT DISTRIBUTE/PUBLISH: URL to AWS SQS Queue>"
Set-Variable -Name "TOPIC_ARN" -Value "<DO NOT DISTRIBUTE/PUBLISH: ARN for AWS Topic to recieve status messages from Rekognition>"
Set-Variable -Name "JOB_TAG" -Value "<Name for job to report to AWS Simple Notification Service>"


# Execute VidFaceDetection.py with parameters defined above.
python VidFaceDetection.py `
	--video $VIDEO `
	--bucket $BUCKET `
	--collection $FACE_COLLECTION `
	--role $ROLE_ARN `
	--sqs $QUEUE_URL `
	--topic $TOPIC_ARN `
	--jobtag $JOB_TAG
