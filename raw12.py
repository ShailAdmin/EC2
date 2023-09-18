import boto3

# Initialize Boto3 clients for both source and target regions
source_region = 'us-east-1'  # Replace with your source region
target_region = 'us-west-2'  # Replace with your target region
ec2_source = boto3.client('ec2', region_name=source_region)
ec2_target = boto3.client('ec2', region_name=target_region)

# Function to list all AMIs in the source region
def list_amis():
    response = ec2_source.describe_images(Owners=['self'])
    return response['Images']

# Function to copy an AMI to the target region
def copy_ami(ami_id):
    response = ec2_source.copy_image(
        SourceImageId=ami_id,
        SourceRegion=source_region,
        Name='',
        Description=''
    )
    
    # Describe the copied AMI to retrieve its name and tags
    copied_ami_id = response['ImageId']
    copied_ami = ec2_target.describe_images(ImageIds=[copied_ami_id])['Images'][0]
    
    # Set the name and tags of the copied AMI to match the source AMI
    ami_name = copied_ami['Name']
    ami_tags = copied_ami.get('Tags', [])
    
    ec2_target.create_tags(
        Resources=[copied_ami_id],
        Tags=ami_tags
    )
    
    ec2_target.create_image(
        InstanceId='',
        Name=ami_name,
        Description='',
        BlockDeviceMappings=[]
    )

# List all AMIs in the source region
amis_to_copy = list_amis()

# Copy each AMI to the target region with the same name and tags
for ami in amis_to_copy:
    ami_id = ami['ImageId']
    copy_ami(ami_id)
    print(f"AMI {ami_id} copied to {target_region} with the same name and tags")
