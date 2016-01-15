# placebo-example
A sample project for demonstrating Placebo

This is a simple command-line utility for demonstrating Placebo's recording and playback features. It uses `describe_instances` to get a list of every EC2 instance ID in the specified region, then calls `describe_instance_status` on them individually and prints their state ('running', 'stopped', 'terminated', etc.).

In `--record` mode, placebo-example will store the response to every AWS call as a JSON file. In `--playback` mode, placebo-example will reference those stored responses instead of making calls to AWS.

Passing `--prefix` allows you to store multiple recordings in the same directory. For example: `--region us-east-1 --prefix alpha` and `--region us-west-2 --prefix beta` will store data sets for both regions separately.

Try recording and playing back an execution; note the difference in execution time, and that playing back does not require any internet connection. Also note that you can directly modify the JSON recording data - try changing a 'running' instance to 'stopped'.

## Requirements

Placebo-example requires `argparse` (available in the Python 2.7 standard library), `boto3`, and `placebo`. It was originally written for Python 2.7.

## Command Line Arguments

```
usage: placebo-example.py [-h] [--region REGION] [--path PATH]
                          [--prefix PREFIX] [--record | --playback]

A sample Placebo project.

optional arguments:
  -h, --help       show this help message and exit
  --region REGION  AWS region
  --path PATH      JSON recording path
  --prefix PREFIX  Recording prefix (for multiple data sets)
  --record         Record AWS calls
  --playback       Playback AWS calls

Pass AWS credentials via environment variables: $AWS_ACCESS_KEY_ID and
$AWS_SECRET_ACCESS_KEY, or $AWS_PROFILE
```
### Example

```
# Install required packages
pip install boto3 placebo argparse

# Make the JSON data directory
mkdir ./json

# Record an execution
AWS_PROFILE=stage ./placebo-example.py --path ./json --record

# Show the recorded files
ls ./json

# Playback the execution
AWS_PROFILE=stage ./placebo-example.py --path ./json --playback
```
