#! /bin/bash

export AWS_PROFILE=MYPROFILE

function question(){
    echo "Enter 'cs' to create s3 bucket"
    echo "Enter 'us' to upload template to s3 bucket"
    echo "Enter 'cp' to create a stack"
    echo "Enter 'up' to update a stack"
    read -p "Enter option : " input

    if [ $input == "cs" ]
    then
        createtlbucket
    elif [ $input == "us" ]
    then
        uploadtemplate
    elif [ $input == "cp" ]
    then
        deploypackage
    elif [ $input == "up" ]
    then
        updatepackage
    else
        echo "No option"
    fi
}

function createtlbucket(){
    read -r -p "Enter a bucket name to create : " bucketname
    echo "Creating..."
    aws s3 mb s3://$bucketname --region eu-west-2
}

function uploadtemplate(){
    read -r -p "Enter a bucket name to upload : " bucketname
    echo "Uploading..."
    aws s3 cp templates/sirius_lambda_template.yaml s3://$bucketname/templates/etl_lambda_s3_template.yaml
}

function deploypackage(){
    read -r -p "Enter a stack name to create : " stackname
    echo "Creating..."
    aws cloudformation create-stack \
    --stack-name $stackname \
    --template-url https://deman4-group3.s3.eu-west-1.amazonaws.com/templates/etl_lambda_s3_template.yaml \
    --capabilities CAPABILITY_IAM \
    --region eu-west-1
    echo "Completed!."
}

function updatepackage(){
    read -r -p "Enter a stack name to update : " stackname
    echo "Updating..."
    aws cloudformation update-stack \
    --stack-name $stackname \
    --template-url https://deman4-group3.s3.eu-west-1.amazonaws.com/templates/etl_lambda_s3_template.yaml \
    --capabilities CAPABILITY_IAM \
    --region eu-west-1
    echo "Completed!."
}

question