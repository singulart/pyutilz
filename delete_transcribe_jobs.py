import boto3

session = boto3.Session(profile_name='rich')
transcribe = session.client('transcribe')

def delete_transcription_jobs():
    next_token = None
    jobs_to_delete = []

    while True:
        if next_token:
            response = transcribe.list_transcription_jobs(NextToken=next_token)
        else:
            response = transcribe.list_transcription_jobs()

        jobs = response.get('TranscriptionJobSummaries', [])

        for job in jobs:
            job_name = job.get('TranscriptionJobName', '')
            if job_name.endswith('.wav'):
                jobs_to_delete.append(job_name)

        next_token = response.get('NextToken')
        if not next_token:
            break

    for job_name in jobs_to_delete:
        try:
            transcribe.delete_transcription_job(TranscriptionJobName=job_name)
            print(f"Deleted job: {job_name}")
        except Exception as e:
            print(f"Failed to delete job {job_name}: {e}")

    print(f"Deleted {len(jobs_to_delete)} transcription jobs.")

delete_transcription_jobs()
