import boto3

# Initialize the Boto3 EC2 client for the source and destination regions
source_region = 'us-east-1'  # Replace with your source region
destination_region = 'us-west-2'  # Replace with your destination region

source_ec2 = boto3.client('ec2', region_name=source_region)
destination_ec2 = boto3.client('ec2', region_name=destination_region)

# Function to copy an AMI with its tags and name
def copy_ami(ami_id):
    # Get the AMI details
    response = source_ec2.describe_images(ImageIds=[ami_id])
    ami = response['Images'][0]
    
    # Copy the AMI to the destination region
    copied_ami = destination_ec2.copy_image(
        SourceImageId=ami_id,
        SourceRegion=source_region,
        Name=ami['Name'],
        Description=ami['Description']
    )
    
    # Get the new AMI ID in the destination region
    new_ami_id = copied_ami['ImageId']
    
    # Copy the tags from the source AMI to the destination AMI
    tags = ami.get('Tags', [])
    if tags:
        destination_ec2.create_tags(Resources=[new_ami_id], Tags=tags)
    
    return new_ami_id

# List of source AMI IDs you want to copy
source_ami_ids = ['ami-XXXXXXXXXXXXXXXXX', 'ami-YYYYYYYYYYYYYYYYY']

# Copy AMIs to the destination region
for source_ami_id in source_ami_ids:
    new_ami_id = copy_ami(source_ami_id)
    print(f"Copied AMI {source_ami_id} to {destination_region} with new ID {new_ami_id}")
