import boto3

# Initialize the Boto3 EC2 client
ec2_client = boto3.client('ec2')

# Define the instance IDs for which you want to create AMIs
instance_ids = ['your_instance_id_1', 'your_instance_id_2']  # Add more instance IDs as needed

# Create an AMI for each instance and tag it with the instance type
for instance_id in instance_ids:
    response = ec2_client.create_image(
        InstanceId=instance_id,
        Name=f"AMI for {instance_id}",
        Description=f"AMI created for {instance_id}",
        NoReboot=True  # Set this to False if you want to reboot the instance during the AMI creation process
    )

    # Get the instance type of the instance
    instance_type = ec2_client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['InstanceType']

    # Add a tag to the created AMI with the instance type
    ami_id = response['ImageId']
    ec2_client.create_tags(
        Resources=[ami_id],
        Tags=[{'Key': 'InstanceType', 'Value': instance_type}]
    )

    print(f"AMI {ami_id} created for instance {instance_id} with InstanceType tag set to {instance_type}")
