aws cloudformation deploy --template-file pipeline.json \
  --stack-name FetchProcess --parameter-overrides \
  GithubOwner=selobu \
  GithubRepoName=selobu/fetchprocess \
  --capabilities CAPABILITY_IAM