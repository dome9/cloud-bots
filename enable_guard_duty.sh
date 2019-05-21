# enable_guard_duty.sh <lambda_arn> <aws_profile_name>

declare -a regions=("us-east-2" "us-east-1" "us-west-1" "us-west-2" "ap-northeast-1" "ap-northeast-2" "ap-south-1" "ap-southeast-1" "ap-southeast-2" "ca-central-1" "eu-central-1" "eu-west-1" "eu-west-2" "eu-west-3" "sa-east-1")

lambda_arn=$1

if [ -z "$2" ]; then
    # Profile not set
    profile="default"
else
    # Profile set in ARGs
    profile=$2
fi

lambda_region=`echo $lambda_arn | awk -F':' '{print $4}'`
account_id=`echo $lambda_arn | awk -F':' '{print $5}'`
lambda_name=`echo $lambda_arn | awk -F':' '{print $7}'`

## now loop through the above array
for region in "${regions[@]}"
do
    echo "### Starting work on region: " $region

    # Turn on GD
    echo "Turning on GuardDuty" 
    aws guardduty create-detector \
    --enable \
    --region $region \
    --profile $profile

    # Send the rules to CW
    echo "### Setting up CloudWatch event rule to look for GD findings"
    aws events put-rule \
    --name GuardDutyFindings \
    --event-pattern "{\"source\":[\"aws.guardduty\"]}" \
    --region $region \
    --profile $profile 

    # Create an SNS topic
    echo "### Creating SNS topic"
    sns_arn=`aws sns create-topic \
    --name GuardDutyFindings \
    --region $region \
    --profile $profile \
    | jq '.TopicArn' \
    | sed s/\"//g`
    echo "### New topic ARN: " $sns_arn

    # Give CW the permissions to post to the topic
    echo "### Updating SNS permissions for receiving CW events"
    aws sns set-topic-attributes \
    --topic-arn "$sns_arn" \
    --attribute-name Policy \
    --attribute-value "{\"Version\":\"2008-10-17\",\"Id\":\"__default_policy_ID\",\"Statement\":[{\"Sid\":\"__default_statement_ID\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":[\"SNS:Subscribe\",\"SNS:ListSubscriptionsByTopic\",\"SNS:DeleteTopic\",\"SNS:GetTopicAttributes\",\"SNS:Publish\",\"SNS:RemovePermission\",\"SNS:AddPermission\",\"SNS:Receive\",\"SNS:SetTopicAttributes\"],\"Resource\":\"$sns_arn\",\"Condition\":{\"StringEquals\":{\"AWS:SourceOwner\":\"$account_id\"}}},{\"Sid\":\"Allow_Publish_Events\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"events.amazonaws.com\"},\"Action\":\"sns:Publish\",\"Resource\":\"$sns_arn\"}]}" \
    --region $region \
    --profile $profile 

    # Send the CW events to the new topic
    echo "### Sending CW events to new SNS topic"
    aws events put-targets \
    --rule GuardDutyFindings \
    --targets "Id"="1","Arn"=$sns_arn \
    --region $region \
    --profile $profile

    echo "### Adding Lambda function as a subscriber to new SNS topic"
    aws sns subscribe \
    --topic-arn $sns_arn \
    --protocol lambda \
    --notification-endpoint $lambda_arn \
    --region $region \
    --profile $profile

    # # Lambda permission only needs to be set once
    echo "Adding permission to Lambda for CW events to invoke it"
    aws lambda add-permission \
    --function-name $lambda_name \
    --statement-id "$region-sns" \
    --source-arn $sns_arn \
    --action 'lambda:InvokeFunction' \
    --principal sns.amazonaws.com \
    --region $lambda_region \
    --profile $profile
    
done

