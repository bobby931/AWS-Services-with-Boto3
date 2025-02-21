import boto3
import os

# Instantiate boto3 resource for S3 and name your bucket 
s3 = boto3.resource('s3')

bucket_name = 'crud-abbb'

# Check if the bucket exists
all_my_buckets = [bucket.name for bucket in s3.buckets.all()]
print("All buckets:", all_my_buckets)  # Debug print

# Create the bucket if it does not exist
if bucket_name not in all_my_buckets:
    try:
        print(f"{bucket_name} bucket does not exist. Creating now...")
        s3.create_bucket(Bucket=bucket_name)
        print(f"{bucket_name} bucket created successfully.")
    except Exception as e:
        print(f"Error creating bucket: {e}")
else:
    print(f"{bucket_name} already exists. No need to create a new one.")

# Define file paths
file1 = 'file1.txt'
file2 = 'file2.txt'


#upload file to new bucket
s3.Bucket(bucket_name).upload_file(Filename=file1, Key=file1)
 

# Read and print the file from the bucket
obj = s3.Object(bucket_name, file1)
body = obj.get()['Body'].read()
print(body)

#Update File 1 in bucket with content of file2
s3.Object(bucket_name, file1).put(Body=open(file2, 'rb'))
obj = s3.Object(bucket_name, file1)
body = obj.get()['Body'].read()
print(body)

# Delete File from Bucket
s3.Object(bucket_name, file1).delete()

#Delete Bucket
bucket = s3.Bucket(bucket_name)
bucket.delete()

