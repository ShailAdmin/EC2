import boto3

# Initialize Boto3 clients for both source and target regions
source_region = 'us-east-1'  # Change to your source region
target_region = 'us-west-2'  # Change to your target region
ec2_source = boto3.client('ec2', region_name=source_region)
ec2_target = boto3.client('ec2', region_name=target_region)

# Function to copy all AMIs from the source region to the target region
def copy_all_amis():
    response = ec2_source.describe_images(Owners=['self'])
    amis_to_copy = response['Images']

    for ami in amis_to_copy:
        source_ami_id = ami['ImageId']
        ami_name = ami['Name']

        # Copy the AMI to the target region
        response = ec2_target.copy_image(
            SourceImageId=source_ami_id,
            SourceRegion=source_region,
            Name=ami_name,
            Description=f"Copy of {ami_name} from {source_region} to {target_region}"
        )

        target_ami_id = response['ImageId']
        print(f"AMI {ami_name} (ID: {source_ami_id}) copied to {target_region} as {target_ami_id}")

# Copy all AMIs from the source region to the target region
copy_all_amis()
