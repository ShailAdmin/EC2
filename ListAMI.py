import boto3

# Replace 'your_access_key' and 'your_secret_key' with your AWS IAM user's access and secret keys
aws_access_key = 'your_access_key'
aws_secret_key = 'your_secret_key'

# Create a Boto3 EC2 client
ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# Get all your own created AMIs
response = ec2.describe_images(Owners=['self'])

# List the AMIs
for ami in response['Images']:
    print(f"AMI ID: {ami['ImageId']}")
    print(f"Name: {ami.get('Name', 'N/A')}")
    print(f"Description: {ami.get('Description', 'N/A')}")
    print(f"Creation Date: {ami['CreationDate']}")
    print()
