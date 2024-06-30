EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'senderemail@gmail.com' #change
EMAIL_HOST_USER = 'senderemail@gmail.com' #change
EMAIL_HOST_PASSWORD = 'password for that email' #change
EMAIL_PORT = 587

PASSWORD_RESET_TIMOUT = 14400