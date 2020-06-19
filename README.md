# listinstances
List instances in all regions in AWS account

- Asks for tags to list instances having a specific tag (optional)

List instances all regions in your AWS account and returns the following information

InstanceId, PublicIP, AZ, Instance Type, State(Running/Stopped) and whether its within free tier

Usage: 

From the shell, 

python main.py

To list instance of a specific tag:
Would you like to list instances selectively using tags? (Enter 'Y'|'N'): Y
Enter Tag key: xxxxx
Enter Tag value: xxxxx

To just list all instances:
Would you like to list instances selectively using tags? (Enter 'Y'|'N'): N

Ensure access and secret keys are configured or the instance has correct role attached and has permissions to run the describe-instances API call.
Run with Python 2.7
