import boto3

def stop_ec2_instances(region_name):
    """
    Stops all running EC2 instances in a given AWS region.
    """
    print(f"Checking EC2 instances in region: {region_name}")
    ec2 = boto3.client('ec2', region_name=region_name)

    # Retrieve all running EC2 instances
    response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    
    instances_to_stop = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_to_stop.append(instance['InstanceId'])

    if instances_to_stop:
        print(f"Stopping instances: {instances_to_stop}")
        ec2.stop_instances(InstanceIds=instances_to_stop)
    else:
        print("No running instances found.")

def main():
    """
    Iterates over all AWS regions and stops running EC2 instances.
    """
    session = boto3.Session()
    regions = [region['RegionName'] for region in session.client('ec2').describe_regions()['Regions']]

    for region in regions:
        stop_ec2_instances(region)

if __name__ == "__main__":
    main()
