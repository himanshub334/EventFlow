#!/bin/sh
set -e
awslocal sqs create-queue --queue-name eventflow-events-dlq || true
awslocal sqs create-queue --queue-name eventflow-events || true
echo "EventFlow SQS queues initialized."
