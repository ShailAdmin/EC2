import boto3

# Initialize Boto3 clients for both source and destination regions
source_region = 'us-east-1'  # Replace with the source region
destination_region = 'us-west-2'  # Replace with the destination region

source_ec2 = boto3.client('ec2', region_name=source_region)
destination_ec2 = boto3.client('ec2', region_name=destination_region)

# Function to copy an AMI with the same tags and name
def copy_ami(source_ami_id):
    # Get source AMI details
    response = source_ec2.describe_images(ImageIds=[source_ami_id])
    source_ami = response['Images'][0]

    # Copy the AMI to the destination region
    response = source_ec2.copy_image(
        SourceImageId=source_ami_id,
        SourceRegion=source_region,
        Name=source_ami['Name'],  # Use the same name
        Description=source_ami['Description'],
    )

    destination_ami_id = response['ImageId']

    # Wait for the AMI to be available in the destination region
    waiter = destination_ec2.get_waiter('image_available')
    waiter.wait(ImageIds=[destination_ami_id])

    # Get source AMI tags and apply them to the destination AMI
    tags = source_ami.get('Tags', [])
    if tags:
        destination_ec2.create_tags(
            Resources=[destination_ami_id],
            Tags=tags
        )

    return destination_ami_id

# Replace 'source_ami_id' with the ID of the source AMI you want to copy
source_ami_id = 'ami-XXXXXXXXXXXXXXXXX'

# Copy the AMI to the destination region
destination_ami_id = copy_ami(source_ami_id)
print(f"Copied AMI {source_ami_id} to {destination_region} as {destination_ami_id}")
