#!/bin/bash

# Script to set up Supabase connection for the scraper

echo Setting up Supabase connection for the fly-scraper-demo
echo ------------------------------------------------------
echo

# Check if the Supabase URL and key are provided
if [ -z  ] || [ -z  ]; then
  echo Usage: ./setup_supabase.sh SUPABASE_URL SUPABASE_KEY [TABLE_NAME]
  echo Example: ./setup_supabase.sh https://abcdefghijklm.supabase.co eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... scraped_data
  exit 1
fi

SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_TABLE=scraped_data

# Set the secrets in Fly.io
echo Setting Fly.io secrets...
/root/.fly/bin/flyctl secrets set SUPABASE_URL= SUPABASE_KEY= SUPABASE_TABLE=

# Check if the secrets were set successfully
if [ 0 -eq 0 ]; then
  echo ✅ Supabase connection details set as Fly.io secrets
else
  echo ❌ Failed to set Fly.io secrets
  exit 1
fi

echo
echo Supabase Configuration Complete!
echo
echo Next steps:
echo 1. Create the required table in Supabase using the supabase_setup.sql file
echo 2. Deploy your application with: flyctl deploy
echo
