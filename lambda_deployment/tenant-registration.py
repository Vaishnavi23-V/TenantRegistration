import json
import uuid
import requests


def register_tenant(event, context):
    print("event:",)
    print(event)
    try:
        # Generate a unique user ID
        tenant_id = str(uuid.uuid4())

        # Get tenant details from event
        tenant_details = event
        print(tenant_details)
        
        # Add generated tenant ID to the user details
        tenant_details['tenantId'] = tenant_id
        print(tenant_details)
        
        create_admin_tenant(tenant_details)
        
        return {
            "statusCode": 200,
            "body": "Tenant creation is successful."
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }

def create_admin_tenant(tenant_details):
    try:
        url = "https://5npujorei3.execute-api.us-east-1.amazonaws.com/prod/user/tenant-admin"
        print("calling create admin tenant api")
        
        response=requests.post(url, json=tenant_details, timeout=5) 
        print("response:",response)
    except requests.RequestException as e:
        print(f"Error creating user: {e}")