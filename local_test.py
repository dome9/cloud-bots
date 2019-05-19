## LOCAL TESTING
from index import * 

#sample event

#to change the event type, paste in the message line from the sample event that you want to use from below. 

event = {
    'Records': [{
        'EventSource': 'aws:sns',
        'EventVersion': '1.0',
        'EventSubscriptionArn': 'arn:aws:sns:us-west-2:905007184296:eventsToSlack:0cf0e80c-1fef-4421-9cc0-b3c102ac7836',
        'Sns': {
            'Type': 'Notification',
            'MessageId': 'd59748d6-f529-532f-bf13-1a1e438fde5c',
            'TopicArn': 'arn:aws:sns:us-west-2:905007184296:eventsToSlack',
            'Subject': 'Dome9 Continuous compliance: Entity status change detected',
            'Message': '{"policy":{"name":"sns_failed_events","description":""},"bundle":{"name":"Copy of sns_send_event_failures","description":""},"reportTime":"2018-01-30T03:05:14.489Z","rule":{"name":"s3 should fail","description":"","remediation":"","complianceTags":"AUTO: sg_rules_delete","severity":"High"},"status":"Failed","account":{"id":"668504586196","vendor":"Aws"},"region":"us-west-2","entity":{"logging":{"targetBucketName":null,"targetPrefix":null,"grants":[],"enabled":false},"acl":{"grants":[{"canonicalUser":"db1b62654bda37f8a0d7ea765caa232a3950af8a64ef30f976417454e644bfa5","displayName":"alex","emailAddress":null,"premission":"FULL_CONTROL","premissionHeaderName":"x-amz-grant-full-control","type":"CanonicalUser","uri":null}],"ownerDisplayName":"alex","ownerId":"db1b62654bda37f8a0d7ea765caa232a3950af8a64ef30f976417454e644bfa5"},"policy":{"Version":"2012-10-17","Statement":[{"Sid":"AWSCloudTrailAclCheck20150319","Effect":"Allow","Principal":{"Service":"cloudtrail.amazonaws.com"},"Action":"s3:GetBucketAcl","Resource":"arn:aws:s3:::sg-663eb256"},{"Sid":"AWSCloudTrailWrite20150319","Effect":"Allow","Principal":{"Service":"cloudtrail.amazonaws.com"},"Action":"s3:PutObject","Resource":"arn:aws:s3:::sg-663eb256/AWSLogs/905007184296/*","Condition":{"StringEquals":{"s3:x-amz-acl":"bucket-owner-full-control"}}}]},"versioning":{"status":"Off","mfaDelete":false},"website":{"indexDocumentSuffix":null,"errorDocument":null,"routingRules":[],"redirectAllRequestsTo":{"hostName":"","httpRedirectCode":"","protocol":"","replaceKeyPrefixWith":"","replaceKeyWith":""}},"encryption":{"serverSideEncryptionRules":[]},"replication":{"role":"","rules":[]},"vpc":null,"id":"sg-663eb256","type":"S3Bucket","name":"sg-663eb256","dome9Id":"1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|s3Bucket|sg-663eb256-62362","accountNumber":"905007184296","region":"us-west-2","source":"db","tags":[]}}',
            'Timestamp': '2018-01-04T23:10:30.652Z',
            'SignatureVersion': '1',
            'Signature': 'fKnhCGtvNIKIKslbL54A2ZjIiGc/NPw==',
            'SigningCertUrl': 'https://sns.us-west-2.amazonaws.com/SimpleNotificationService-433026a4050d206028891664da859041.pem',
            'UnsubscribeUrl': 'https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:905007184296:eventsToSlack:0cf0e80c-1fef-4421-9cc0-b3c102ac7836',
            'MessageAttributes': {}
        }
    }]
}



#export SNS_TOPIC_ARN="arn:aws:sns:us-west-2:905007184296:eventsToSlack"
SNS_TOPIC_ARN = "arn:aws:sns:us-west-2:905007184296:eventsToSlack"

context = ""


lambda_handler(event,context)

''' 
Sample Events

#VPC
            'Message': '{"policy":{"name":"sns_failed_events","description":""},"bundle":{"name":"Copy of sns_send_event_failures","description":""},"reportTime":"2018-01-30T03:05:14.489Z","rule":{"name":"vpc should fail","description":"","remediation":"","complianceTags":"","severity":"High"},"status":"Failed","account":{"id":"905007184296","vendor":"Aws"},"region":"eu-west-2","entity":{"cidr":"172.31.0.0/16","subnets":[{"state":"available","availabilityZone":"eu-west-2b","defaultForAz":true,"mapPublicIpOnLaunch":true,"availableIpAddressCount":4091,"externalId":"subnet-02ae9148","name":"","description":"","cidr":"172.31.16.0/20","nacl":{"inbound":[{"name":"","number":100,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"INBOUND","action":"ALLOW"},{"name":"","number":32767,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"INBOUND","action":"DENY"}],"outbound":[{"name":"","number":100,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"OUTBOUND","action":"ALLOW"},{"name":"","number":32767,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"OUTBOUND","action":"DENY"}],"isDefault":true,"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"172.31.0.0/16","region":"eu_west_2","id":"vpc-66d0210f","accountNumber":"905007184296","vpnGateways":[],"internetGateways":[{"externalId":"igw-54699c3d","vpcAttachments":[{"state":"available","vpcId":"vpc-66d0210f"}],"name":""}],"dhcpOptionsId":"dopt-723ccd1b","instanceTenancy":"default","isDefault":true,"state":"available","tags":{},"name":"","source":"Db"},"id":"acl-6522d30c","type":"NACL","name":"","dome9Id":"1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|nacl|acl-6522d30c-62362","accountNumber":"905007184296","region":"eu_west_2","source":"db","tags":[]},"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"172.31.0.0/16","region":"eu_west_2","id":"vpc-66d0210f","accountNumber":"905007184296","vpnGateways":[],"internetGateways":[{"externalId":"igw-54699c3d","vpcAttachments":[{"state":"available","vpcId":"vpc-66d0210f"}],"name":""}],"dhcpOptionsId":"dopt-723ccd1b","instanceTenancy":"default","isDefault":true,"state":"available","tags":{},"name":"","source":"Db"},"id":"subnet-02ae9148","type":"Subnet","dome9Id":"1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|subnet|subnet-02ae9148-62362","accountNumber":"905007184296","region":"eu_west_2","source":"db","tags":[]},{"state":"available","availabilityZone":"eu-west-2a","defaultForAz":true,"mapPublicIpOnLaunch":true,"availableIpAddressCount":4091,"externalId":"subnet-50eaf028","name":"","description":"","cidr":"172.31.0.0/20","nacl":{"inbound":[{"name":"","number":100,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"INBOUND","action":"ALLOW"},{"name":"","number":32767,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"INBOUND","action":"DENY"}],"outbound":[{"name":"","number":100,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"OUTBOUND","action":"ALLOW"},{"name":"","number":32767,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"OUTBOUND","action":"DENY"}],"isDefault":true,"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"172.31.0.0/16","region":"eu_west_2","id":"vpc-66d0210f","accountNumber":"905007184296","vpnGateways":[],"internetGateways":[{"externalId":"igw-54699c3d","vpcAttachments":[{"state":"available","vpcId":"vpc-66d0210f"}],"name":""}],"dhcpOptionsId":"dopt-723ccd1b","instanceTenancy":"default","isDefault":true,"state":"available","tags":{},"name":"","source":"Db"},"id":"acl-6522d30c","type":"NACL","name":"","dome9Id":"1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|nacl|acl-6522d30c-62362","accountNumber":"905007184296","region":"eu_west_2","source":"db","tags":[]},"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"172.31.0.0/16","region":"eu_west_2","id":"vpc-66d0210f","accountNumber":"905007184296","vpnGateways":[],"internetGateways":[{"externalId":"igw-54699c3d","vpcAttachments":[{"state":"available","vpcId":"vpc-66d0210f"}],"name":""}],"dhcpOptionsId":"dopt-723ccd1b","instanceTenancy":"default","isDefault":true,"state":"available","tags":{},"name":"","source":"Db"},"id":"subnet-50eaf028","type":"Subnet","dome9Id":"1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|subnet|subnet-50eaf028-62362","accountNumber":"905007184296","region":"eu_west_2","source":"db","tags":[]},{"state":"available","availabilityZone":"eu-west-2c","defaultForAz":true,"mapPublicIpOnLaunch":true,"availableIpAddressCount":4091,"externalId":"subnet-1f12e976","name":"","description":"","cidr":"172.31.32.0/20","nacl":{"inbound":[{"name":"","number":100,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"INBOUND","action":"ALLOW"},{"name":"","number":32767,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"INBOUND","action":"DENY"}],"outbound":[{"name":"","number":100,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"OUTBOUND","action":"ALLOW"},{"name":"","number":32767,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"OUTBOUND","action":"DENY"}],"isDefault":true,"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"172.31.0.0/16","region":"eu_west_2","id":"vpc-66d0210f","accountNumber":"905007184296","vpnGateways":[],"internetGateways":[{"externalId":"igw-54699c3d","vpcAttachments":[{"state":"available","vpcId":"vpc-66d0210f"}],"name":""}],"dhcpOptionsId":"dopt-723ccd1b","instanceTenancy":"default","isDefault":true,"state":"available","tags":{},"name":"","source":"Db"},"id":"acl-6522d30c","type":"NACL","name":"","dome9Id":"1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|nacl|acl-6522d30c-62362","accountNumber":"905007184296","region":"eu_west_2","source":"db","tags":[]},"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"172.31.0.0/16","region":"eu_west_2","id":"vpc-66d0210f","accountNumber":"905007184296","vpnGateways":[],"internetGateways":[{"externalId":"igw-54699c3d","vpcAttachments":[{"state":"available","vpcId":"vpc-66d0210f"}],"name":""}],"dhcpOptionsId":"dopt-723ccd1b","instanceTenancy":"default","isDefault":true,"state":"available","tags":{},"name":"","source":"Db"},"id":"subnet-1f12e976","type":"Subnet","dome9Id":"1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|subnet|subnet-1f12e976-62362","accountNumber":"905007184296","region":"eu_west_2","source":"db","tags":[]}],"dhcpOptionsId":"dopt-723ccd1b","instanceTenancy":"default","isDefault":true,"state":"available","vpnGateways":[],"internetGateways":[{"externalId":"igw-54699c3d","vpcAttachments":[{"state":"available","vpcId":"vpc-66d0210f"}],"name":""}],"routeTables":[{"associations":[{"isMain":true,"subnetId":null}],"propagatingVgws":[],"routes":[{"destinationCidrBlock":"172.31.0.0/16","destinationIpv6CidrBlock":null,"destinationPrefixListId":null,"egressOnlyInternetGatewayId":null,"gatewayId":"local","instanceId":null,"instanceOwnerId":null,"natGatewayId":null,"networkInterfaceId":null,"origin":"CreateRouteTable","state":"active","vpcPeeringConnectionId":null},{"destinationCidrBlock":"0.0.0.0/0","destinationIpv6CidrBlock":null,"destinationPrefixListId":null,"egressOnlyInternetGatewayId":null,"gatewayId":"igw-54699c3d","instanceId":null,"instanceOwnerId":null,"natGatewayId":null,"networkInterfaceId":null,"origin":"CreateRoute","state":"active","vpcPeeringConnectionId":null}],"routeTableId":"rtb-0319e86a","vpcId":"vpc-66d0210f","tags":{},"name":"","tagsEntities":{}}],"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"172.31.0.0/16","region":"eu_west_2","id":"vpc-66d0210f","accountNumber":"905007184296","vpnGateways":[],"internetGateways":[{"externalId":"igw-54699c3d","vpcAttachments":[{"state":"available","vpcId":"vpc-66d0210f"}],"name":""}],"dhcpOptionsId":"dopt-723ccd1b","instanceTenancy":"default","isDefault":true,"state":"available","tags":{},"name":"","source":"Db"},"id":"vpc-66d0210f","type":"VPC","name":"","dome9Id":"vpc-66d0210f","accountNumber":"905007184296","region":"eu-west-2","source":"db","tags":[]}}',

#S3 BUCKET
            'Message': '{"policy":{"name":"sns_failed_events","description":""},"bundle":{"name":"Copy of sns_send_event_failures","description":""},"reportTime":"2018-01-30T03:05:14.489Z","rule":{"name":"s3 should fail","description":"","remediation":"","complianceTags":"","severity":"High"},"status":"Failed","account":{"id":"905007184296","vendor":"Aws"},"region":"","entity":{"logging":{"targetBucketName":null,"targetPrefix":null,"grants":[],"enabled":false},"acl":{"grants":[{"canonicalUser":"db1b62654bda37f8a0d7ea765caa232a3950af8a64ef30f976417454e644bfa5","displayName":"alex","emailAddress":null,"premission":"FULL_CONTROL","premissionHeaderName":"x-amz-grant-full-control","type":"CanonicalUser","uri":null}],"ownerDisplayName":"alex","ownerId":"db1b62654bda37f8a0d7ea765caa232a3950af8a64ef30f976417454e644bfa5"},"policy":{"Version":"2012-10-17","Statement":[{"Sid":"AWSCloudTrailAclCheck20150319","Effect":"Allow","Principal":{"Service":"cloudtrail.amazonaws.com"},"Action":"s3:GetBucketAcl","Resource":"arn:aws:s3:::sg-663eb256"},{"Sid":"AWSCloudTrailWrite20150319","Effect":"Allow","Principal":{"Service":"cloudtrail.amazonaws.com"},"Action":"s3:PutObject","Resource":"arn:aws:s3:::sg-663eb256/AWSLogs/905007184296/*","Condition":{"StringEquals":{"s3:x-amz-acl":"bucket-owner-full-control"}}}]},"versioning":{"status":"Off","mfaDelete":false},"website":{"indexDocumentSuffix":null,"errorDocument":null,"routingRules":[],"redirectAllRequestsTo":{"hostName":"","httpRedirectCode":"","protocol":"","replaceKeyPrefixWith":"","replaceKeyWith":""}},"encryption":{"serverSideEncryptionRules":[]},"replication":{"role":"","rules":[]},"vpc":null,"id":"sg-663eb256","type":"S3Bucket","name":"sg-663eb256","dome9Id":"1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|s3Bucket|sg-663eb256-62362","accountNumber":"905007184296","region":"","source":"db","tags":[]}}',

#IAM USER
            'Message': '{"policy":{"name":"sns_failed_events","description":""},"bundle":{"name":"Copy of sns_send_event_failures","description":""},"reportTime":"2018-01-30T03:05:14.489Z","rule":{"name":"iamuser should fail","description":"","remediation":"","complianceTags":"","severity":"High"},"status":"Failed","account":{"id":"905007184296","vendor":"Aws"},"entity":{"createDate":1483998628,"passwordLastUsed":1517239732,"arn":"arn:aws:iam::905007184296:testuser2","path":null,"managedPolicies":null,"inlinePolicies":null,"attachedGroups":null,"passwordEnabled":false,"passwordLastChanged":-62135596800,"passwordNextRotation":-62135596800,"mfaActive":false,"firstAccessKey":{"isActive":true,"lastRotated":1505498566,"lastUsedDate":-62135596800,"lastUsedRegion":"","lastUsedService":""},"secondAccessKey":{"isActive":true,"lastRotated":1505498570,"lastUsedDate":-62135596800,"lastUsedRegion":"","lastUsedService":""},"firstCertificate":{"isActive":false,"lastRotated":-62135596800},"secondCertificate":{"isActive":false,"lastRotated":-62135596800},"combinedPolicies":null,"vpc":null,"id":"","type":"IamUser","name":"testuser2","dome9Id":"","accountNumber":"905007184296","region":null,"source":"db","tags":[]}}',

#IAM ROLE
            'Message': '{"policy":{"name":"sns_failed_events","description":""},"bundle":{"name":"Copy of sns_send_event_failures","description":""},"reportTime":"2018-01-30T03:05:14.489Z","rule":{"name":"iamrole should fail","description":"","remediation":"","complianceTags":"AUTO: iam_quarantine_role","severity":"High"},"status":"Failed","account":{"id":"905007184296","vendor":"Aws"},"entity":{"arn":"arn:aws:iam::905007184296:role/readonlypermissionsdome9-Role-HZQA3GMOJELS","assumeRolePolicy":{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":"arn:aws:iam::634729597623:root"},"Action":"sts:AssumeRole","Condition":{"StringEquals":{"sts:ExternalId":"abc123"}}}]},"path":"/","managedPolicies":[{"arn":"arn:aws:iam::aws:policy/SecurityAudit","name":"SecurityAudit"},{"arn":"arn:aws:iam::aws:policy/AmazonInspectorReadOnlyAccess","name":"AmazonInspectorReadOnlyAccess"}],"inlinePolicies":[{"name":"Dome9Readonly","document":{"Version":"2012-10-17","Statement":[{"Action":["logs:Describe*","logs:Get*","logs:FilterLogEvents","cloudtrail:LookupEvents","lambda:List*","s3:GetEncryptionConfiguration","s3:List*","elasticfilesystem:Describe*","sns:ListSubscriptions","sns:ListSubscriptionsByTopic"],"Resource":"*","Effect":"Allow","Sid":"Dome9ReadOnly"}]}}],"combinedPolicies":[{"name":"readonlypermissionsdome9-Role-HZQA3GMOJELS","id":"arn:aws:iam::905007184296:role/readonlypermissionsdome9-Role-HZQA3GMOJELS","relationType":"AssumeRole","policyDocument":{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":"arn:aws:iam::634729597623:root"},"Action":"sts:AssumeRole","Condition":{"StringEquals":{"sts:ExternalId":"abc123"}}}]}},{"name":"Dome9Readonly","id":null,"relationType":"Inline","policyDocument":{"Version":"2012-10-17","Statement":[{"Action":["logs:Describe*","logs:Get*","logs:FilterLogEvents","cloudtrail:LookupEvents","lambda:List*","s3:GetEncryptionConfiguration","s3:List*","elasticfilesystem:Describe*","sns:ListSubscriptions","sns:ListSubscriptionsByTopic"],"Resource":"*","Effect":"Allow","Sid":"Dome9ReadOnly"}]}},{"name":null,"id":"arn:aws:iam::aws:policy/SecurityAudit","relationType":"DirectlyAttached","policyDocument":{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Resource":"*","Action":["acm:DescribeCertificate","acm:ListCertificates","autoscaling:Describe*","batch:DescribeComputeEnvironments","batch:DescribeJobDefinitions","clouddirectory:ListDirectories","cloudformation:DescribeStack*","cloudformation:GetTemplate","cloudformation:ListStack*","cloudformation:GetStackPolicy","cloudfront:Get*","cloudfront:List*","cloudhsm:ListHapgs","cloudhsm:ListHsms","cloudhsm:ListLunaClients","cloudsearch:DescribeDomains","cloudsearch:DescribeServiceAccessPolicies","cloudtrail:DescribeTrails","cloudtrail:GetTrailStatus","cloudtrail:ListTags","cloudwatch:Describe*","codebuild:ListProjects","codecommit:BatchGetRepositories","codecommit:GetBranch","codecommit:GetObjectIdentifier","codecommit:GetRepository","codecommit:List*","codedeploy:Batch*","codedeploy:Get*","codedeploy:List*","codepipeline:ListPipelines","cognito-identity:ListIdentityPools","cognito-idp:ListUserPools","config:Deliver*","config:Describe*","config:Get*","datapipeline:DescribeObjects","datapipeline:DescribePipelines","datapipeline:EvaluateExpression","datapipeline:GetPipelineDefinition","datapipeline:ListPipelines","datapipeline:QueryObjects","datapipeline:ValidatePipelineDefinition","directconnect:Describe*","ds:DescribeDirectories","dynamodb:ListStreams","dynamodb:ListTables","ec2:Describe*","ecr:DescribeRepositories","ecr:GetRepositoryPolicy","ecs:Describe*","ecs:List*","elasticache:Describe*","elasticbeanstalk:Describe*","elasticfilesystem:DescribeFileSystems","elasticloadbalancing:Describe*","elasticmapreduce:DescribeJobFlows","elasticmapreduce:ListClusters","elasticmapreduce:ListInstances","es:Describe*","es:ListDomainNames","events:DescribeEventBus","events:ListRules","firehose:Describe*","firehose:List*","gamelift:ListBuilds","gamelift:ListFleets","glacier:DescribeVault","glacier:GetVaultAccessPolicy","glacier:ListVaults","iam:GenerateCredentialReport","iam:Get*","iam:List*","iot:ListThings","kinesis:ListStreams","kinesisanalytics:ListApplications","kms:Describe*","kms:Get*","kms:List*","lambda:GetPolicy","lambda:ListFunctions","logs:DescribeResourcePolicies","logs:DescribeLogGroups","logs:DescribeMetricFilters","machinelearning:DescribeMLModels","mediastore:GetContainerPolicy","mediastore:ListContainers","opsworks-cm:DescribeServers","rds:Describe*","rds:DownloadDBLogFilePortion","rds:ListTagsForResource","redshift:Describe*","route53:Get*","route53:List*","route53domains:GetDomainDetail","route53domains:GetOperationDetail","route53domains:ListDomains","route53domains:ListOperations","route53domains:ListTagsForDomain","s3:GetAccelerateConfiguration","s3:GetAnalyticsConfiguration","s3:GetBucket*","s3:GetEncryptionConfiguration","s3:GetInventoryConfiguration","s3:GetLifecycleConfiguration","s3:GetMetricsConfiguration","s3:GetObjectAcl","s3:GetObjectVersionAcl","s3:GetReplicationConfiguration","s3:ListAllMyBuckets","sdb:DomainMetadata","sdb:ListDomains","serverlessrepo:GetApplicationPolicy","serverlessrepo:ListApplications","ses:GetIdentityDkimAttributes","ses:GetIdentityVerificationAttributes","ses:ListIdentities","snowball:ListClusters","snowball:ListJobs","sns:GetTopicAttributes","sns:ListSubscriptionsByTopic","sns:ListTopics","sqs:GetQueueAttributes","sqs:ListQueues","ssm:DescribeDocumentPermission","ssm:ListDocuments","states:ListStateMachines","storagegateway:DescribeBandwidthRateLimit","storagegateway:DescribeCache","storagegateway:DescribeCachediSCSIVolumes","storagegateway:DescribeGatewayInformation","storagegateway:DescribeMaintenanceStartTime","storagegateway:DescribeNFSFileShares","storagegateway:DescribeSnapshotSchedule","storagegateway:DescribeStorediSCSIVolumes","storagegateway:DescribeTapeArchives","storagegateway:DescribeTapeRecoveryPoints","storagegateway:DescribeTapes","storagegateway:DescribeUploadBuffer","storagegateway:DescribeVTLDevices","storagegateway:DescribeWorkingStorage","storagegateway:List*","tag:GetResources","tag:GetTagKeys","trustedadvisor:Describe*","waf:ListWebACLs","waf-regional:ListWebACLs"]}]}},{"name":null,"id":"arn:aws:iam::aws:policy/AmazonInspectorReadOnlyAccess","relationType":"DirectlyAttached","policyDocument":{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["inspector:Describe*","inspector:Get*","inspector:List*","inspector:LocalizeText","inspector:Preview*","ec2:DescribeInstances","ec2:DescribeTags","sns:ListTopics","events:DescribeRule","events:ListRuleNamesByTarget"],"Resource":"*"}]}}],"vpc":null,"id":"AROAIC3FAVDTFA5ARHK5I","type":"IamRole","name":"readonlypermissionsdome9-Role-HZQA3GMOJELS","dome9Id":"1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|iam|AROAIC3FAVDTFA5ARHK5I-62362","accountNumber":"905007184296","region":null,"source":"db","tags":[]}}',

#INSTANCE
            'Message': '{"policy":{"name":"sns_failed_events","description":""},"bundle":{"name":"Copy of sns_send_event_failures","description":""},"reportTime":"2018-01-30T03:05:14.489Z","rule":{"name":"this rule should fail","description":"","remediation":"","complianceTags":"pci 2.3|AUTO: delete_sg","severity":"High"},"status":"Failed","account":{"id":"905007184296","vendor":"Aws"},"region":"Oregon","entity":{"image":"ami-bf4193c7","kernelId":null,"platform":"linux","launchTime":1514572312,"inboundRules":[],"outboundRules":[],"nics":[{"id":"eni-1c24c23e","name":"eth0","subnet":{"state":"available","availabilityZone":"us-west-2b","defaultForAz":true,"mapPublicIpOnLaunch":true,"availableIpAddressCount":4086,"externalId":"subnet-ee5d8b89","name":"","description":"","cidr":"172.31.16.0/20","nacl":{"inbound":[{"name":"","number":100,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"INBOUND","action":"ALLOW"},{"name":"","number":32766,"protocol":"ALL","source":"172.31.48.0/28","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"INBOUND","action":"ALLOW"},{"name":"","number":32767,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"INBOUND","action":"DENY"}],"outbound":[{"name":"","number":100,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"OUTBOUND","action":"ALLOW"},{"name":"","number":32767,"protocol":"ALL","source":"0.0.0.0/0","destination":"0.0.0.0/0","destinationPort":0,"destinationPortTo":65535,"direction":"OUTBOUND","action":"DENY"}],"isDefault":true,"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"172.31.0.0/16","region":"us_west_2","id":"vpc-3543f352","accountNumber":"905007184296","vpnGateways":[],"internetGateways":[{"externalId":"igw-3c6b2a58","vpcAttachments":[{"state":"available","vpcId":"vpc-3543f352"}],"name":""}],"dhcpOptionsId":"dopt-b18786d5","instanceTenancy":"default","isDefault":true,"state":"available","tags":{},"name":"","source":"Db"},"id":"acl-f0395e97","type":"NACL","name":"","dome9Id":"1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|5|nacl|acl-f0395e97-62362","accountNumber":"905007184296","region":"us_west_2","source":"db","tags":[{"key":"AlertLogic-EnvironmentID","value":"E49BD84B-9720-455D-B7CF-4B3500443FD3"},{"key":"AlertLogic-AccountID","value":"134224348"},{"key":"AlertLogic","value":"Security"}]},"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"172.31.0.0/16","region":"us_west_2","id":"vpc-3543f352","accountNumber":"905007184296","vpnGateways":[],"internetGateways":[{"externalId":"igw-3c6b2a58","vpcAttachments":[{"state":"available","vpcId":"vpc-3543f352"}],"name":""}],"dhcpOptionsId":"dopt-b18786d5","instanceTenancy":"default","isDefault":true,"state":"available","tags":{},"name":"","source":"Db"},"id":"subnet-ee5d8b89","type":"Subnet","dome9Id":"1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|5|subnet|subnet-ee5d8b89-62362","accountNumber":"905007184296","region":"us_west_2","source":"db","tags":[]},"privateDnsName":"ip-172-31-30-90.us-west-2.compute.internal","publicIpAddress":"","privateIpAddress":"172.31.30.90","securityGroups":[{"description":"launch-wizard-5 created 2017-12-29T09:14:16.382-08:00","inboundRules":[],"outboundRules":[],"networkAssetsStats":[],"isProtected":false,"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"172.31.0.0/16","region":"us_west_2","id":"vpc-3543f352","accountNumber":"905007184296","vpnGateways":[],"internetGateways":[{"externalId":"igw-3c6b2a58","vpcAttachments":[{"state":"available","vpcId":"vpc-3543f352"}],"name":""}],"dhcpOptionsId":"dopt-b18786d5","instanceTenancy":"default","isDefault":true,"state":"available","tags":{},"name":"","source":"Db"},"id":"sg-7badea07","type":"SecurityGroup","name":"launch-wizard-5","dome9Id":"2384935","accountNumber":"905007184296","region":"us_west_2","source":"db","tags":[]}]}],"isPublic":false,"instanceType":"t2.nano","isRunning":false,"volumes":[{"attachments":[{"attachTime":1514567667,"deleteOnTermination":true,"device":"/dev/xvda","instanceId":"i-0579293b8a3aeafb9","state":"attached","volumeId":"vol-02b194a15d9c58429"}],"availabilityZone":"us-west-2b","createTime":1514567667,"encrypted":false,"iops":100,"kmsKeyId":null,"size":8,"snapshotId":"snap-016f4ef92d26f9538","state":"in-use","tags":[],"volumeId":"vol-02b194a15d9c58429","volumeType":"gp2"}],"profileArn":null,"roles":[],"scanners":{"scans":null,"findings":null},"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"172.31.0.0/16","region":"us_west_2","id":"vpc-3543f352","accountNumber":"905007184296","vpnGateways":[],"internetGateways":[{"externalId":"igw-3c6b2a58","vpcAttachments":[{"state":"available","vpcId":"vpc-3543f352"}],"name":""}],"dhcpOptionsId":"dopt-b18786d5","instanceTenancy":"default","isDefault":true,"state":"available","tags":{},"name":"","source":"Db"},"id":"i-0579293b8a3aeafb9","type":"Instance","name":"test2222","dome9Id":"","accountNumber":"905007184296","region":"us_west_2","source":"db","tags":[{"key":"owner","value":"Who owns this box"},{"key":"thisimykey","value":"thisismyvalue"},{"key":"(thisi","value":"mykey:thisismyvalue)"}]}}',


#VPC pretty:
{
    "policy": {
        "name": "sns_failed_events",
        "description": ""
    },
    "bundle": {
        "name": "Copy of sns_send_event_failures",
        "description": ""
    },
    "reportTime": "2018-01-30T03:05:14.489Z",
    "rule": {
        "name": "vpc should fail",
        "description": "",
        "remediation": "",
        "complianceTags": "",
        "severity": "High"
    },
    "status": "Failed",
    "account": {
        "id": "905007184296",
        "vendor": "Aws"
    },
    "region": "eu-west-2",
    "entity": {
        "cidr": "172.31.0.0/16",
        "subnets": [{
            "state": "available",
            "availabilityZone": "eu-west-2b",
            "defaultForAz": true,
            "mapPublicIpOnLaunch": true,
            "availableIpAddressCount": 4091,
            "externalId": "subnet-02ae9148",
            "name": "",
            "description": "",
            "cidr": "172.31.16.0/20",
            "nacl": {
                "inbound": [{
                    "name": "",
                    "number": 100,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "INBOUND",
                    "action": "ALLOW"
                }, {
                    "name": "",
                    "number": 32767,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "INBOUND",
                    "action": "DENY"
                }],
                "outbound": [{
                    "name": "",
                    "number": 100,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "OUTBOUND",
                    "action": "ALLOW"
                }, {
                    "name": "",
                    "number": 32767,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "OUTBOUND",
                    "action": "DENY"
                }],
                "isDefault": true,
                "vpc": {
                    "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
                    "cidr": "172.31.0.0/16",
                    "region": "eu_west_2",
                    "id": "vpc-66d0210f",
                    "accountNumber": "905007184296",
                    "vpnGateways": [],
                    "internetGateways": [{
                        "externalId": "igw-54699c3d",
                        "vpcAttachments": [{
                            "state": "available",
                            "vpcId": "vpc-66d0210f"
                        }],
                        "name": ""
                    }],
                    "dhcpOptionsId": "dopt-723ccd1b",
                    "instanceTenancy": "default",
                    "isDefault": true,
                    "state": "available",
                    "tags": {},
                    "name": "",
                    "source": "Db"
                },
                "id": "acl-6522d30c",
                "type": "NACL",
                "name": "",
                "dome9Id": "1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|nacl|acl-6522d30c-62362",
                "accountNumber": "905007184296",
                "region": "eu_west_2",
                "source": "db",
                "tags": []
            },
            "vpc": {
                "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
                "cidr": "172.31.0.0/16",
                "region": "eu_west_2",
                "id": "vpc-66d0210f",
                "accountNumber": "905007184296",
                "vpnGateways": [],
                "internetGateways": [{
                    "externalId": "igw-54699c3d",
                    "vpcAttachments": [{
                        "state": "available",
                        "vpcId": "vpc-66d0210f"
                    }],
                    "name": ""
                }],
                "dhcpOptionsId": "dopt-723ccd1b",
                "instanceTenancy": "default",
                "isDefault": true,
                "state": "available",
                "tags": {},
                "name": "",
                "source": "Db"
            },
            "id": "subnet-02ae9148",
            "type": "Subnet",
            "dome9Id": "1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|subnet|subnet-02ae9148-62362",
            "accountNumber": "905007184296",
            "region": "eu_west_2",
            "source": "db",
            "tags": []
        }, {
            "state": "available",
            "availabilityZone": "eu-west-2a",
            "defaultForAz": true,
            "mapPublicIpOnLaunch": true,
            "availableIpAddressCount": 4091,
            "externalId": "subnet-50eaf028",
            "name": "",
            "description": "",
            "cidr": "172.31.0.0/20",
            "nacl": {
                "inbound": [{
                    "name": "",
                    "number": 100,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "INBOUND",
                    "action": "ALLOW"
                }, {
                    "name": "",
                    "number": 32767,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "INBOUND",
                    "action": "DENY"
                }],
                "outbound": [{
                    "name": "",
                    "number": 100,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "OUTBOUND",
                    "action": "ALLOW"
                }, {
                    "name": "",
                    "number": 32767,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "OUTBOUND",
                    "action": "DENY"
                }],
                "isDefault": true,
                "vpc": {
                    "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
                    "cidr": "172.31.0.0/16",
                    "region": "eu_west_2",
                    "id": "vpc-66d0210f",
                    "accountNumber": "905007184296",
                    "vpnGateways": [],
                    "internetGateways": [{
                        "externalId": "igw-54699c3d",
                        "vpcAttachments": [{
                            "state": "available",
                            "vpcId": "vpc-66d0210f"
                        }],
                        "name": ""
                    }],
                    "dhcpOptionsId": "dopt-723ccd1b",
                    "instanceTenancy": "default",
                    "isDefault": true,
                    "state": "available",
                    "tags": {},
                    "name": "",
                    "source": "Db"
                },
                "id": "acl-6522d30c",
                "type": "NACL",
                "name": "",
                "dome9Id": "1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|nacl|acl-6522d30c-62362",
                "accountNumber": "905007184296",
                "region": "eu_west_2",
                "source": "db",
                "tags": []
            },
            "vpc": {
                "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
                "cidr": "172.31.0.0/16",
                "region": "eu_west_2",
                "id": "vpc-66d0210f",
                "accountNumber": "905007184296",
                "vpnGateways": [],
                "internetGateways": [{
                    "externalId": "igw-54699c3d",
                    "vpcAttachments": [{
                        "state": "available",
                        "vpcId": "vpc-66d0210f"
                    }],
                    "name": ""
                }],
                "dhcpOptionsId": "dopt-723ccd1b",
                "instanceTenancy": "default",
                "isDefault": true,
                "state": "available",
                "tags": {},
                "name": "",
                "source": "Db"
            },
            "id": "subnet-50eaf028",
            "type": "Subnet",
            "dome9Id": "1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|subnet|subnet-50eaf028-62362",
            "accountNumber": "905007184296",
            "region": "eu_west_2",
            "source": "db",
            "tags": []
        }, {
            "state": "available",
            "availabilityZone": "eu-west-2c",
            "defaultForAz": true,
            "mapPublicIpOnLaunch": true,
            "availableIpAddressCount": 4091,
            "externalId": "subnet-1f12e976",
            "name": "",
            "description": "",
            "cidr": "172.31.32.0/20",
            "nacl": {
                "inbound": [{
                    "name": "",
                    "number": 100,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "INBOUND",
                    "action": "ALLOW"
                }, {
                    "name": "",
                    "number": 32767,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "INBOUND",
                    "action": "DENY"
                }],
                "outbound": [{
                    "name": "",
                    "number": 100,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "OUTBOUND",
                    "action": "ALLOW"
                }, {
                    "name": "",
                    "number": 32767,
                    "protocol": "ALL",
                    "source": "0.0.0.0/0",
                    "destination": "0.0.0.0/0",
                    "destinationPort": 0,
                    "destinationPortTo": 65535,
                    "direction": "OUTBOUND",
                    "action": "DENY"
                }],
                "isDefault": true,
                "vpc": {
                    "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
                    "cidr": "172.31.0.0/16",
                    "region": "eu_west_2",
                    "id": "vpc-66d0210f",
                    "accountNumber": "905007184296",
                    "vpnGateways": [],
                    "internetGateways": [{
                        "externalId": "igw-54699c3d",
                        "vpcAttachments": [{
                            "state": "available",
                            "vpcId": "vpc-66d0210f"
                        }],
                        "name": ""
                    }],
                    "dhcpOptionsId": "dopt-723ccd1b",
                    "instanceTenancy": "default",
                    "isDefault": true,
                    "state": "available",
                    "tags": {},
                    "name": "",
                    "source": "Db"
                },
                "id": "acl-6522d30c",
                "type": "NACL",
                "name": "",
                "dome9Id": "1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|nacl|acl-6522d30c-62362",
                "accountNumber": "905007184296",
                "region": "eu_west_2",
                "source": "db",
                "tags": []
            },
            "vpc": {
                "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
                "cidr": "172.31.0.0/16",
                "region": "eu_west_2",
                "id": "vpc-66d0210f",
                "accountNumber": "905007184296",
                "vpnGateways": [],
                "internetGateways": [{
                    "externalId": "igw-54699c3d",
                    "vpcAttachments": [{
                        "state": "available",
                        "vpcId": "vpc-66d0210f"
                    }],
                    "name": ""
                }],
                "dhcpOptionsId": "dopt-723ccd1b",
                "instanceTenancy": "default",
                "isDefault": true,
                "state": "available",
                "tags": {},
                "name": "",
                "source": "Db"
            },
            "id": "subnet-1f12e976",
            "type": "Subnet",
            "dome9Id": "1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|18|subnet|subnet-1f12e976-62362",
            "accountNumber": "905007184296",
            "region": "eu_west_2",
            "source": "db",
            "tags": []
        }],
        "dhcpOptionsId": "dopt-723ccd1b",
        "instanceTenancy": "default",
        "isDefault": true,
        "state": "available",
        "vpnGateways": [],
        "internetGateways": [{
            "externalId": "igw-54699c3d",
            "vpcAttachments": [{
                "state": "available",
                "vpcId": "vpc-66d0210f"
            }],
            "name": ""
        }],
        "routeTables": [{
            "associations": [{
                "isMain": true,
                "subnetId": null
            }],
            "propagatingVgws": [],
            "routes": [{
                "destinationCidrBlock": "172.31.0.0/16",
                "destinationIpv6CidrBlock": null,
                "destinationPrefixListId": null,
                "egressOnlyInternetGatewayId": null,
                "gatewayId": "local",
                "instanceId": null,
                "instanceOwnerId": null,
                "natGatewayId": null,
                "networkInterfaceId": null,
                "origin": "CreateRouteTable",
                "state": "active",
                "vpcPeeringConnectionId": null
            }, {
                "destinationCidrBlock": "0.0.0.0/0",
                "destinationIpv6CidrBlock": null,
                "destinationPrefixListId": null,
                "egressOnlyInternetGatewayId": null,
                "gatewayId": "igw-54699c3d",
                "instanceId": null,
                "instanceOwnerId": null,
                "natGatewayId": null,
                "networkInterfaceId": null,
                "origin": "CreateRoute",
                "state": "active",
                "vpcPeeringConnectionId": null
            }],
            "routeTableId": "rtb-0319e86a",
            "vpcId": "vpc-66d0210f",
            "tags": {},
            "name": "",
            "tagsEntities": {}
        }],
        "vpc": {
            "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
            "cidr": "172.31.0.0/16",
            "region": "eu_west_2",
            "id": "vpc-66d0210f",
            "accountNumber": "905007184296",
            "vpnGateways": [],
            "internetGateways": [{
                "externalId": "igw-54699c3d",
                "vpcAttachments": [{
                    "state": "available",
                    "vpcId": "vpc-66d0210f"
                }],
                "name": ""
            }],
            "dhcpOptionsId": "dopt-723ccd1b",
            "instanceTenancy": "default",
            "isDefault": true,
            "state": "available",
            "tags": {},
            "name": "",
            "source": "Db"
        },
        "id": "vpc-66d0210f",
        "type": "VPC",
        "name": "",
        "dome9Id": "vpc-66d0210f",
        "accountNumber": "905007184296",
        "region": "eu-west-2",
        "source": "db",
        "tags": []
    }
}



#IAM ROLE EXAMPLE:
{
    "policy": {
        "name": "sns_failed_events",
        "description": ""
    },
    "bundle": {
        "name": "Copy of sns_send_event_failures",
        "description": ""
    },
    "reportTime": "2018-01-30T03:05:14.489Z",
    "rule": {
        "name": "iamrole should fail",
        "description": "",
        "remediation": "",
        "complianceTags": "",
        "severity": "High"
    },
    "status": "Failed",
    "account": {
        "id": "905007184296",
        "vendor": "Aws"
    },
    "entity": {
        "arn": "arn:aws:iam::905007184296:role/readonlypermissionsdome9-Role-HZQA3GMOJELS",
        "assumeRolePolicy": {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::634729597623:root"
                },
                "Action": "sts:AssumeRole",
                "Condition": {
                    "StringEquals": {
                        "sts:ExternalId": "abc123"
                    }
                }
            }]
        },
        "path": "/",
        "managedPolicies": [{
            "arn": "arn:aws:iam::aws:policy/SecurityAudit",
            "name": "SecurityAudit"
        }, {
            "arn": "arn:aws:iam::aws:policy/AmazonInspectorReadOnlyAccess",
            "name": "AmazonInspectorReadOnlyAccess"
        }],
        "inlinePolicies": [{
            "name": "Dome9Readonly",
            "document": {
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": ["logs:Describe*", "logs:Get*", "logs:FilterLogEvents", "cloudtrail:LookupEvents", "lambda:List*", "s3:GetEncryptionConfiguration", "s3:List*", "elasticfilesystem:Describe*", "sns:ListSubscriptions", "sns:ListSubscriptionsByTopic"],
                    "Resource": "*",
                    "Effect": "Allow",
                    "Sid": "Dome9ReadOnly"
                }]
            }
        }],
        "combinedPolicies": [{
            "name": "readonlypermissionsdome9-Role-HZQA3GMOJELS",
            "id": "arn:aws:iam::905007184296:role/readonlypermissionsdome9-Role-HZQA3GMOJELS",
            "relationType": "AssumeRole",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "arn:aws:iam::634729597623:root"
                    },
                    "Action": "sts:AssumeRole",
                    "Condition": {
                        "StringEquals": {
                            "sts:ExternalId": "abc123"
                        }
                    }
                }]
            }
        }, {
            "name": "Dome9Readonly",
            "id": null,
            "relationType": "Inline",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": ["logs:Describe*", "logs:Get*", "logs:FilterLogEvents", "cloudtrail:LookupEvents", "lambda:List*", "s3:GetEncryptionConfiguration", "s3:List*", "elasticfilesystem:Describe*", "sns:ListSubscriptions", "sns:ListSubscriptionsByTopic"],
                    "Resource": "*",
                    "Effect": "Allow",
                    "Sid": "Dome9ReadOnly"
                }]
            }
        }, {
            "name": null,
            "id": "arn:aws:iam::aws:policy/SecurityAudit",
            "relationType": "DirectlyAttached",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Resource": "*",
                    "Action": ["acm:DescribeCertificate", "acm:ListCertificates", "autoscaling:Describe*", "batch:DescribeComputeEnvironments", "batch:DescribeJobDefinitions", "clouddirectory:ListDirectories", "cloudformation:DescribeStack*", "cloudformation:GetTemplate", "cloudformation:ListStack*", "cloudformation:GetStackPolicy", "cloudfront:Get*", "cloudfront:List*", "cloudhsm:ListHapgs", "cloudhsm:ListHsms", "cloudhsm:ListLunaClients", "cloudsearch:DescribeDomains", "cloudsearch:DescribeServiceAccessPolicies", "cloudtrail:DescribeTrails", "cloudtrail:GetTrailStatus", "cloudtrail:ListTags", "cloudwatch:Describe*", "codebuild:ListProjects", "codecommit:BatchGetRepositories", "codecommit:GetBranch", "codecommit:GetObjectIdentifier", "codecommit:GetRepository", "codecommit:List*", "codedeploy:Batch*", "codedeploy:Get*", "codedeploy:List*", "codepipeline:ListPipelines", "cognito-identity:ListIdentityPools", "cognito-idp:ListUserPools", "config:Deliver*", "config:Describe*", "config:Get*", "datapipeline:DescribeObjects", "datapipeline:DescribePipelines", "datapipeline:EvaluateExpression", "datapipeline:GetPipelineDefinition", "datapipeline:ListPipelines", "datapipeline:QueryObjects", "datapipeline:ValidatePipelineDefinition", "directconnect:Describe*", "ds:DescribeDirectories", "dynamodb:ListStreams", "dynamodb:ListTables", "ec2:Describe*", "ecr:DescribeRepositories", "ecr:GetRepositoryPolicy", "ecs:Describe*", "ecs:List*", "elasticache:Describe*", "elasticbeanstalk:Describe*", "elasticfilesystem:DescribeFileSystems", "elasticloadbalancing:Describe*", "elasticmapreduce:DescribeJobFlows", "elasticmapreduce:ListClusters", "elasticmapreduce:ListInstances", "es:Describe*", "es:ListDomainNames", "events:DescribeEventBus", "events:ListRules", "firehose:Describe*", "firehose:List*", "gamelift:ListBuilds", "gamelift:ListFleets", "glacier:DescribeVault", "glacier:GetVaultAccessPolicy", "glacier:ListVaults", "iam:GenerateCredentialReport", "iam:Get*", "iam:List*", "iot:ListThings", "kinesis:ListStreams", "kinesisanalytics:ListApplications", "kms:Describe*", "kms:Get*", "kms:List*", "lambda:GetPolicy", "lambda:ListFunctions", "logs:DescribeResourcePolicies", "logs:DescribeLogGroups", "logs:DescribeMetricFilters", "machinelearning:DescribeMLModels", "mediastore:GetContainerPolicy", "mediastore:ListContainers", "opsworks-cm:DescribeServers", "rds:Describe*", "rds:DownloadDBLogFilePortion", "rds:ListTagsForResource", "redshift:Describe*", "route53:Get*", "route53:List*", "route53domains:GetDomainDetail", "route53domains:GetOperationDetail", "route53domains:ListDomains", "route53domains:ListOperations", "route53domains:ListTagsForDomain", "s3:GetAccelerateConfiguration", "s3:GetAnalyticsConfiguration", "s3:GetBucket*", "s3:GetEncryptionConfiguration", "s3:GetInventoryConfiguration", "s3:GetLifecycleConfiguration", "s3:GetMetricsConfiguration", "s3:GetObjectAcl", "s3:GetObjectVersionAcl", "s3:GetReplicationConfiguration", "s3:ListAllMyBuckets", "sdb:DomainMetadata", "sdb:ListDomains", "serverlessrepo:GetApplicationPolicy", "serverlessrepo:ListApplications", "ses:GetIdentityDkimAttributes", "ses:GetIdentityVerificationAttributes", "ses:ListIdentities", "snowball:ListClusters", "snowball:ListJobs", "sns:GetTopicAttributes", "sns:ListSubscriptionsByTopic", "sns:ListTopics", "sqs:GetQueueAttributes", "sqs:ListQueues", "ssm:DescribeDocumentPermission", "ssm:ListDocuments", "states:ListStateMachines", "storagegateway:DescribeBandwidthRateLimit", "storagegateway:DescribeCache", "storagegateway:DescribeCachediSCSIVolumes", "storagegateway:DescribeGatewayInformation", "storagegateway:DescribeMaintenanceStartTime", "storagegateway:DescribeNFSFileShares", "storagegateway:DescribeSnapshotSchedule", "storagegateway:DescribeStorediSCSIVolumes", "storagegateway:DescribeTapeArchives", "storagegateway:DescribeTapeRecoveryPoints", "storagegateway:DescribeTapes", "storagegateway:DescribeUploadBuffer", "storagegateway:DescribeVTLDevices", "storagegateway:DescribeWorkingStorage", "storagegateway:List*", "tag:GetResources", "tag:GetTagKeys", "trustedadvisor:Describe*", "waf:ListWebACLs", "waf-regional:ListWebACLs"]
                }]
            }
        }, {
            "name": null,
            "id": "arn:aws:iam::aws:policy/AmazonInspectorReadOnlyAccess",
            "relationType": "DirectlyAttached",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["inspector:Describe*", "inspector:Get*", "inspector:List*", "inspector:LocalizeText", "inspector:Preview*", "ec2:DescribeInstances", "ec2:DescribeTags", "sns:ListTopics", "events:DescribeRule", "events:ListRuleNamesByTarget"],
                    "Resource": "*"
                }]
            }
        }],
        "vpc": null,
        "id": "AROAIC3FAVDTFA5ARHK5I",
        "type": "IamRole",
        "name": "readonlypermissionsdome9-Role-HZQA3GMOJELS",
        "dome9Id": "1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|iam|AROAIC3FAVDTFA5ARHK5I-62362",
        "accountNumber": "905007184296",
        "region": null,
        "source": "db",
        "tags": []
    }
}


#IAM USER EXMAPLE:
{
    "policy": {
        "name": "sns_failed_events",
        "description": ""
    },
    "bundle": {
        "name": "Copy of sns_send_event_failures",
        "description": ""
    },
    "reportTime": "2018-01-30T03:05:14.489Z",
    "rule": {
        "name": "iamuser should fail",
        "description": "",
        "remediation": "",
        "complianceTags": "",
        "severity": "High"
    },
    "status": "Failed",
    "account": {
        "id": "905007184296",
        "vendor": "Aws"
    },
    "entity": {
        "createDate": 1483998628,
        "passwordLastUsed": 1517239732,
        "arn": "arn:aws:iam::905007184296:root",
        "path": null,
        "managedPolicies": null,
        "inlinePolicies": null,
        "attachedGroups": null,
        "passwordEnabled": false,
        "passwordLastChanged": -62135596800,
        "passwordNextRotation": -62135596800,
        "mfaActive": false,
        "firstAccessKey": {
            "isActive": true,
            "lastRotated": 1505498566,
            "lastUsedDate": -62135596800,
            "lastUsedRegion": "",
            "lastUsedService": ""
        },
        "secondAccessKey": {
            "isActive": true,
            "lastRotated": 1505498570,
            "lastUsedDate": -62135596800,
            "lastUsedRegion": "",
            "lastUsedService": ""
        },
        "firstCertificate": {
            "isActive": false,
            "lastRotated": -62135596800
        },
        "secondCertificate": {
            "isActive": false,
            "lastRotated": -62135596800
        },
        "combinedPolicies": null,
        "vpc": null,
        "id": "",
        "type": "IamUser",
        "name": "<root_account>",
        "dome9Id": "",
        "accountNumber": "905007184296",
        "region": null,
        "source": "db",
        "tags": []
    }
}


#INSTANCE EXAMPLE
{
    "policy": {
        "name": "sns_failed_events",
        "description": ""
    },
    "bundle": {
        "name": "Copy of sns_send_event_failures",
        "description": ""
    },
    "reportTime": "2018-01-30T03:05:14.489Z",
    "rule": {
        "name": "this rule should fail",
        "description": "",
        "remediation": "",
        "complianceTags": "pci 2.3|AUTO: delete_sg",
        "severity": "High"
    },
    "status": "Failed",
    "account": {
        "id": "905007184296",
        "vendor": "Aws"
    },
    "region": "Oregon",
    "entity": {
        "image": "ami-bf4193c7",
        "kernelId": null,
        "platform": "linux",
        "launchTime": 1514572312,
        "inboundRules": [],
        "outboundRules": [],
        "nics": [{
            "id": "eni-1c24c23e",
            "name": "eth0",
            "subnet": {
                "state": "available",
                "availabilityZone": "us-west-2b",
                "defaultForAz": true,
                "mapPublicIpOnLaunch": true,
                "availableIpAddressCount": 4086,
                "externalId": "subnet-ee5d8b89",
                "name": "",
                "description": "",
                "cidr": "172.31.16.0/20",
                "nacl": {
                    "inbound": [{
                        "name": "",
                        "number": 100,
                        "protocol": "ALL",
                        "source": "0.0.0.0/0",
                        "destination": "0.0.0.0/0",
                        "destinationPort": 0,
                        "destinationPortTo": 65535,
                        "direction": "INBOUND",
                        "action": "ALLOW"
                    }, {
                        "name": "",
                        "number": 32766,
                        "protocol": "ALL",
                        "source": "172.31.48.0/28",
                        "destination": "0.0.0.0/0",
                        "destinationPort": 0,
                        "destinationPortTo": 65535,
                        "direction": "INBOUND",
                        "action": "ALLOW"
                    }, {
                        "name": "",
                        "number": 32767,
                        "protocol": "ALL",
                        "source": "0.0.0.0/0",
                        "destination": "0.0.0.0/0",
                        "destinationPort": 0,
                        "destinationPortTo": 65535,
                        "direction": "INBOUND",
                        "action": "DENY"
                    }],
                    "outbound": [{
                        "name": "",
                        "number": 100,
                        "protocol": "ALL",
                        "source": "0.0.0.0/0",
                        "destination": "0.0.0.0/0",
                        "destinationPort": 0,
                        "destinationPortTo": 65535,
                        "direction": "OUTBOUND",
                        "action": "ALLOW"
                    }, {
                        "name": "",
                        "number": 32767,
                        "protocol": "ALL",
                        "source": "0.0.0.0/0",
                        "destination": "0.0.0.0/0",
                        "destinationPort": 0,
                        "destinationPortTo": 65535,
                        "direction": "OUTBOUND",
                        "action": "DENY"
                    }],
                    "isDefault": true,
                    "vpc": {
                        "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
                        "cidr": "172.31.0.0/16",
                        "region": "us_west_2",
                        "id": "vpc-3543f352",
                        "accountNumber": "905007184296",
                        "vpnGateways": [],
                        "internetGateways": [{
                            "externalId": "igw-3c6b2a58",
                            "vpcAttachments": [{
                                "state": "available",
                                "vpcId": "vpc-3543f352"
                            }],
                            "name": ""
                        }],
                        "dhcpOptionsId": "dopt-b18786d5",
                        "instanceTenancy": "default",
                        "isDefault": true,
                        "state": "available",
                        "tags": {},
                        "name": "",
                        "source": "Db"
                    },
                    "id": "acl-f0395e97",
                    "type": "NACL",
                    "name": "",
                    "dome9Id": "1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|5|nacl|acl-f0395e97-62362",
                    "accountNumber": "905007184296",
                    "region": "us_west_2",
                    "source": "db",
                    "tags": [{
                        "key": "AlertLogic-EnvironmentID",
                        "value": "E49BD84B-9720-455D-B7CF-4B3500443FD3"
                    }, {
                        "key": "AlertLogic-AccountID",
                        "value": "134224348"
                    }, {
                        "key": "AlertLogic",
                        "value": "Security"
                    }]
                },
                "vpc": {
                    "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
                    "cidr": "172.31.0.0/16",
                    "region": "us_west_2",
                    "id": "vpc-3543f352",
                    "accountNumber": "905007184296",
                    "vpnGateways": [],
                    "internetGateways": [{
                        "externalId": "igw-3c6b2a58",
                        "vpcAttachments": [{
                            "state": "available",
                            "vpcId": "vpc-3543f352"
                        }],
                        "name": ""
                    }],
                    "dhcpOptionsId": "dopt-b18786d5",
                    "instanceTenancy": "default",
                    "isDefault": true,
                    "state": "available",
                    "tags": {},
                    "name": "",
                    "source": "Db"
                },
                "id": "subnet-ee5d8b89",
                "type": "Subnet",
                "dome9Id": "1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|5|subnet|subnet-ee5d8b89-62362",
                "accountNumber": "905007184296",
                "region": "us_west_2",
                "source": "db",
                "tags": []
            },
            "privateDnsName": "ip-172-31-30-90.us-west-2.compute.internal",
            "publicIpAddress": "",
            "privateIpAddress": "172.31.30.90",
            "securityGroups": [{
                "description": "launch-wizard-5 created 2017-12-29T09:14:16.382-08:00",
                "inboundRules": [],
                "outboundRules": [],
                "networkAssetsStats": [],
                "isProtected": false,
                "vpc": {
                    "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
                    "cidr": "172.31.0.0/16",
                    "region": "us_west_2",
                    "id": "vpc-3543f352",
                    "accountNumber": "905007184296",
                    "vpnGateways": [],
                    "internetGateways": [{
                        "externalId": "igw-3c6b2a58",
                        "vpcAttachments": [{
                            "state": "available",
                            "vpcId": "vpc-3543f352"
                        }],
                        "name": ""
                    }],
                    "dhcpOptionsId": "dopt-b18786d5",
                    "instanceTenancy": "default",
                    "isDefault": true,
                    "state": "available",
                    "tags": {},
                    "name": "",
                    "source": "Db"
                },
                "id": "sg-7badea07",
                "type": "SecurityGroup",
                "name": "launch-wizard-5",
                "dome9Id": "2384935",
                "accountNumber": "905007184296",
                "region": "us_west_2",
                "source": "db",
                "tags": []
            }]
        }],
        "isPublic": false,
        "instanceType": "t2.nano",
        "isRunning": false,
        "volumes": [{
            "attachments": [{
                "attachTime": 1514567667,
                "deleteOnTermination": true,
                "device": "/dev/xvda",
                "instanceId": "i-0579293b8a3aeafb9",
                "state": "attached",
                "volumeId": "vol-02b194a15d9c58429"
            }],
            "availabilityZone": "us-west-2b",
            "createTime": 1514567667,
            "encrypted": false,
            "iops": 100,
            "kmsKeyId": null,
            "size": 8,
            "snapshotId": "snap-016f4ef92d26f9538",
            "state": "in-use",
            "tags": [],
            "volumeId": "vol-02b194a15d9c58429",
            "volumeType": "gp2"
        }],
        "profileArn": null,
        "roles": [],
        "scanners": {
            "scans": null,
            "findings": null
        },
        "vpc": {
            "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
            "cidr": "172.31.0.0/16",
            "region": "us_west_2",
            "id": "vpc-3543f352",
            "accountNumber": "905007184296",
            "vpnGateways": [],
            "internetGateways": [{
                "externalId": "igw-3c6b2a58",
                "vpcAttachments": [{
                    "state": "available",
                    "vpcId": "vpc-3543f352"
                }],
                "name": ""
            }],
            "dhcpOptionsId": "dopt-b18786d5",
            "instanceTenancy": "default",
            "isDefault": true,
            "state": "available",
            "tags": {},
            "name": "",
            "source": "Db"
        },
        "id": "i-0579293b8a3aeafb9",
        "type": "Instance",
        "name": "test2222",
        "dome9Id": "",
        "accountNumber": "905007184296",
        "region": "us_west_2",
        "source": "db",
        "tags": [{
            "key": "owner",
            "value": "Who owns this box"
        }, {
            "key": "thisimykey",
            "value": "thisismyvalue"
        }, {
            "key": "(thisi",
            "value": "mykey:thisismyvalue)"
        }]
    }
}



#S3 BUCKET EXMAPLE

{
    "policy": {
        "name": "sns_failed_events",
        "description": ""
    },
    "bundle": {
        "name": "Copy of sns_send_event_failures",
        "description": ""
    },
    "reportTime": "2018-01-30T03:05:14.489Z",
    "rule": {
        "name": "s3 should fail",
        "description": "",
        "remediation": "",
        "complianceTags": "",
        "severity": "High"
    },
    "status": "Failed",
    "account": {
        "id": "905007184296",
        "vendor": "Aws"
    },
    "region": "",
    "entity": {
        "logging": {
            "targetBucketName": null,
            "targetPrefix": null,
            "grants": [],
            "enabled": false
        },
        "acl": {
            "grants": [{
                "canonicalUser": "db1b62654bda37f8a0d7ea765caa232a3950af8a64ef30f976417454e644bfa5",
                "displayName": "alex",
                "emailAddress": null,
                "premission": "FULL_CONTROL",
                "premissionHeaderName": "x-amz-grant-full-control",
                "type": "CanonicalUser",
                "uri": null
            }],
            "ownerDisplayName": "alex",
            "ownerId": "db1b62654bda37f8a0d7ea765caa232a3950af8a64ef30f976417454e644bfa5"
        },
        "policy": {
            "Version": "2012-10-17",
            "Statement": [{
                "Sid": "AWSCloudTrailAclCheck20150319",
                "Effect": "Allow",
                "Principal": {
                    "Service": "cloudtrail.amazonaws.com"
                },
                "Action": "s3:GetBucketAcl",
                "Resource": "arn:aws:s3:::sg-663eb256"
            }, {
                "Sid": "AWSCloudTrailWrite20150319",
                "Effect": "Allow",
                "Principal": {
                    "Service": "cloudtrail.amazonaws.com"
                },
                "Action": "s3:PutObject",
                "Resource": "arn:aws:s3:::sg-663eb256/AWSLogs/905007184296/*",
                "Condition": {
                    "StringEquals": {
                        "s3:x-amz-acl": "bucket-owner-full-control"
                    }
                }
            }]
        },
        "versioning": {
            "status": "Off",
            "mfaDelete": false
        },
        "website": {
            "indexDocumentSuffix": null,
            "errorDocument": null,
            "routingRules": [],
            "redirectAllRequestsTo": {
                "hostName": "",
                "httpRedirectCode": "",
                "protocol": "",
                "replaceKeyPrefixWith": "",
                "replaceKeyWith": ""
            }
        },
        "encryption": {
            "serverSideEncryptionRules": []
        },
        "replication": {
            "role": "",
            "rules": []
        },
        "vpc": null,
        "id": "sg-663eb256",
        "type": "S3Bucket",
        "name": "sg-663eb256",
        "dome9Id": "1|89ff48fc-9c8b-4292-a169-d6e938af2dd2|rg|s3Bucket|sg-663eb256-62362",
        "accountNumber": "905007184296",
        "region": "",
        "source": "db",
        "tags": []
    }
}







'''