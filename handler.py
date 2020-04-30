import json
import numpy as np
import os
import boto3
import pickle
import sklearn

def handler(event, context):
    
    print ('Event', event)
    user_features = event['user_features']
    
    user_features =  [52000, 6.47072538,  5.99418979,  4.2856596 ,  1.24035892, 12.25743824,
         1.22741581,  6.95454665, 10.68485591,  8.01601715,  5.11749038,
         3.        ]
         
    s3_client = boto3.client('s3')     

    #bucket = 'sagemaker-us-east-1-595380434278'
    #prefix = 'sagemaker/capstone'
    #response = s3_client.get_object(Bucket=bucket, Key=os.path.join(prefix, 'trained_kmeans.pkl'))#.decode('utf8')
    #body = response['Body'].read()
    #kmeans = pickle.loads(body)
         
    print (user_features)         
    # Call prediction function from sagemaker        
    
    #runtime = boto3.Session().client('sagemaker-runtime')

    payload = json.dumps(user_features)

    # Now we use the SageMaker runtime to invoke our endpoint, sending the review we were given
    #response = runtime.invoke_endpoint(EndpointName = 'kmeans-2020-04-27-16-04-50-554',    # The name of the endpoint we created
    #                                   ContentType = 'application/json',                 # The data format that is expected
    #                                   Body = payload)                       # The actual review

    # The response is an HTTP response whose body contains the result of our inference
    #result = response['Body'].read().decode('utf-8')
    
    #result = json.loads(response['Body'].read().decode())
    #res = result['predictions']
    #
    user_cluster = 3
    
    return {
        'statusCode': 200,
        'payload': payload,
        'cluster': user_cluster
    }