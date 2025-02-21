import boto3

# Create EC2 resource and instance name
ec2 = boto3.resource('ec2')
instance_name = 'ec2-ba'

# Store instance id
instance_id = None

instances = ec2.instances.all()
instance_exists = False

# Checking if instance already exists
for instance in instances:
    for tag in instance.tags:
        if tag['Key'] == 'Name' and tag['Value'] == instance_name:
            instance_exists = True
            instance_id = instance.id
            print(f"An instance named {instance_name} with id {instance_id} already exists")
            break
    if instance_exists:
        break

if not instance_exists:
    # Launch the instance
    new_instance = ec2.create_instances(
        ImageId='ami-053a45fff0a704a47',  # Replace with the desired Amazon Machine Image (AMI) ID
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',  # Replace with the desired instance type
        KeyName='key1',  # Replace with your key pair name
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name  # Corrected the syntax issue here
                    }
                ]
            }
        ]
    )
    instance_id = new_instance[0].id
    print(f"Instance named {instance_name} with id {instance_id} created")

# Stop instance
ec2.Instance(instance_id).stop()
print(f"Instance {instance_name}--{instance_id} has been stopped")

# Start instance
ec2.Instance(instance_id).start()
print(f"Instance {instance_name}--{instance_id} has been started")

# Terminate instance
ec2.Instance(instance_id).terminate()
print(f"Instance {instance_name}--{instance_id} has been terminated")
