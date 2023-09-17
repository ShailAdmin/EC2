import boto3

# Initialize the Boto3 EC2 client
ec2_client = boto3.client('ec2')

# Function to list your own created AMIs and return their IDs
def list_amis():
    response = ec2_client.describe_account_attributes()
    account_id = response['AccountAttributes'][0]['AttributeValues'][0]['AttributeValue']
    
    response = ec2_client.describe_images(Owners=[account_id])
    
    ami_ids = [image['ImageId'] for image in response['Images']]
    return ami_ids

# Function to create EC2 instances using a list of AMI IDs
def create_instances(ami_ids, instance_type, key_name, security_group_ids):
    num_instances = len(ami_ids)
    
    response = ec2_client.run_instances(
        ImageId=ami_ids[0],  # Choose the first AMI ID from the list
        InstanceType=instance_type,
        MinCount=num_instances,
        MaxCount=num_instances,
        KeyName=key_name,
        SecurityGroupIds=security_group_ids
    )
    
    instance_ids = [instance['InstanceId'] for instance in response['Instances']]
    return instance_ids

# List your AMIs
ami_ids = list_amis()

if not ami_ids:
    print("No AMIs found.")
else:
    print("AMIs found:")
    for ami_id in ami_ids:
        print(ami_id)

# Create EC2 instances using the list of AMIs
if ami_ids:
    instance_type = 't2.micro'  # Replace with your desired instance type
    key_name = 'your-key-pair-name'  # Replace with your key pair name
    security_group_ids = ['sg-0123456789abcdef0']  # Replace with your security group IDs

    instance_ids = create_instances(ami_ids, instance_type, key_name, security_group_ids)
    
    print("\nCreating instances with the following instance IDs:")
    for instance_id in instance_ids:
        print(instance_id)
