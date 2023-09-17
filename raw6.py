import boto3

# Initialize the Boto3 EC2 client
ec2_client = boto3.client('ec2')

# Describe all AMIs in your account
response = ec2_client.describe_images(Owners=['self'])
all_amis = response['Images']

# Iterate through each AMI and create an EC2 instance with the specified instance type
for ami in all_amis:
    ami_id = ami['ImageId']
    ami_name = ami['Name']
    
    if ami_name.endswith("t2.micro"):
        instance_type = 't2.micro'
    elif ami_name.endswith("t3.micro"):
        instance_type = 't3.micro'
    elif ami_name.endswith("t2.large"):
        instance_type = 't2.large'
    else:
        instance_type = 'default-instance-type'  # Set a default instance type or handle other cases
    
    try:
        response = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            KeyName='your-key-pair-name',  # Replace with your key pair name
            SecurityGroupIds=['sg-0123456789abcdef0'],  # Replace with your security group IDs
        )
        
        # Get the instance ID of the launched instance
        instance_id = response['Instances'][0]['InstanceId']
        
        print(f"Launched instance {instance_id} with AMI {ami_id} and instance type {instance_type}")
    except Exception as e:
        print(f"Error launching instance with AMI {ami_id} and instance type {instance_type}: {str(e)}")
