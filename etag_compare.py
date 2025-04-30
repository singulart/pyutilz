import boto3
import re

def list_s3_files(bucket_name, prefix):
    session = boto3.Session(profile_name='rich')
    s3 = session.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    files = {}
    
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            etag = obj['ETag'].strip('"')  # Remove quotes from eTag
            files[key] = etag
    
    return files

def extract_filename_variants(files):
    pattern = re.compile(r'^(.*?)(\(\d+\))?\.wav$')
    grouped_files = {}
    
    for filename, etag in files.items():
        match = pattern.match(filename)
        if match:
            base_name = match.group(1) + '.wav'
            grouped_files.setdefault(base_name, {})[filename] = etag
    
    return grouped_files

def compare_etags(grouped_files):
    results = []
    
    for base_name, versions in grouped_files.items():
        if len(versions) > 1:
            etags = list(set(versions.values()))
            if len(etags) == 1:
                results.append(f"MATCH: {base_name} - All versions have the same eTag")
            else:
                results.append(f"MISMATCH: {base_name} - Different eTags detected")
    
    return results

def main():
    bucket_name = 'amazon-connect-e2f41bc27d25'
    prefix = 'connect/USEYE/CFSRecordings/'
    
    files = list_s3_files(bucket_name, prefix)
    print(f"Found {len(files)} files")
    grouped_files = extract_filename_variants(files)
    results = compare_etags(grouped_files)
    
    for result in results:
        print(result)

if __name__ == '__main__':
    main()