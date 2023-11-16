aws cloudformation deploy --template-file pipeline.json \
  --stack-name FetchProcess --parameter-overrides \
  GithubOwner=selobu \
  GithubRepoName=fetchprocess \
  --capabilities CAPABILITY_IAM