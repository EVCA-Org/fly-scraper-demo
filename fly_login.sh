#!/bin/bash

# Check if FLY_API_TOKEN is provided
if [ -z "" ]; then
  echo "Error: FLY_API_TOKEN is not set"
  echo "Usage: FLY_API_TOKEN=your_token ./fly_login.sh"
  exit 1
fi

# Use the token to authenticate with Fly.io
/root/.fly/bin/flyctl auth token ""

# Verify authentication
echo "Checking authentication status:"
/root/.fly/bin/flyctl auth whoami

echo "Ready to deploy to Fly.io!"
