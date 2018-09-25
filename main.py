# See AWS Python SDK documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migrations3.html

# Run the AWS Client to configure the AWS SDK key: aws configure

import argparse
import time
from random import randint

import boto3
import numpy as np

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='AWS S3 file access tests suite.')
    parser.add_argument('-b', '--s3bucket', help='S3 bucket name', required=True)
    parser.add_argument('-f', '--filename', help='Filename to upload and retrieve', required=True)
    parser.add_argument('-n', '--testcount', help='Retrieval test count', required=True)

    args = parser.parse_args()

    # low-level functional API
    client = boto3.client('s3')

    # high-level object-oriented API
    resource = boto3.resource('s3')

    # Show the available buckets
    print('Current S3 buckets:')
    for bucket in resource.buckets.all():
        print('\tBucket: {}'.format(bucket.name))

    # Upload a test file to S3
    s3_bucket_name = args.s3bucket
    # s3_bucket_name = 'bertrand-bucket-test-1'
    s3_bucket = resource.Bucket(s3_bucket_name)
    s3_doc_key = args.filename
    print('\nUpload test file {} to S3 bucket {} ...'.format(s3_doc_key, s3_bucket_name))

    body = ''
    with open(s3_doc_key, "rt") as in_file:
        body = in_file.read()

    s3_bucket.put_object(Key=s3_doc_key, Body=body)

    # Retrieve a file from S3
    # See https://dluo.me/s3databoto3
    count = 10
    if args.testcount:
        count = int(args.testcount)

    exec_times = []
    for i in np.arange(1, count + 2):
        print('\n[{}] Retrieving document key {}...'.format(i, s3_doc_key))
        start_time = time.monotonic()
        obj = client.get_object(Bucket=s3_bucket_name, Key=s3_doc_key)
        body_str = obj['Body'].read().decode("utf-8")
        end_time = time.monotonic()
        exec_time_ms = (end_time - start_time) * 1000  # timedelta(seconds=end_time - start_time)
        print('Retrieved {} KB chars in {}'.format(len(body_str) / 1024, exec_time_ms))
        if i > 1:
            # Do not record the first access, which will cause S3 to cache the object
            # TODO: How to run the test without the caching.
            exec_times.append(exec_time_ms)
        wait_time_ms = randint(1000, 2000)
        print("Sleeping for {} ms...".format(wait_time_ms))
        time.sleep(wait_time_ms / 1000)

    print('Min: {}'.format(np.round(np.min(exec_times))))
    print('Max: {}'.format(np.round(np.max(exec_times))))
    print('Avg: {}'.format(np.round(np.average(exec_times))))
    print('Med: {}'.format(np.round(np.median(exec_times))))

    # TODO: Plot of a random sample of 50K file download.
