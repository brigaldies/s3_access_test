# See AWS Python SDK documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migrations3.html

import time

import boto3

if __name__ == "__main__":

    # low-level functional API
    client = boto3.client('s3')

    # high-level object-oriented API
    resource = boto3.resource('s3')

    # Show the available buckets
    print('Current S3 buckets:')
    for bucket in resource.buckets.all():
        print('\tBucket: {}'.format(bucket.name))

    # Upload a test file to S3
    s3_bucket_name = 'bertrand-bucket-test-1'
    s3_bucket = resource.Bucket(s3_bucket_name)
    print('\nUpload a test file to S3 bucket {} ...'.format(s3_bucket_name))

    # s3_doc_key = 'the_adventure_of_tom_sawyer.txt'
    # s3_doc_key = 'test_1.txt'
    s3_doc_key = 'test_1.txt'
    # body = 'This is the content of a text file.'
    body = ''

    with open(s3_doc_key, "rt") as in_file:
        body = in_file.read()

    s3_bucket.put_object(Key=s3_doc_key, Body=body)

    # Retrieve a file from S3
    print('Retrieving document key {}...'.format(s3_doc_key))
    start_time = time.monotonic()
    obj = client.get_object(Bucket=s3_bucket_name, Key=s3_doc_key)
    body_str = obj['Body'].read().decode("utf-8")
    end_time = time.monotonic()
    exec_time_ms = (end_time - start_time) * 1000  # timedelta(seconds=end_time - start_time)
    print('Retrieved {} KB chars in {}'.format(len(body_str) / 1024, exec_time_ms))

    # TODO: Plot of a random sample of 50K file download.
