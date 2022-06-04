# coding_exercise
Coding exercise for search engine revenue identification from hit level data.

# AWS Apps used:
Executing transformation:
AWS Lambda

Storage:
S3

Code Repository:
Github

CI/CD:
Code Build
Code Deploy
Code Pipeline
Cloudformation

Logs/Monitoring:
Cloudwatch

Roles created in AWS:
Cloudformation role
Lambda role


# Process of Execution:

Event based Trigger:
This is serverless architecture where code is processing in AWS Lambda which scales and runs in mutiple instances based on the volume/load on the server.
when hit file placed in s3 bucket, event is triggered and it kicks off lambda function which inturn runs business rules and generate revenue for the search engine domains. Output file will be loaded to S3 bucket.

Cloudformation template is used to create required S3 buckets and lambda function through pipeline. 
Cloudformation packages the code and creates change set, once pipline executes this change set, required artifacts are created in AWS and code is deployed. 

Steps to run the code:
1. Place data.tsv hit data file in S3 input bucket = search-engine-revenue-input
2. S3 event will be triggered and Lambda function wil be kicked off to run the code.
3. check output file generated in S3 Output Bucket = search-engine-revenue-output






