# Step 3 - AWS Infrastructure

> Approximate time: 25-30 minutes

Time to setup all the AWS resources. In this lab, we'll setup the Lambda Functions, API Gateway and DynamoDB instances. We are going bottom up on this, from DB to API Gateway.

If you are familiar with the AWS console, the lab is fairly quick to perform.

![Infrastructure](../assets/dive-into-iot.png)

> If this current documentation feels dated, please refer the official AWS documentation on each of the topics.

<!-- > If the lab is running late, I might ask you to run the CF script, which build the whole setup for you. -->

## IAM Role

Let's create a simple IAM role, which is a catch all role for this lab. It is not the recommended route, but in interest of time, we are going to follow this process. For a proper application you should follow the [**"Best Practices"**](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

### Create a New Role

> Please delete this role later, we are giving very broadstroke permissions here, only for the purpose of this lab. This is not the recommended route, you should **ONLY** give the required permissions in real world scenarios.

 * Get to AWS [IAM Console](https://console.aws.amazon.com/iam/)
 * Select **Roles** from the menu on the left under **Access Management**
 * Click on **Create Role**
 * Under Type pick **AWS Service**
 * Under **Choose the service that will use this role**, select **Lambda**
 * Click on **Next: Permissions**
 * Under policy, **Attach** the following policies
   * `AmazonAPIGatewayInvokeFullAccess`
   * `AmazonDynamoDBFullAccess`
   * `AWSLambdaBasicExecutionRole`
   * `AWSIoTFullAccess`
   > This is **stricly** not recommended for production.
 * Hit **Save** and this is ready to use!

## DynamoDB

We need a simple DynamoDB table to capture the IoT data received from the sensor.

| Column | Type | Purpose |
| ----- |------| --------|
|Item   | String  | This is the partition key, and also the hardware component for which the data is being registered.  |
|State   | String   | What did the sensor read (dark/light), or current LED status |
|Level   | Number  | Amount of light detected by sensor  |
|Timestamp   | Datetime  | Time the event occurred  |
| ExpirationTime(TTL)  | TTL   | Time to live, after which the data will be deleted, so we can keep our tables clean |

## Lambda Function to turn on LED

A simple python lambda function to process API request and send it as an MQTT message to the pi.

### Steps to create one

 * Got to [Lambda Console](https://console.aws.amazon.com/lambda)
 * Click **Create function** to create a new function.
 * Select **Use a blueprint**
 * Under the **Blueprints** search, type "Hello"
 * Select `hello-world-python`
 * Click **Configure**
 * Give a useful **Function Name** e.g. `<YOUR_THING_NAME>-led-flasher`
 * **Use an existing role**, and pick the role you've created in the **IAM Role section** above.
 * Click **Create Function**  to actually create a function.

### The function

Once the function has been created, you can copy the code listed below to **Function Code**

```
import json
import boto3

print('Received message from API gateway')


def lambda_handler(event, context):

    print ('Lambda Invoked')
    client = boto3.client('iot-data', region_name='us-east-1')
    print(event)

    # Change topic, qos and payload as appropriate.
    response = client.publish(
        topic='$aws/things/FlyingZombieAttach_Pi/flasher',
        qos=1,
        payload=str(event['led'])
    )

    print('Response')
    print(response)

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        }
    }
```

### Other Settings

 * Under **Tags**, add valid, useful tags, which will help you identify this lambda function, if using a shared account.
 * Change **Description** of lambda function under **"Basic Settings"**
 * Leave the rest of the settings as is for now.

## API Gateway

There are two ways to setup the API Gateway on the console, you can either continue setting it as an **Add Trigger** from the **Lambda Designer** section, or go to API Gateway and do it from there.

I prefer is from the API gateway section, the rest of the document follows the steps.

> Our API gateway is **Open**, which means anyone with the URL can access it, please delete it after the lab. Ideally you would front it using Cognito to prevent unauthorized access.

### Setup API gateway, fronting a Lambda Function

 * Go to AWS Console for [API Gateway](https://console.aws.amazon.com/apigateway/)
 * Click **Create API**
 * Select **REST API**, click on **Build**
   * (not the private one )
 * Leave the protocol as **REST**, **New API**
 * Give it a valid name e.g. `<YOUR_THING_NAME>-apig`
 * Click **Create**

Your API should now send you to a new screen

### Setup Resources

 * Click on the **Action** button on the top
 * Select **Create Resource**, a new screen to define a resource should pop up.
 * Give a **Resource Name** e.g. `flasher`, copy the same value to **Resource Path**
 * Check **Enable API Gateway CORS** (do we need this ? confirm config and update...)
 * With `flasher` highlighted, click on **Action -> Create Method**
 * Select `POST` from the dropdown, and hit the small checkbox
 * Choose **Integration Type** ~ `Lambda Function`
 * Check **Use Lambda Proxy integration**
 * Under the textbox for **Lambda Function**, type the name of your Lambda function defined above.
 * An alert will pop-up confirming permissions, hit **Ok** to confirm.

### Deploy API

 * Click on `flasher`, and highlight it again.
 * Click on **Actions -> Deploy API**
 * A pop-up asking for `stage` shows up, choose **[New Stage]**, under **Deployment Stage**
 * Give a **Stage Name** e.g. `lab`
 * A new screen with **Invoke URL** on a blue highlight should pop-up.
 * Copy this URL to a text editor. This is the URL, where the API is published.
   * `https://<YOUR_URL>.execute-api.us-east-1.amazonaws.com/lab/flasher`


## Lambda Function to Log LED status (this might not work)
> something is missing in config 

Every time the LED glows or a garbage message is received, it gets logged to DynamoDB

### Steps to create one

 * Got to [Lambda Console](https://console.aws.amazon.com/lambda)
 * Click **Create function** to create a new function.
 * Select **Use a blueprint**
 * Under the **Blueprints** search, type "Hello"
 * Select `hello-world-python`
 * Click **Configure**
 * Give a useful **Function Name** e.g. `<YOUR_THING_NAME>-logger`
 * **Use an existing role**, and pick the role you've created in the **IAM Role section** above.
 * Click **Create Function**  to actually create a function.

### The function

```
import boto3
from datetime import datetime

'''
Will be called by the Pi to update the Last Known Good State in Dynamo
'''

def lambda_handler(event, context):
    dynamo = boto3.client("dynamodb")
    now = datetime.now()

    item = {
        "received_timestamp": {
            "S": now.strftime("%m/%d/%Y, %H:%M:%S.%f")
        },
        "timestamp": {
          "S": event["timestamp"]  
        },
        "status": {
            "S": event["state"]
        }
    }

    response = dynamo.put_item(TableName="<YOUR_THING_NAME>-EventLog", Item=item, ReturnConsumedCapacity='TOTAL')

    return {
        'statusCode': 200,
        'body': response
    }
```

## IoT Rule (the new way)
[**IoT Rules**](https://docs.aws.amazon.com/iot/latest/developerguide/iot-rules.html) are a new introduction to the IoT core. Instead of using Lambda functions to be triggered off an MQTT event and then handle the payload, there are now rules in place which allow you to directly channel/process data to different AWS services.

Refer the [official documentation](https://docs.aws.amazon.com/iot/latest/developerguide/iot-rules.html) for the list of possible options available.

> There is a way to directly write to DynamoDB without using the lambda function, but I've not explored this option, if you find it, please create a PR and I can update this documentation.

## Next --> [04 - Bringing it all together](../04-end-to-end)
This concludes our AWS infrastructure creation. Time to test the whole thing!
