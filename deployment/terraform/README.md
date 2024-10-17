# Blueprint Implementation Using Infrastructure as Code

### Prerequisites:
* Terraform installed
* AWS CLI installed
* AWS account

### Step by step deployment:
#### 1. Configure AWS Credentials
```shell
aws configure
```
Output:
```shell
AWS Access Key ID [None]: <YOUR_AWS_ACCESS_KEY_ID>
AWS Secret Access Key [None]: <YOUR_AWS_SECRET_ACCESS_KEY>
Default region name [None]: <YOUR_AWS_REGION>  # e.g., us-east-1
Default output format [None]: json
```
#### 2. Go to the IaC directory
```shell
cd deployment/terraform
```
#### 3. Initialize Terraform
```shell
terraform init
```

#### 4. Apply the Terraform Configuration
```shell
terraform apply
```
review the changes, then approve

#### Step 5: Verify the deployment
```shell
aws ec2 describe-instances
```

#### 6. Clean Up Resources (After usage)
```shell
terraform destroy
```
review the changes, then approve

