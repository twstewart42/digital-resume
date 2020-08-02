provider "aws" {
  region = "us-east-1"
}
 
module "cloudfront-s3-website" {
    source           = "chgangaraju/cloudfront-s3-website/aws"
    version          = "1.0.0"
    hosted_zone      = "twstewart.me"
    domain_name      = "twstewart.me"
    aws_region       = "us-east-1"
}

module "blog" {
    source           = "chgangaraju/cloudfront-s3-website/aws"
    version          = "1.0.0"
    hosted_zone      = "twstewart.me"
    domain_name      = "blog.twstewart.me"
    aws_region       = "us-east-1"
}

#module "movie-dev" {
#    source           = "chgangaraju/cloudfront-s3-website/aws"
#    version          = "1.0.0"
#    hosted_zone      = "twstewart.me"
#    domain_name      = "avsdvqaega.twstewart.me"
#    aws_region       = "us-east-1"
#}

module "stewstunes_cloudfront_s3_website" {
  # Github Source
  #source      = "git@github.com:twstewart42/terraform-aws-cloudfront-s3-website.git?ref=tags/v1.1.0"
  #local file Source
  #source      = "../../../../../../fun-coding/terraform-aws-cloudfront-s3-website"
  # Terraform registry source
  source       = "twstewart42/cloudfront-s3-website-lambda-edge/aws"
  version      = "1.1.0"
  hosted_zone = "stewstunes.com"
  domain_name = "stewstunes.com"
  aws_region  = "us-east-1"
  tags = {
    Project = "StewStunes"
  }
}
