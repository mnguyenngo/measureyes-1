### Measureyes AWS Rekognition Pipeline
The applications found in this directory deploy AWS Rekognition on stored video to detect persons and Head Turns (HTs) and return HT data and aggregate statistics.   
#### Suggested Workflow:
From within `measureyes/src/aws/app/` directory...
1. Execute `run_rek.sh` OR `run_rek.ps1` -- From Unix/Linux or Powershell terminal, deploy AWS Rekognition on target video (via VidFaceDetection.py) and write responses to raw json files stored in a local sub-directory named for unique video ID.
2. `ExportRekToSQL.py` -- Parse raw json response files into a Pandas DataFrame and export to Postgres.
3. `HTDetect.py` -- Import parsed data from Postgres and detect HTs based on user-specified HT parameters including facial-pose and "dwell" thresholds. Output results and aggregate statistics as HTDetect objects.   
#### See documentation in scripts listed above for requirements and detailed instructions.
