# My Digital resume
This repository is for the code and words that make up my digital resume.
Built to be as simplistic as possible,  while still providing great content

The hosting of this content is setup on a static S3 bucket, with cloudfront distribution and SSL termination. [https://twstewart.me](https://twstewart.me)

# Setup
I elected to use terraform to create the S3 bucket, and setup the cloudfront https/CDN capabilities

see [main.tf](main.tf) for more details on the modules I am using to create these assets in AWS.

```
terraform init
terraform plan
terraform apply
```

### Points of information not covered by this terraform module
* Must be using Route53 as primary DNS provider for the domain
* Must already have an ACM cert available in us-east-1 region. Cloudfront can only use certs from us-east-1.
* If using a star cert, Cert must have Subject Alternative matching exact record of the Fully Qualified Domain Name used in Cloudfront

# Deploying Code to an S3 bucket.
At first simple awscli uploads was fine, but as the project grows and tracking changes becomes more involved, I needed a better/more automated solution.

aws cli method
```
aws s3 cp index.html s3://twstewart.me/index.html
```

Using the [deploy.py](deploy.py) script, it compares the md5sum of the content to what S3 has, and if those are different it assumes that the local version is newer and uploads it.

```
$ python3 deploy.py 
README.md
02553fa1c58d56c575ad51ffaa344d36 0eaa144426e1ab562bb8561ad0b9af4e
upload new
LICENSE
3694dc21d7856a346f1d50d039bb3de9 3694dc21d7856a346f1d50d039bb3de9
.gitignore
ee7f8c2e1cc8440043b7bb1a31edcbc3 ee7f8c2e1cc8440043b7bb1a31edcbc3
deploy.py
91b9b0e8e63c8ef891f391904ea2e2e3 91b9b0e8e63c8ef891f391904ea2e2e3
pages/side-projects.html
1080459ca31cb674ee4b120ef17a9547 1080459ca31cb674ee4b120ef17a9547
...
```


