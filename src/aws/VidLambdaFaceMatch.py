"""
Code and comments derived from:
https://aws.amazon.com/blogs/machine-learning/find-distinct-people-in-a-video-with-amazon-rekognition/
Accessed 2018-09-10
"""

"""
LAMBDA ONE: Processes video into thumbnail frames for AWS Rekognition index_faces command
"""

# Retrieve the key for the S3 object that caused this function to be triggered
key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
filename = key.split('/')[-1]

# Create a new transcoding job. Files created by Elastic Transcoder start with 'elastictranscoder/[filename]/[timestamp]_'
timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')

client = boto3.client('elastictranscoder')
response = client.create_job(
  PipelineId=os.environ['PipelineId'],
  Input={'Key': key},
  OutputKeyPrefix='elastictranscoder/{}/{}_'.format(filename, timestamp),
  Output={
    'Key': 'transcoded-video.mp4',
    'ThumbnailPattern': 'thumbnail-{count}',
    'PresetId': os.environ['PresetId']
  }
)




"""
LAMBDA TWO: Creates a new collection in Amazon Rekognition.
"""
"""
2.A Calls the IndexFaces operation for each thumbnail. The solution uses concurrent
threads to increase the throughput of requests to Amazon Rekognition and to reduce
the time needed to complete the operation. In the end, the collection contains as
many faces as there are faces detected in each thumbnail.
"""

# Create a new collection. I use the job ID for the name of the collection
collectionId = sns_msg['jobId']
rekognition.create_collection(CollectionId=collectionId)

# Retrieve the list of thumbnail objects in the S3 bucket
thumbnailKeys = []
prefix = sns_msg['outputKeyPrefix']
prefix += sns_msg['outputs'][0]['thumbnailPattern'].replace('{count}', '')

paginator = s3.get_paginator('list_objects')
response_iterator = paginator.paginate(
  Bucket=os.environ['Bucket'],
  Prefix=prefix
)
for page in response_iterator:
  thumbnailKeys += [i['Key'] for i in page['Contents']]

# Call the IndexFaces operation for each thumbnail
faces = {}
indexFacesQueue = Queue()

def index_faces_worker():
  rekognition = boto3.client('rekognition', region_name=os.environ['AWS_REGION'])

  while True:
    key = indexFacesQueue.get()

    try:
      response = rekognition.index_faces(
        CollectionId=collectionId,
        Image={'S3Object': {
          'Bucket': os.environ['Bucket'],
          'Name': key
        }},
        ExternalImageId=str(frameNumber)
      )

      # Store information about returned faces in a local variable
      frameNumber = int(key[:-4][-5:])
      for face in response['FaceRecords']:
        faceId = face['Face']['FaceId']
        faces[faceId] = {
          'FrameNumber': frameNumber,
          'BoundingBox': face['Face']['BoundingBox']
        }

    # Put the key back in the queue if the IndexFaces operation failed
    except:
      indexFacesQueue.put(key)

    indexFacesQueue.task_done()

# Start CONCURRENT_THREADS threads
for i in range(CONCURRENT_THREADS):
  t = Thread(target=index_faces_worker)
  t.daemon = True
  t.start()

# Wait for all thumbnail objects to be processed
for key in thumbnailKeys:
  indexFacesQueue.put(key)
indexFacesQueue.join()



"""
2.B  For each face stored in the collection, calls the SearchFaces operation to
search for faces that are similar to that face and in which it has a confidence
in the match that is higher than 97%.
"""

searchFacesQueue = Queue()

def search_faces_worker():
  rekognition = boto3.client('rekognition', region_name=os.environ['AWS_REGION'])

  while True:
    faceId = searchFacesQueue.get()

    try:
      response = rekognition.search_faces(
        CollectionId=collectionId,
        FaceId=faceId,
        FaceMatchThreshold=97,
        MaxFaces=256
      )
      matchingFaces = [i['Face']['FaceId'] for i in response['FaceMatches']]

      # Delete the face from the local variable 'faces' if it has no matching faces
      if len(matchingFaces) > 0:
        faces[faceId]['MatchingFaces'] = matchingFaces
      else:
        del faces[faceId]

    except:
        searchFacesQueue.put(faceId)

    searchFacesQueue.task_done()

for i in range(CONCURRENT_THREADS):
  t = Thread(target=search_faces_worker)
  t.daemon = True
  t.start()

for faceId in list(faces):
  searchFacesQueue.put(faceId)
searchFacesQueue.join()


"""
2.C Find faces in the collection that match each face that it detected. It starts
from the first face that appears in the video and associates that face with a
peopleId of 1. Then, it recursively propagates the peopleId to the matching faces.
In other words, if faceA matches faceB and faceB matches faceC, the function decides
that faceA, faceB and faceC correspond to the same person and assigns them all
the same peopleId. To avoid false positives, the Lambda function propagates the
peopleId from faceA to faceB only if there are at least two faces that match faceB
that also match faceA. When the peopleId 1 has fully propagated, the function associates
a peopleId of 2 to the next face appearing in the video that has no peopleId associated with it.
It continues this process until all of the faces have a peopleId.
"""

# Sort the list of faces in the order of which they appear in the video
def getKey(item):
  return item[1]
facesFrameNumber = {k: v['FrameNumber'] for k, v in faces.items()}
faceIdsSorted = [i[0] for i in sorted(facesFrameNumber.items(), key=getKey)]

# Identify unique people and detect the frames in which they appear
def propagate_person_id(faceId):
  for matchingId in faces[faceId]['MatchingFaces']:
    if not 'PersonId' in faces[matchingId]:

      numberMatchingLoops = 0
      for matchingId2 in faces[matchingId]['MatchingFaces']:
          if faceId in faces[matchingId2]['MatchingFaces']:
              numberMatchingLoops = numberMatchingLoops + 1

      if numberMatchingLoops >= 2:
          personId = faces[faceId]['PersonId']
          faces[matchingId]['PersonId'] = personId
          propagate_person_id(matchingId)

personId = 0
for faceId in faceIdsSorted:
  if not 'PersonId' in faces[faceId]:
    personId = personId + 1
    faces[faceId]['PersonId'] = personId
    propagate_person_id(faceId)
