
  

# Friendsurance Challenge

* This doc still not finished, i have some security group problems *  

  

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

# Deploying Application

## Setting up the environment

First of all install aws iam authenticator:

https://docs.aws.amazon.com/pt_br/eks/latest/userguide/install-aws-iam-authenticator.html


Now you can config your kubeconfig using that command:

        aws eks --region us-east-2 update-kubeconfig --name challenge
        Updated context arn:aws:eks:us-east-2:360560397478:cluster/challenge in /home/alisson/.kube/config

I'm considering that you have the kubectl installed, if you don't install using that link: https://kubernetes.io/docs/tasks/tools/install-kubectl/

To know if you are connected to cluster you can run the following commands:

        alisson@alisson-avell:~/FriendsChallenge$ kubectl config get-clusters
        NAME
        arn:aws:eks:us-east-2:360560397478:cluster/challenge
        alisson@alisson-avell:~/FriendsChallenge$ kubectl get namespaces
        NAME          STATUS   AGE
        default       Active   5m28s
        kube-public   Active   5m28s
        kube-system   Active   5m28s
        alisson@alisson-avell:~/FriendsChallenge$ 

Is mandatory to add worker nodes to the kubernetes cluster, the CloudFormation create a Role to join worker nodes in the cluster, to see that role run the command:

        aws iam list-roles

You will see something like this:

        {
            "Description": "", 
            "AssumeRolePolicyDocument": {
                "Version": "2012-10-17", 
                "Statement": [
                    {
                        "Action": "sts:AssumeRole", 
                        "Effect": "Allow", 
                        "Principal": {
                            "Service": "ec2.amazonaws.com"
                        }
                    }
                ]
            }, 
            "MaxSessionDuration": 3600, 
            "RoleId": "AROAVH4YTBSTNDZDYUOAU", 
            "CreateDate": "2019-09-08T16:06:27Z", 
            "RoleName": "challenge-NodeInstanceRole-13WTUG51LAGD2", 
            "Path": "/", 
            "Arn": "arn:aws:iam::360560397478:role/challenge-NodeInstanceRole-13WTUG51LAGD2"
        }

The ARN is importante thing, so get this value and replace in kubernetes/nodes.yaml inside this repo.
You should replace this line:

        - rolearn:  arn:aws:iam::360560397478:role/challenge-NodeInstanceRole-1Q4O4RA5S2MQ0 

After that run the command:

        $ kubectl apply -f kubernetes/nodes.yaml 
        configmap/aws-auth created

Now you can see the nodes in your cluster with this command:

        $ kubectl get nodes
        NAME                                            STATUS   ROLES    AGE     VERSION
        ip-192-168-114-38.us-east-2.compute.internal    Ready    <none>   3m53s   v1.13.8-eks-cd3eb0
        ip-192-168-166-107.us-east-2.compute.internal   Ready    <none>   3m51s   v1.13.8-eks-cd3eb0


### Building application image

I'm considering that you already have docker installed in your computer, if you don't please install: https://docs.docker.com/install/

In the repository we have a Dockerfile, to create the image, run the command:

        docker build . -t challenge

Get your RDS endpoint:

        aws rds describe-db-instances

You should see an output similitar to this:

        "DBName": "challengedb", 
            "PreferredMaintenanceWindow": "wed:04:01-wed:04:31", 
            "Endpoint": {
                "HostedZoneId": "Z2XHWR1WZ565X2", 
                "Port": 3306, 
                "Address": "cc8ieyo3kmj6w1.cy64xkoh0drv.us-east-2.rds.amazonaws.com"
            }, 
            "DBInstanceStatus": "available",


Create a temporary container to run the migrations:
    docker run --rm -ti --env S3_BUCKET="challenge-alissonfriendsbucket-1aeyanfextgbh" --env MYSQL_Connection="mysql://<YOUR_DATABASE_USER>:<YOUR_DATABASE_PASSWORD>@<DB_ENDPOINT>/challengedb"   -p 5000:5000 challenge bash

Inside of container run that commands:
        export LC_ALL=C.UTF-8
        export LANG=C.UTF-8
        cd /opt
        flask db migrate
        flask db upgrade    

Now exit the container and push to the ECR repository:
        aws ecr get-login

In the end of the output you are going to see this an url similar to that:
     https://360560397478.dkr.ecr.us-east-2.amazonaws.com

It is the url of your repository generated by CloudFormation.

To log in that repo run the command:

    $(aws ecr get-login --no-include-email --region us-east-2)

Tag your image with the repo url and push, in my case:

    docker tag challenge:latest 360560397478.dkr.ecr.us-east-2.amazonaws.com/challenge:latest
    docker push 360560397478.dkr.ecr.us-east-2.amazonaws.com/challenge:latest

At this point we have an image of our application inside ECR, we are ready to deploy.

### Deploying

Inside this repo there a kubernetes folder, where you gonna find a file deploy.yaml.

First you need to replace some environment vars:

        - name: AWS_ACCESS_KEY_ID
          value: "YOUR_ACCESS_KEY"
        - name: AWS_SECRET_ACCESS_KEY
          value: "YOUR_SECRET_KEY"
        - name: S3_BUCKET
          value: "challenge-alissonfriendsbucket-1aeyanfextgbh"
        - name: MYSQL_Connection
          value: "mysql://<YOUR_USER>:<YOUR_PASSSWORD>@cc3zrcp53x9jie.cy64xkoh0drv.us-east-2.rds.amazonaws.com/challengedb"


 Now run in the terminal:

        kubectl apply -f kubernetes/deploy.yaml
        
        service/challenge created
        deployment.apps/challenge-deploy created

You can get an public ip address from a instance using:

        aws ec2 describe-instances

And acessing on browser:

        http://18.222.162.46:30500/api/image