import boto3

# Initialize the Boto3 EC2 client
ec2_client = boto3.client('ec2')

# List all available AMIs
response = ec2_client.describe_images(Owners=['self'])  # List only your own AMIs

# Extract the list of AMIs and display them with their names and IDs
amis = response['Images']
print("Available AMIs:")
for index, ami in enumerate(amis, start=1):
    print(f"{index}. AMI Name: {ami['Name']}, AMI ID: {ami['ImageId']}")

# Select AMIs by their index
selected_indices = input("Enter the indices of the AMIs you want to use for creating instances (comma-separated): ")
selected_indices = [int(index) - 1 for index in selected_indices.split(",")]

# Specify instance details
instance_type = 't2.micro'
key_name = 'your-key-pair-name'
security_group_ids = ['sg-0123456789abcdef0']

# Launch instances from the selected AMIs
for index in selected_indices:
    ami_id = amis[index]['ImageId']
    response = ec2_client.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        KeyName=key_name,
        SecurityGroupIds=security_group_ids
    )
    
    instance_id = response['Instances'][0]['InstanceId']
    print(f"Launched instance {instance_id} from AMI {ami_id}.")
