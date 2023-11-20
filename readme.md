# Project description

## Overview

Fetch and process app is a servless api to allows you to

Deploy this Chalice app using AWS Lambda and API Gateway.

**External API Integration:**

Use any public API (e.g., JSONPlaceholder, REST Countries) or a mock API service.
Implement a mechanism to handle rate limits and possible errors from the external API.

## Setup and deployment

0. Install and configura aws cli
1. Create an aws user with the required role and permisions (lambda, cloudwatch, cloudformation, codepipeline, s3, IAM, APIGateway, codeDeploy, DynamoDB, SecretsManager)
2. Create a github repo and upload this source code
3. Create an aws access key https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sts/assume-role.html

    save your credentials

    ```bash
    $ cd ~/
    $ mkdir .aws
    $ cd .aws
    $ vim ~/.aws/credentials
    ```

    save the folowing

    ```
    [default]
    aws_access_key_id=*****
    aws_secret_access_key= ******
    ```

    Replace **** with your own credentials

4. Create an OAuth key pair from github and store it as an aws secret

    ``` bash 
    $ vim ///tmp/secret.json 
    ```

    write your github secret
    ```
    {"OAuthToken": "ghp_**********"}
    ```

    save it with aws secrets

    ``` bash
    $ aws secretsmanager create-secret --name FUTURELOOPACCESSTOKEN         --description "Token for Github Repo Access" --secret-string file:///tmp/secret.json
    ```

5. deploying it 

    In the following lines please replace GithubOwner and GithubRepoName using your repository data

    ``` bash
    $ aws cloudformation deploy --template-file pipeline.json \
        --stack-name FetchProcess --parameter-overrides \
        GithubOwner= selobu \
        GithubRepoName= fetchprocess \
        GithubRepoSecretId=FUTURELOOPACCESSTOKEN \
        --capabilities CAPABILITY_IAM
    ```

6. Protect your cloud formation generated to prevent unwanted deletion.

7. You can get the generated development deployed endpoint using the script 

    ```
    $ . getcurrenturl.sh
    ```

## dabase description

Tablename | Simple  Primary key | description
---|---|---
Demo | id | store data retrieved from de selected api endpoint
ratelimit | timestamp | store request to limit maximum request per a given time


### Sample data

**Demo** database

``` JSON
{
    "Demo": [
        "PutRequest":{
            "Item":{
                "Id": { "N": "12" },
                "Timestamp":{ "S" : "1657909397" },
                "title": { "S": "title" },
                "body": { "S": "<div>Some content</div>" },
                "userID":{ "N": "12541" }
            }
        }
    ]

}
```

**RateLimit** database

``` JSON
{ "RateLimit": [
    "PutRequest":{
        "Item":{
            "timestamp" : [ "S": "1657909382"]
        }
    }

]}

```


## Local deployment


```
    $ chalice local --port 8001
```

The chalice app should be running in http://127.0.0.1:8001


## api docs

endpoints:


/fetch-data: Triggers data fetch from the external API.
/view-data: Displays stored results.
/status: Provides information on the last fetch (e.g., timestamp, number of items fetched, any errors).

Detailed api information https://app.swaggerhub.com/apis/SELOBU_1/futureloop/1.0.0  (in progress)

## logging format

By default de app use the follogin format, for detailed information please read https://docs.python.org/3.9/library/logging.html

` %(asctime)s - %(name)s - %(levelname)s - %(message)s `

## decisions making

1. Create a sonfiguration file to read general information such as app name, fetch url endpoints
2. DB: selected dynamodb to store information
3. Security: JWT to protect endpoints
4. API docs: selected restapi but the framework is lacking of automatically sawagger structure generation, so I choose swaggerhub to create the api documentation.
5. Create a hack to enforce custom logging format
