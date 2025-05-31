make ci
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 211125345442.dkr.ecr.us-east-1.amazonaws.com
docker build -t review_extractor .
docker tag review_extractor:latest 211125345442.dkr.ecr.us-east-1.amazonaws.com/review_extractor:latest
docker push 211125345442.dkr.ecr.us-east-1.amazonaws.com/review_extractor:latest

