# Have to do it via CLI because CFTs don't output consistent role names
# Update trust_policy.json with the account ID where the main function will live
# Usage: ./create_role.sh <AWS Profile>

PROFILE=$1
if [[ $1 -eq 0 ]] ; then
    echo 'Usage: ./create_role.sh <AWS Profile>'
    exit 0
fi

if grep -Fxq CCOUNT_ID_WHERE_FUNCTION_IS_RUNNING trust_policy.json 
then
    echo "Please Update trust_policy.json with the account ID where the main function will live"
    exit
fi        


aws iam create-role \
--role-name Dome9CloudBots \
--assume-role-policy-document file://trust_policy.json \
--profile $PROFILE                   
                  
ARN=`aws iam create-policy \
--policy-name Dome9CloudBots \
--policy-document file://remediation_policy.json \
--query 'Policy.Arn' \
--profile $PROFILE  \
| sed s/\"//g`


aws iam attach-role-policy \
--role-name Dome9CloudBots \
--policy-arn $ARN \
--profile $PROFILE                   
              