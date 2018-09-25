#Adapted from AWS Rekognition demo (accessed Sept 2018): https://docs.aws.amazon.com/rekognition/latest/dg/video-analyzing-with-sqs.html
#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import time
import boto3
import json
import sys
import os
import shutil
import argparse


class VideoDetect():

    rek = boto3.client('rekognition')
    sqs = boto3.client('sqs')
    s3 = boto3.resource('s3')

    def __init__(self, bucket, video, collection, roleArn, queueURL, topicArn,
                 jobTag="Measureyes FaceSearch"):
        # Data sources and stores
        self.bucket = bucket
        self.video = video
        self.collection = collection

        # Credentialed IAM Role for access to AWS Rekognition and SQS services
        self.roleArn = roleArn

        # AWS Simple Queue Service and Topic for logging and flow control
        self.queueUrl = queueURL
        self.topicArn = topicArn

        # Customizeable job tag
        self.jobTag = jobTag


    def main(self, write_data=None):
        """
        Execute AWS Rekognition StartFaceSearch and GetFaceSearch functions.
        Optionally (default) print FaceSearch response data.
        """
        jobFound = False

        #=====================================
        response = self.rek.start_face_search(
            Video={'S3Object':{'Bucket':self.bucket, 'Name':self.video}},
            FaceMatchThreshold=0.7,
            CollectionId=self.collection,
            NotificationChannel={'RoleArn':self.roleArn, 'SNSTopicArn':self.topicArn},
            JobTag=self.jobTag
            )
        #=====================================
        print('Start Job Id: ' + response['JobId'])
        dotLine = 0

        while jobFound == False:
            sqsResponse = self.sqs.receive_message(QueueUrl=self.queueUrl, MessageAttributeNames=['ALL'],
                                          MaxNumberOfMessages=10)

            if sqsResponse:

                if 'Messages' not in sqsResponse:
                    # Print a series of dotted lines while the job is processing
                    if dotLine<60:
                        print('.', end='')
                        dotLine=dotLine+1
                    else:
                        print()
                        dotLine=0
                    sys.stdout.flush() # Good practice: Clear buffer after python printing
                    continue

                for message in sqsResponse['Messages']: # Once SQS gets a msg that the job is done (or it failed)...
                    # Dig into the nested json message to extract and print info about the job status
                    notification = json.loads(message['Body'])
                    rekMessage = json.loads(notification['Message'])
                    print(rekMessage['JobId'])
                    print(rekMessage['Status'])
                    if str(rekMessage['JobId']) == response['JobId']:
                        print('Matching Job Found:' + rekMessage['JobId'])
                        jobFound = True
                        print_bool = True if write_data is None else False
                        #=============================================
                        self.GetResultsFaceSearch(rekMessage['JobId']) #, print_response=print_bool)
                        #=============================================

                        self.sqs.delete_message(QueueUrl=self.queueUrl,
                                       ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(rekMessage['JobId']) + ' : ' + str(response['JobId']))
                    # Delete the unknown message. Consider sending to dead letter queue
                    self.sqs.delete_message(QueueUrl=self.queueUrl,
                                   ReceiptHandle=message['ReceiptHandle'])

        print('\nJOB COMPLETE')


    def GetResultsFaceSearch(self, jobId, print_response=False):
        maxResults = 1000
        paginationToken = ''
        finished = False
        counter = 1

        while finished == False:
            get_response = self.rek.get_face_search(JobId=jobId,
                                            MaxResults=maxResults,
                                            NextToken=paginationToken,
                                            SortBy='TIMESTAMP')

            if print_response:

                print('\n\nVideo compression codec: ', get_response['VideoMetadata']['Codec'])
                print('Video duration (seconds): ', str(get_response['VideoMetadata']['DurationMillis'] / 1000.))
                print('Video format: ', get_response['VideoMetadata']['Format'])
                print('Video framerate: ', get_response['VideoMetadata']['FrameRate'])

                for faceDetection in get_response['Persons']:
                    # print('Detection Timestamp: ', str(faceDetection['Timestamp']))
                    # print('Person index: ', faceDetection['Person']['Index'])

                    if 'Face' in faceDetection['Person']:
                        print('Detection Timestamp: ', str(faceDetection['Timestamp']))
                        print('Person index: ', faceDetection['Person']['Index'])
                        print('Face yaw: ', faceDetection['Person']['Face']['Pose']['Yaw'])
                        print('Face pitch: ', faceDetection['Person']['Face']['Pose']['Pitch'])

                    if 'FaceMatches' in faceDetection:
                        print(faceDetection['FaceMatches']['Face']['FaceId'])
                        print(faceDetection['FaceMatches']['Face']['Confidence'])
                        print(faceDetection['FaceMatches']['Face']['ImageId'])

            else:
                # destination_dir assumes script is run from measureyes/src/
                destination_dir = "../data/" + self.video.split("/")[-1].split(".")[0] + "_response/"
                destination_file = destination_dir + self.video.split("/")[-1].split(".")[0] + "_response_" + "%04d" % (counter,) + ".json"
                if counter == 1:
                    # On first pass, create destination directory named for the video; overwrite it if it already exists
                    # This directory will contain the video's individual .json response files
                    if os.path.exists(destination_dir):
                        shutil.rmtree(destination_dir)
                    os.makedirs(destination_dir)

                with open(destination_file, 'w+') as f:
                    json.dump(get_response, f)
                print("\nDATA WRITTEN TO: {}\n".format(destination_file))
                counter += 1

            if 'NextToken' in get_response: # If the first "get_face_search" command didn't get all the results...
                paginationToken = get_response['NextToken']
            else:
                finished = True
                if print_response: sys.stdout.flush()



if __name__ == "__main__":

    # For tracking runtime
    start_time = time.time()

    # Configure arguments for command-line execution
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', help='(string) S3 bucket name')
    parser.add_argument('--video', help='(string) AWS S3 path/file of video to be analyzed')
    parser.add_argument('-coll', '--collection',
        help='(string) AWS Rekogntion Collection for Indexing Vectorized (Anonymized) Facial IDs')
    parser.add_argument('-role', '--role',
        help='(string) Amazon Resource Number (ARN) for IAM role provisioned with Rekognition credentials')
    parser.add_argument('--sqs',
        help='(string) URL for AWS Simple Queue Service for logging and flow control')
    parser.add_argument('-sns', '--topic',
        help='(string) Amazon Resource Number (ARN) for Simple Notification Service (SNS) Topic to which AWS Rek publishes status notifications')
    parser.add_argument('-tag', '--jobtag',
        help='OPTIONAL: (string) Identifier to ID job in completion status published to assigned SNS Topic')

    args = parser.parse_args()

    JOB_TAG = args.jobtag if args.jobtag is not None else 'Measureyes FaceSearch'

    print("""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    PARAMETERS SPECIFIED FOR REKOGNTION VIDEO ANALYSIS:
        S3 Bucket: {}
        Target Video: {}
        AWS Collection (Face Index): {}
        IAM Role: {}
        SQS ARN: {}
        SNS Topic: {}
        Cluster file name: {}
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """.format(args.bucket, args.video, args.collection, args.role, args.sqs, args.topic, JOB_TAG)
    )


    # Initialize VideoDetect instance with options defined in command line
    analyzer = VideoDetect(args.bucket,
                         args.video,
                         args.collection,
                         args.role,
                         args.sqs,
                         args.topic,
                         jobTag=JOB_TAG
                        )
    analyzer.main()


    print('\nRuntime in Seconds: ', (time.time() - start_time))
