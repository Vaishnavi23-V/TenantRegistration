from aws_cdk import (
    aws_apigateway as apigateway,
    aws_cognito as cognito, 
    Stack,
    aws_iam as iam
)
from constructs import Construct
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.aws_apigateway import LambdaRestApi
from aws_cdk.aws_cognito import UserPool, UserPoolClient

class TenantRegistrationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
    # Lambda Function
        tenant_registration = Function(
            self, "TenantRegistration",
            runtime=Runtime.PYTHON_3_9,
            handler="tenant-registration.register_tenant",
            code=Code.from_asset("lambda_deployment"),
        )

        user_management = Function(
            self, "TenantAdminUserFunction",
            runtime=Runtime.PYTHON_3_9,
            handler="user-management.create_tenant_admin_user",
            code=Code.from_asset("lambda_deployment"),
        )

        # API Gateway 
        api = LambdaRestApi(
            self, "RegistrationApi",
            handler=tenant_registration,
        )

        # Add resource for api gateway with specific http methods
        registration_resource = api.root.add_resource("registration")
        registration_resource.add_method(
            http_method="POST",
             integration=apigateway.LambdaIntegration(
                handler=tenant_registration,
                proxy=True
            )
            )
        
        user_resource = api.root.add_resource("user").add_resource("tenant-admin")
        user_resource.add_method(
            http_method="POST",
            integration=apigateway.LambdaIntegration(
                handler=user_management,
                proxy=True
            )
        )

         # Cognito User Pool
        user_pool = UserPool(self, "TenantUserPool")

        # Cognito User Pool Client
        user_pool_client = UserPoolClient(
          self, "TenantUserPoolClient",
          user_pool=user_pool,
          o_auth=cognito.OAuthSettings(
              flows=cognito.OAuthFlows(
              implicit_code_grant=True,  
              authorization_code_grant=False  
    ),
      scopes=[cognito.OAuthScope.OPENID],
          )
)

        # Custom domain for the User Pool
        user_pool_domain = cognito.CfnUserPoolDomain(
            self, "TenantUserPoolDomain",
            user_pool_id=user_pool.user_pool_id,
            domain="my-cloud-platform"
        )

        # Grant permissions for Cognito to use the custom domain
        user_pool_domain.node.add_dependency(user_pool)
        user_pool_domain.node.add_dependency(user_pool_client)

         # Add permissions to the Lambda function's IAM role to allow calling CreateGroup operation in Cognito
        user_management.role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["cognito-idp:CreateGroup", 
                        "cognito-idp:AdminCreateUser",
                        "cognito-idp:AdminAddUserToGroup"],
                resources= ["arn:aws:cognito-idp:us-east-1:723094108107:userpool/us-east-1_jDEPOze1y"],
            )
        )