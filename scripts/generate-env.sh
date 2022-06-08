echo DB_USERNAME=$DB_USERNAME >> .env
echo DB_HOST=$DB_HOST >> .env
echo DB_PASSWORD=$DB_PASSWORD >> .env
echo DB_PORT=$DB_PORT >> .env
echo DB_NAME=$DB_NAME >> .env

echo JWT_TOKEN=$JWT_TOKEN >> .env
echo JWT_EMAIL_VERIFICATION_TOKEN=$JWT_EMAIL_VERIFICATION_TOKEN >> .env
echo JWT_PASSWORD_RESET_TOKEN=$JWT_PASSWORD_RESET_TOKEN >> .env

REDIS_HOST=$REDIS_HOST >> .env
REDIS_PORT=$REDIS_PORT >> .env
REDIS_USERNAME=$REDIS_USERNAME >> .env
REDIS_PASSWORD=$REDIS_PASSWORD >> .env

echo EMAILS_ENABLED=$EMAILS_ENABLED >> .env
echo EMAIL_TEMPLATES_DIR=$EMAIL_TEMPLATES_DIR >> .env
echo MAILS_FROM_NAME=$MAILS_FROM_NAME >> .env
echo EMAILS_SMTP_HOST=$EMAILS_SMTP_HOST >> .env
echo EMAILS_PORT=$EMAILS_PORT >> .env
echo EMAILS_USER=$EMAILS_USER >> .env
echo EMAILS_PASSWORD=$EMAILS_PASSWORD >> .env

echo CORS_ALLOWED_ORIGINS=$CORS_ALLOWED_ORIGINS >> .env