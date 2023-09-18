import boto3

# Initialize Boto3 EC2 client
ec2 = boto3.client('ec2')

# Function to create an EC2 instance with a specific instance type
def create_ec2_instance(ami_id, instance_type):
    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        KeyName='your-key-name',  # Replace with your SSH key name
        SecurityGroupIds=['your-security-group-id'],  # Replace with your security group ID
        SubnetId='your-subnet-id',  # Replace with your subnet ID
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': f'Instance-{instance_type}'
                    }
                ]
            }
        ]
    )
    instance_id = response['Instances'][0]['InstanceId']
    print(f"Created EC2 instance {instance_id} with instance type {instance_type}")

# List of AMI IDs
ami_ids = ['ami-XXXXXXXXXXXXXXXXX', 'ami-YYYYYYYYYYYYYYYYY']  # Replace with your AMI IDs

# Create EC2 instances with instance types based on the last part of the AMI name
for ami_id in ami_ids:
    ami_name = ec2.describe_images(ImageIds=[ami_id])['Images'][0]['Name']
    last_part = ami_name.split('-')[-1]
    instance_type = f"t2.{last_part}"  # You can modify the instance type naming logic here
    create_ec2_instance(ami_id, instance_type)
