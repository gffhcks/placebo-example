import boto3
import placebo
import argparse


def main():
    '''
    Query AWS for the state of 10 EC2 instances.
    Record or playback with Placebo.
    '''
    # Command line arguments
    parser = argparse.ArgumentParser(description='A sample Placebo project.')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--path', default='.', help='JSON recording path')
    parser.add_argument('--prefix',
                        help='Recording prefix (for multiple data sets)')

    placebo_group = parser.add_mutually_exclusive_group()
    placebo_group.add_argument('--record', action='store_true',
                               help='Record AWS calls')
    placebo_group.add_argument('--playback', action='store_true',
                               help='Playback AWS calls')
    parser.epilog = '''Pass AWS credentials via environment variables:
    $AWS_ACCESS_KEY_ID and $AWS_SECRET_ACCESS_KEY, or $AWS_PROFILE'''
    args = parser.parse_args()

    # Establish a Boto3 session
    session = boto3.Session()
    # Create a Placebo pill - use JSON files in the specified location.
    pill = placebo.attach(session, data_path=args.path, prefix=args.prefix)

    # Begin recording or playback
    if args.record:
        pill.record()
    elif args.playback:
        pill.playback()

    ec2 = session.client('ec2', region_name=args.region)

    # Get info about all instances, narrow down to a list of instance IDs
    response = ec2.describe_instances()
    reservations = response['Reservations']
    instance_lists = [reservation['Instances'] for reservation in reservations]
    instances = [instance for ilist in instance_lists for instance in ilist]
    instance_ids = [instance['InstanceId'] for instance in instances]

    # Get the instance state for each instance ID
    for instance_id in instance_ids:
        status = ec2.describe_instance_status(InstanceIds=[instance_id],
                                              IncludeAllInstances=True)
        state = status['InstanceStatuses'][0]['InstanceState']['Name']
        print instance_id + " " + state


if __name__ == '__main__':
    main()
