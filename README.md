
  

# Friendsurance Challenge

  

  

## Application

  

  

The challenge`s objective is complete the following topics:

  

  

* Create na API using Python with this requirements:

  

* Receive a POST request with an image URL

  

* The application will have an endpoint that can receive an HTTP request

  

* Download that image

  

* Upload the Image in a S3 Bucket

  

* Receive a GET request

  

* The reponse should be a list of images stored in S3

  

* Interact with a Database

  

* Create a table with store the following data

  

* Name of the image (the name received in the request)

  

* Original link of the image (the link received in the request)

  

* Path to the image in S3 (bucket + key name)

  

* Timestamp of when the image was stored in S3

  

* Create Instructions how to Deploy de Application

  

  

## Infrastructure

  

  

* All the infrastructure should be in AWS

  

* The infrastructure should be created using CloudFormation

  

* Create instructions how to deploy that Infrastructure

  
  

### Deploying the Infrastructure

  

#### Pre requisites

  

1. First of all you should to have an AWS account: https://console.aws.amazon.com/

2. Create an IAM: https://console.aws.amazon.com/iam/home , I created a user with administrator access, so i can manage everything by cli

3. Install AWS Cli: https://docs.aws.amazon.com/pt_br/cli/latest/userguide/cli-chap-install.html

  

#### Setting up the environment

1. Configure your local machine

    alisson@alisson-avell:~$ aws configure
    
    AWS Access Key ID [****************K3PT]: YOUR_AWS_ACCESS_KEY
    
    AWS Secret Access Key [****************JPrR]: YOUR_AWS_SECRET_KEY
    
    Default region name [us-east-2]: us-east-2
    
    Default output format [None]:

  

2. Test if aws cli is ok:

    alisson@alisson-avell:~$ aws cloudformation list-stacks
    
    {
    
    "StackSummaries": []
    
    }

  
  

#### Deploying the infrastructure

  

Inside of this repo there is a folder named infrastructure, where you should found a template.yaml.

This template will create an stack deploy:

1. One IAM Role to manage de EKS Cluster

2. One VPC

3. Two Subnets, cause it is a requirement for EKS Cluster, so we can have a high availability

4. One Security Group

5. One S3 Bucket where we will store the application images

6. The EKS Cluster that will run the application

7. A ECR to store the application image

8. An RDS Server where we will store the metadata.

  

Create the Stack:

    aws cloudformation create-stack --stack-name challenge --template-body file://template.yaml --capabilities CAPABILITY_IAM --disable-rollback --parameters ParameterKey=DBUser,ParameterValue="alisson" ParameterKey=DBPassword,ParameterValue="teste123"

  

To see if something went wrong run this command:

    $ aws cloudformation list-stacks
    
    {
    
    "StackSummaries": [
    
    {
    
    "StackId": "arn:aws:cloudformation:us-east-2:360560397478:stack/challenge/e4821ac0-d188-11e9-ad50-0285144e27ac",
    
    "DriftInformation": {
    
    "StackDriftStatus": "NOT_CHECKED"
    
    },
    
    "StackStatusReason": "The following resource(s) failed to create: [challengedb, eksrole, alissonfriendsbucket, challengevpc]. ",
    
    "CreationTime": "2019-09-07T16:05:37.676Z",
    
    "StackName": "challenge",
    
    "StackStatus": "CREATE_FAILED"
    
    }
    
    ]
    
    }

  

To know what went wrong run this command:

  

    aws cloudformation describe-stack-events --stack-name challenge

  

An example of error:

    {
    
    "StackId": "arn:aws:cloudformation:us-east-2:360560397478:stack/challenge/e4821ac0-d188-11e9-ad50-0285144e27ac",
    
    "EventId": "challengedb-CREATE_FAILED-2019-09-07T16:05:41.211Z",
    
    "ResourceStatus": "CREATE_FAILED",
    
    "ResourceType": "AWS::RDS::DBInstance",
    
    "Timestamp": "2019-09-07T16:05:41.211Z",
    
    "ResourceStatusReason": "Cannot find version 5.6.13 for mysql (Service: AmazonRDS; Status Code: 400; Error Code: InvalidParameterCombination; Request ID: 6711bace-082d-4ba6-9807-d965b6fc2bc9)",
    
    "StackName": "challenge",
    
    "ResourceProperties": "{\"MasterUserPassword\":\"teste123\",\"EngineVersion\":\"5.6.13\",\"DBInstanceClass\":\"db.t3.micro\",\"MasterUsername\":\"alisson\",\"DBName\":\"challengedb\",\"Engine\":\"MySQL\",\"AllocatedStorage\":\"5\"}",
    
    "PhysicalResourceId": "",
    
    "LogicalResourceId": "challengedb"
    
    },

  

To deploy again run:

    aws cloudformation delete-stack --stack-name challenge

  

And create the Stack again.
If everything goes well, you will receive this:

        aws cloudformation describe-stacks
        {
            "Stacks": [
                {
                    "StackId": "arn:aws:cloudformation:us-east-2:360560397478:stack/challenge1/c7a48210-d18a-11e9-bf2d-02649197f7a0", 
                    "DriftInformation": {
                        "StackDriftStatus": "NOT_CHECKED"
                    }, 
                    "Parameters": [
                        {
                            "ParameterValue": "teste123", 
                            "ParameterKey": "DBPassword"
                        }, 
                        {
                            "ParameterValue": "alisson", 
                            "ParameterKey": "DBUser"
                        }
                    ], 
                    "Tags": [], 
                    "CreationTime": "2019-09-07T16:15:59.676Z", 
                    "Capabilities": [
                        "CAPABILITY_IAM"
                    ], 
                    "StackName": "challenge1", 
                    "NotificationARNs": [], 
                    "StackStatus": "CREATE_COMPLETE", 
                    "DisableRollback": true, 
                    "RollbackConfiguration": {}
                }, 
