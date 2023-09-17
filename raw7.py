import boto3

# Initialize the Boto3 EC2 client
ec2 = boto3.client('ec2')

# Function to create an AMI from an EC2 instance
def create_ami(instance_id):
    # Get instance details
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]
    
    # Extract instance tags and type
    tags = instance.get('Tags', [])
    instance_type = instance['InstanceType']
    
    # Create the AMI
    ami_name = f"{instance_type}_AMI"
    ami_description = f"AMI for {instance_id}"
    
    response = ec2.create_image(
        InstanceId=instance_id,
        Name=ami_name,
        Description=ami_description,
        DryRun=False
    )
    
    ami_id = response['ImageId']
    
    # Add tags to the AMI
    ec2.create_tags(
        Resources=[ami_id],
        Tags=tags
    )
    
    return ami_id

# List of instance IDs you want to create AMIs from
instance_ids = ['i-XXXXXXXXXXXXXXXXX', 'i-YYYYYYYYYYYYYYYYY']

# Create AMIs for each instance
for instance_id in instance_ids:
    ami_id = create_ami(instance_id)
    print(f"Created AMI {ami_id} for instance {instance_id}")
