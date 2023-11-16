aws cloudformation describe-stacks --stack-name FetchProcess \
   --query "Stacks[0].Outputs[?OutputKey=='https://github.com/selobu/fetchprocess'] | [0].OutputValue"