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
parser.add_argument('--write', type=int, required=False)
parser.add_argument('--read', type=int, required=False)
parser.add_argument('--num-files', type=int, default=1, required=False)
parser.add_argument('--file-size', type=int, default=4096, required=False)
parser.add_argument('--files-per-folder', type=int, required=False)
args = parser.parse_args()

# Set common variables

ENDPOINT_URL = ( 'https://' + args.url)
AWS_ACCESS_KEY_ID = args.access_key
AWS_SECRET_ACCESS_KEY = args.secret_key
AWS_BUCKET = args.bucket
FILES_NUM = args.num_files
FILES_SIZE = args.file_size


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


def s3_bench_write(size,files_number,bucket):
    """Main function that generates and uplad the file on s3."""
    logging.info('begin upload...')
    for file_num in range(files_number):
        logging.debug('uploading file %d of %d ', str(file_num), str(FILES_NUM))
        binary_file = generate_random_file(size)
        file_name = str(uuid.uuid4())
        upload_object(file_name,binary_file,bucket)


start_time = time.time()


end_time = time.time()
time_elapsed = (end_time - start_time)
logging.info('operation completed in %d seconds ', str(time_elapsed))
logging.info('end')
