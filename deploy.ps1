Write-Output "Starting Deploy of twstewart.me"
#hugo --quiet
#cd public
Write-Output "Sync files to S3"
aws s3 sync . s3://twstewart.me/ --exclude ".terraform*" --exclude ".git/*"

Write-Output "create invalidation"
aws cloudfront create-invalidation --distribution-id EVKCSGZJP1XAR --paths "/*"

#cd ../
Write-Output "Deploy of twstewart.me is complete"