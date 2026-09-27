kubectl create secret generic challenge-app-secret \
  --from-literal=SECRET_KEY="your_secret_key" \
  --from-literal=GOOGLE_API_KEY="your_google_api_key" \
  --from-literal=IMAGEKIT_PRIVATE_KEY="your_imagekit_private_key" \
  --from-literal=RABBITMQ_PASS="your_rabbitmq_password" \
  --from-literal=MAILTRAP_USERNAME="your_mailtrap_username" \
  --from-literal=MAILTRAP_PASSWORD="your_mailtrap_password" \
  --from-literal=POSTGRES_PASS="your_postgres_password"