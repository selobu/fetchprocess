aws cloudformation describe-stacks --stack-name FetchProcess --query "Stacks[].Outputs[?OutputKey=='EndpointURL'][] | [0].OutputValue"