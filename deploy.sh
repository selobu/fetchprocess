aws cloudformation deploy --template-file pipeline.json \
  --stack-name FetchProcess --parameter-overrides \
  GithubOwner=selobu \
  GithubRepoName=fetchprocess \
  GithubRepoSecretId=FUTURELOOPACCESSTOKEN \
  --capabilities CAPABILITY_IAM