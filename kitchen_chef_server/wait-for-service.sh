#!/bin/sh

# Wait for the service to be up
until eval $SERVICE_CHECK_COMMAND
do
  echo "Waiting for the service to be up..."
  sleep 30
done

echo "Service is up!"

# Run the command when the service is up
echo "Running post-startup command..."
eval $POST_STARTUP_COMMAND
