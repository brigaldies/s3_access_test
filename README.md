Motivation: Measure the S3 file access latency and throughput within an AWS region, as would be the case in a production environment.

See [Getting Started with the AWS SDK for Python (Boto3)](https://aws.amazon.com/developers/getting-started/python/)

Go to [AMI Users](https://console.aws.amazon.com/iam/home?region=us-east-1#/users) to add a user for programmatic access. See screen shots, in order:

- Starting screen: Welcome to Identify and Access Management.png
- Click on users --> Users.png
- Click on Add User --> Add User.png
    - Enter user name
    - Select Programmatic access
- Click on Next:Permissions --> Set permissions.png
    - Click on Attach exiting policies directory
    - Enter S3 in the filter policies search box
    - Select AmazonS3FullAccess
- Click on Next:Review --> Review add user.png
- Click on Create user --> Add user success.png  
- Download the CSV key file by clicking on Download.csv

To run the script in an AWS EC2 instance:

1. Create and launch an EC2 instance using the free-tier Amazon Linux AMI image.
    - Notes:
    - Create a new security group that allows incoming SSH traffic.
    - Create or re-use a key pair.
    - The imagine has Python 2.7 pre-installed, which is not what we want. Later on in the instructions, we install Python 3.6 with yum.
    
1. SSH into the EC2 instance ("ec2-34-239-124-112.compute-1.amazonaws.com" is my EC2 instance's public DNS; aws_ec2_key.pem is the key file I downloaded from the AWS instance creation and launch wizard after creating the key)
    - ```chmod 400 aws_ec2_key.pem``` (One-time setup)
    - ```ssh -i aws_ec2_key.pem ec2-user@ec2-34-239-124-112.compute-1.amazonaws.com```
    - See [Accessing Instances Linux](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html) for the full documentation.

1. Install git with yum: ```sudo yum install git```

1. Install python 3.6: ```sudo yum install python36```

1. Clone the project's repo: ```git clone https://github.com/brigaldies/s3_access_test.git```

1. Navigate to the project's diretory: ```cd s3_access_test```

1. Create a Python virtual env: ```mkdir venv && virtualenv-3.6 venv/s3_access```

1. Activate the virtual Python 3.6 environment: ```source ./venv/s3_access/bin/activate```

1. Load the required packages: ```pip install -r requirements.txt```

1. Run the script: ```python main.py```

You should an output similar to:
```
Current S3 buckets:
	Bucket: bertrand-bucket-test-1

Upload a test file to S3 bucket bertrand-bucket-test-1 ...
Retrieving document key test_1.txt...
Retrieved 55.935546875 KB chars in 38.25454000070749
```

1. Deactivate the virtual environment: ```deactivate```