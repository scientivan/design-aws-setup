#!/usr/bin/env bash
# Buat repositori ECR jika perlu, beri tag, lalu unggah kedua image dari Cloud9.
set -euo pipefail
REGION=${AWS_REGION:-us-east-1}
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
REG=$ACCOUNT.dkr.ecr.$REGION.amazonaws.com
TAG=${TAG:-v1}
aws ecr get-login-password --region "$REGION" | docker login -u AWS --password-stdin "$REG"
for svc in event-service ticket-service; do
  aws ecr describe-repositories --repository-names "ticketing/$svc" --region "$REGION" >/dev/null 2>&1 \
    || aws ecr create-repository --repository-name "ticketing/$svc" --region "$REGION" \
         --image-scanning-configuration scanOnPush=true --query repository.repositoryUri --output text
  docker tag "$svc" "$REG/ticketing/$svc:$TAG"
  docker push "$REG/ticketing/$svc:$TAG"
done
aws ecr describe-images --repository-name ticketing/event-service --region "$REGION" \
  --query 'imageDetails[].{tags:imageTags,pushedAt:imagePushedAt,sizeBytes:imageSizeInBytes}' --output table
aws ecr describe-images --repository-name ticketing/ticket-service --region "$REGION" \
  --query 'imageDetails[].{tags:imageTags,pushedAt:imagePushedAt,sizeBytes:imageSizeInBytes}' --output table
echo "ECR_PUSH_DONE"
