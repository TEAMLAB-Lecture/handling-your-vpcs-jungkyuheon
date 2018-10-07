import boto3
import os
import botocore
# Create an S3 client
s3 = boto3.client('s3')

# Call S3 to list current buckets
response = s3.list_buckets()

# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]

# Print out the bucket list
#print("Bucket List: %s" % buckets)

#s3 = boto3.client('s3', region_name="ap-southeast-1")
bucket_name = input("bucket name:")

filename ="myapp.log"


if bucket_name not in buckets:
    response = s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-southeast-1'
            }
        )
    print(response)
    print("Successfully created")
    s3 = boto3.client('s3')
    s3.upload_file( filename, bucket_name, filename)
    print("file uploaded")
else :
    print("bucket already exist")
    try:
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).download_file(filename, 'old_myapp.log')
        first_file = open("old_myapp.log")
        second_file = open("myapp.log")

        # read lines
        first_lines = first_file.readlines()
        second_lines = second_file.readlines()

        # remove new line characters
        first_lines = [line.strip() for line in first_lines]
        second_lines = [line.strip() for line in second_lines]

        # empty dictionary to store the unique lines.
        final_lines = {}

        # loop through each lines, if the line is not present in the
        # keys of the dictionary, create an entry in dictionary
        # assigning any value (0).
        for line in first_lines:
            if line not in final_lines.keys():
                final_lines[line] = 0

        for line in second_lines:
            if line not in final_lines.keys():
                final_lines[line] = 0

        # join the lines with "\n'
        lines = "\n".join(list(final_lines.keys()))

        # write the output to a text file
        file = open("myapp.log", "w")
        file.write(lines+"\n")

        # close the text file.
        file.close()


        s3 = boto3.client('s3')
        s3.upload_file( 'myapp.log', bucket_name, filename)
        print("file uploaded")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
        s3 = boto3.client('s3')
        s3.upload_file( filename, bucket_name, filename)
        print("file uploaded")
