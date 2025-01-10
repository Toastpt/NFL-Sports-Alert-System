
# NFL Sports Alerts System

## **Project Overview**
This project is an alert system that sends real-time NFL game day score notifications to subscribed users via SMS/Email. It leverages **Amazon SNS**, **AWS Lambda and Python**, **Amazon EvenBridge** and **NFL APIs** to provide sports fans with up-to-date game information. The project demonstrates cloud computing principles and efficient notification mechanisms.  

---

## **Features**
- Fetches live NFL game scores, game status and stadium played using an external API.
- Sends formatted score updates to subscribers via SMS/Email using Amazon SNS.
- Scheduled automation for regular updates using Amazon EventBridge.
-Security is a priority for all cloud based projects with least privileges assigned

## **Prerequisites**
- Free account with subscription and API Key at [sportsdata.io](https://sportsdata.io/)
---

## **Technical Architecture**
![Sports Notification](https://github.com/user-attachments/assets/d7a1f1b3-d426-4a1b-b69a-a525fa1ae726)

---


## **Technologies**
- **Cloud Provider**: AWS
- **Core Services**: SNS, Lambda, EventBridge
- **External API**: NBA Game API (SportsData.io)
- **Programming Language**: Python 3.x
- **IAM Security**:
  - Least privilege policies for Lambda, SNS, and EventBridge.

---

## **Project Structure**
```bash
game-day-notifications/
├── src/
│   ├── gameday_notifications.py          # Main Lambda function code
├── policies/
│   ├── gameday_sns_policy.json           # SNS publishing permissions
│   ├── gameday_eventbridge_policy.json   # EventBridge to Lambda permissions
│   └── gameday_lambda_policy.json        # Lambda execution role permissions
├── .gitignore
└── README.md                        # Project documentation
```

Setup Instructions
This guide will walk you through setting up a notification system using AWS Lambda, SNS, and EventBridge, integrated with an external API. You'll learn how to deploy the Lambda function, configure AWS services, and ensure secure and automated operations.

### **Create an SNS Topic**
1. Open the AWS Management Console.
2. Navigate to the SNS service.
3. Click Create Topic and select Standard as the topic type.
4. Name the topic (e.g., gd_topic) and note the ARN.
5. Click Create Topic.

### **Add Subscriptions to the SNS Topic**
1. After creating the topic, click on the topic name from the list.
2. Navigate to the Subscriptions tab and click Create subscription.
3. Select a Protocol:
- For Email:
  - Choose Email.
  - Enter a valid email address.
- For SMS (phone number):
  - Choose SMS.
  - Enter a valid phone number in international format (e.g., +1234567890).

4. Click Create Subscription.
5. If you added an Email subscription:
- Check the inbox of the provided email address.
- Confirm the subscription by clicking the confirmation link in the email.
6. For SMS, the subscription will be immediately active after creation.

### **Create the SNS Publish Policy**
1. Open the IAM service in the AWS Management Console.
2. Navigate to Policies → Create Policy.
3. Click JSON and paste the JSON policy from gameday_sns_policy.json file
4. Replace REGION and ACCOUNT_ID with your AWS region and account ID.
5. Click Next: Tags (you can skip adding tags).
6. Click Next: Review.
7. Enter a name for the policy (e.g., gd_sns_policy).
8. Review and click Create Policy.

### **Create an IAM Role for Lambda**
1. Open the IAM service in the AWS Management Console.
2. Click Roles → Create Role.
3. Select AWS Service and choose Lambda.
4. Attach the following policies:
- SNS Publish Policy (gd_sns_policy) (created in the previous step).
- Lambda Basic Execution Role (AWSLambdaBasicExecutionRole) (an AWS managed policy).
5. Click Next: Tags (you can skip adding tags).
6. Click Next: Review.
7. Enter a name for the role (e.g., gameday_role).
8. Review and click Create Role.
9. Copy and save the ARN of the role for use in the Lambda function.

### **Deploy the Lambda Function**
1. Open the AWS Management Console and navigate to the Lambda service.
2. Click Create Function.
3. Select Author from Scratch.
4. Enter a function name (e.g., gd_notifications).
5. Choose Python 3.x as the runtime.
6. Assign the IAM role created earlier (gameday_role) to the function.
7. Under the Function Code section:
- Input Python code in the inline editor.
8. Under the Environment Variables section, add the following:
- NFL_API_KEY: your NFL API key.
- SNS_TOPIC_ARN: the ARN of the SNS topic created earlier.
9. Click Create Function.


### **Set Up Automation with Eventbridge**
1. Navigate to the Eventbridge service in the AWS Management Console.
2. Go to Rules → Create Rule.
3. Select Event Source: Schedule.
4. Set the cron schedule for when you want updates (e.g., hourly). I chose to monitor Sunday, Thursday and Saturday games
5. Under Targets, select the Lambda function (gameday_notifications) and save the rule.

![Screenshot 2025-01-09 at 10 58 45 PM](https://github.com/user-attachments/assets/c540a2a1-cc88-468a-b5c4-722f3be1b316)


### **Test the System**
1. Open the Lambda function in the AWS Management Console.
2. Create a test event to simulate execution.
3. Run the function and check CloudWatch Logs for errors.
4. Verify that SMS notifications are sent to the subscribed users.

<img width="329" alt="Screenshot 2025-01-09 at 10 44 23 PM" src="https://github.com/user-attachments/assets/822a4ae1-9697-4863-97d4-055414c07864" />

Cleanup (Optional)
If you no longer need the system, delete the resources to avoid unnecessary costs:

-Delete the Lambda function.
-Delete the SNS topic and its subscriptions.
-Delete the EventBridge rule.

### **What We Learned**
1. Combined SNS with Lambda to create an effective event-driven system.
2. Followed the principle of least privilege by granting minimal permissions required for Lambda to access SNS and other AWS services.
3. By combining EventBridge with Lambda, we created a fully automated, serverless workflow.
4. Integrating external APIs into cloud-based workflows.


### **Future Enhancements**
1. Implement an interactive visual interface
2. Track multiple games amongst different sports
3. Implement system amongst other industries
