#!/usr/bin/env python3
"""Simple S3 storage stress test."""
import os
import time
import argparse
import uuid
import logging
import boto3


# TAKE ARG FOR CONFIG FILE
parser = argparse.ArgumentParser(description='Script arguments')
parser.add_argument('--url', type=str, required=True)
parser.add_argument('--access-key', type=str, required=True)
parser.add_argument('--secret-key', type=str, required=True)
parser.add_argument('--bucket', type=str, required=True)
parser.add_argument('--write', action='store_true', required=False)
parser.add_argument('--read', action='store_true', required=False)
parser.add_argument('--read-max-files', type=int, default=1000 , required=False)
parser.add_argument('--write-files', type=int, default=1, required=False)
parser.add_argument('--file-size', type=int, default=8192, required=False)
parser.add_argument('--files-per-folder', default=None, type=int, required=False)
parser.add_argument('--log-level', type=str, default='WARNING', required=False)
args = parser.parse_args()

# Set common variables

ENDPOINT_URL = ( 'https://' + args.url)
AWS_ACCESS_KEY_ID = args.access_key
AWS_SECRET_ACCESS_KEY = args.secret_key
AWS_BUCKET = args.bucket
PERFORM_READ = args.read
READ_FILES_LIMIT = args.read_max_files
PERFORM_WRITE = args.write
FILES_NUM = args.write_files
FILES_SIZE = args.file_size
FILES_PER_FOLDER = args.files_per_folder
LOG_LEVEL = getattr(logging,args.log_level)

# Set correct log level
logging.basicConfig(level=LOG_LEVEL)


s3_client = boto3.client('s3',
            endpoint_url = ENDPOINT_URL,
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY
            )


def generate_random_file(size):
    """Generate random file of any size."""
    file = (os.urandom(size))
    return file

def upload_object(filename,file,bucket):
    """Upload an object to a s3 bucket."""
    response = s3_client.put_object(
                          Body=file,
                          Bucket=bucket,
                          Key=filename,
                      )
    return response


def s3_bench_write(size,files_number,bucket,files_per_folder):
    """Generates and upload the file on s3."""
    file_path = ''
    file_counter = None
    if files_per_folder:
        file_counter = 0
        file_path = str(0) + '/'
    for file_num in range(files_number):
        if files_per_folder:
            file_counter = file_counter + 1
            if file_counter > files_per_folder:
                # set path name
                file_path = str(file_num) + '/'
                file_counter = 0
        binary_file = generate_random_file(size)
        file_name = file_path + str(uuid.uuid4())
        logging.info('uploading file %d of %d: %s ', file_num, FILES_NUM, file_name)
        upload_object(file_name,binary_file,bucket)


def s3_bench_read(bucket,limit):
    """List all files in the specified bucket/path."""
    logging.info('start reading objects...')
    response = s3_client.list_objects_v2(Bucket=bucket, MaxKeys = limit)
    if LOG_LEVEL == getattr(logging,'INFO'):
        count = 0
        if 'Contents' in response.keys():
            for _ in response['Contents']:
                count = count + 1
        logging.info('reading completed, found %d objects', count)
    logging.info('objects reading completed')



# Script execution
if PERFORM_WRITE:
    logging.info('begin write operations...')
    start_time = time.time()
    s3_bench_write(FILES_SIZE,FILES_NUM,AWS_BUCKET,FILES_PER_FOLDER)
    end_time = time.time()
    time_elapsed = (end_time - start_time)
    logging.info('write operation completed in %d seconds ',time_elapsed)
if PERFORM_READ:
    logging.info('begin read operations')
    start_time = time.time()
    s3_bench_read(AWS_BUCKET,READ_FILES_LIMIT)
    end_time = time.time()
    time_elapsed = (end_time - start_time)
    logging.info('read operation completed in %d seconds ', time_elapsed)

logging.info('end')
