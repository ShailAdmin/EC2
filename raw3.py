import boto3

# Initialize the Boto3 EC2 client
ec2_client = boto3.client('ec2')

# Function to list your own created AMIs and return them as a list
def list_amis():
    response = ec2_client.describe_account_attributes()
    account_id = response['AccountAttributes'][0]['AttributeValues'][0]['AttributeValue']

    response = ec2_client.describe_images(Owners=[account_id])

    ami_ids = [image['ImageId'] for image in response['Images']]
    return ami_ids

# List your AMIs and store them in a variable
my_amis = list_amis()

# Print the list of AMIs or do other operations with my_amis
if my_amis:
    print("My AMIs:")
    for ami_id in my_amis:
        print(ami_id)
else:
    print("No AMIs found.")
