import boto3
import time
import json
import logging
import concurrent.futures
import multiprocessing
from datetime import datetime

from urllib.parse import urlparse

session = boto3.Session(profile_name='rich')
s3_client = session.client('s3')
transcribe_client = session.client('transcribe')

# Configuration
WAV_BUCKET = "amazon-connect-e2f41bc27d25"
AUDIO_PREFIX = "connect/USEYE/CFSRecordings/"
TARGET_PREFIX = "connect/USEYE/CFSRecordings/transcriptions/"
LANGUAGE_CODE = "en-US"
MAX_WORKERS = multiprocessing.cpu_count()

def log_message(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def list_audio_files(bucket, prefix):
    objects = []
    continuation_token = None

    while True:
        list_params = {'Bucket': bucket, 'Prefix': prefix}
        if continuation_token:
            list_params['ContinuationToken'] = continuation_token
        
        response = s3_client.list_objects_v2(**list_params)
        objects.extend(response.get('Contents', []))

        if response.get('IsTruncated'):
            continuation_token = response['NextContinuationToken']
        else:
            break
    return [obj['Key'] for obj in objects if obj['Key'].endswith(('.wav'))]

def start_transcription_job(job_name, file_uri):
    """Start a transcription job with PII redaction enabled."""
    try:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': file_uri},
            MediaFormat=file_uri.split('.')[-1],
            LanguageCode=LANGUAGE_CODE,
            OutputBucketName=WAV_BUCKET,
            OutputKey=f"{TARGET_PREFIX}{job_name}.json",
            Settings={
                'ShowSpeakerLabels': True,
                'MaxSpeakerLabels': 2
            },
            ContentRedaction={
                'RedactionType': 'PII',
                'RedactionOutput': 'redacted'
            }
        )
        log_message(f"Started transcription job: {job_name}")
        return True
    except Exception as e:
        log_message(f"Error starting transcription job {job_name}: {e}")
        return False

def check_job_status(job_name):
    """Check the status of a transcription job."""
    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        status = response['TranscriptionJob']['TranscriptionJobStatus']
        if status in ['COMPLETED', 'FAILED']:
            return response
        time.sleep(5)

def process_audio_file(file_key):
    """Process a single audio file in parallel."""
    job_name = file_key.split('/')[-1]
    file_uri = f"s3://{WAV_BUCKET}/{file_key}"

    if start_transcription_job(job_name, file_uri):
        transcription_result = check_job_status(job_name)
        if transcription_result['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            log_message(f"Transcription completed for {job_name}, saved in S3 at {WAV_BUCKET}/{TARGET_PREFIX}{job_name}.json")
        else:
            log_message(f"Transcription failed for {job_name}")

def process_audio_files():
    """Main processing function with parallel execution."""
    files = list_audio_files(WAV_BUCKET, AUDIO_PREFIX)
    log_message(f"Found {len(files)} audio files.")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(process_audio_file, files)

if __name__ == "__main__":
    process_audio_files()
