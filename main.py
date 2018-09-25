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
    parser.add_argument('-f', '--testfiles', help='List of files to test with', required=True)
    parser.add_argument('-n', '--testcount', help='Retrieval test count', required=False)
    parser.add_argument('-s', '--sleeptime', help='Sleep time between retrievals', required=False)

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
    s3_bucket = resource.Bucket(s3_bucket_name)

    testfiles = str(args.testfiles).split(',')
    for s3_object_key in testfiles:
        print('\nUpload test file {} to S3 bucket {} ...'.format(s3_object_key, s3_bucket_name))
        body = ''
        with open(s3_object_key, "rt") as in_file:
            body = in_file.read()
        s3_bucket.put_object(Key=s3_object_key, Body=body)

    # Retrieve a file from S3
    # See https://dluo.me/s3databoto3
    count = 10
    if args.testcount:
        count = int(args.testcount)

    sleep_time = 2000
    if args.sleeptime:
        sleep_time = int(args.sleeptime)

    print('S3 bucket                 : {}'.format(s3_bucket_name))
    print('test files                : {}'.format(testfiles))
    print('Test count                : {}'.format(count))
    print('Random sleep (Upper bound): {}'.format(sleep_time))

    exec_times = {}
    for i in np.arange(1, count + 1):
        # Alternate files in order to have S3 NOT cache objects:
        for s3_object_key in testfiles:
            print('\n[{}] Retrieving document key {}...'.format(i, s3_object_key))
            start_time = time.monotonic()
            obj = client.get_object(Bucket=s3_bucket_name, Key=s3_object_key)
            body_str = obj['Body'].read().decode("utf-8")
            end_time = time.monotonic()
            exec_time_ms = (end_time - start_time) * 1000  # timedelta(seconds=end_time - start_time)
            print('Retrieved {} KB chars in {}'.format(len(body_str) / 1024, exec_time_ms))
            if s3_object_key not in exec_times.keys():
                exec_times[s3_object_key] = []
            exec_times[s3_object_key].append(exec_time_ms)

            # Random pause
            wait_time_ms = randint(1000, sleep_time)
            print("Sleeping for {} ms...".format(wait_time_ms))
            time.sleep(wait_time_ms / 1000)

    for key, value in exec_times.items():
        print('File {} retrieval test results:'.format(key))
        print('\tMin: {}'.format(np.round(np.min(exec_times[key]))))
        print('\tMax: {}'.format(np.round(np.max(exec_times[key]))))
        print('\tAvg: {}'.format(np.round(np.average(exec_times[key]))))
        print('\tMed: {}'.format(np.round(np.median(exec_times[key]))))

    # TODO: Plot of a random sample of 50K file download.
