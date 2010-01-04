# About
This is a django mining investment website where users invest and get profits depending on selected mining package.
Investment package increments profit everyday and returns capital + profits on the last day of the package.


# Technical details
* Function to run investment process to increment profit till end of investment was implemented without use of background task running services 
such as celery, redis, crontab, django-scheduler etc
* Function to delete notifications of user longer than 3days was implemented using similar method to the above
* Diverse pages were made to run either of the above functions rather than both to reduce load time(speed)
* A single function handles account credit and debit, saves the transaction record and sends appropriate notification 
* Users can get their investment details in PDF
* Gets users location and timezone on sign up
* Ajax and animations


# Features
* Emailing functionality
* Authentication and authorization
* User referral and commission program
* Function to update investments without background tasks libraries like celery, redis etc
* Ajax functionalities to communicate to backend without page reload
* Notification features and auto delete functionality
* Beautiful admin dashboard using django-jazzmin
* Error 404 and 500 pages implemented to handle error pages.
* Configured to use cloudinary cloud storage to serve media files.
* Password reset functionality


# Technologies
* Python
* Django
* Vanilla Javascript
* Ajax


# Pages
Project contains 25+ pages in total outside admin dashboard which includes index, contact, faq, register, login,
dashboard, profile, update password, create investment, invoice, investment history, withdraw, withdraw history, notifications,
affiliates, success, error pages(404 and 500) and password reset pages.


# Libraries used
// Dependent libraries
Django==3.2.2
Pillow==9.2.0
django-cloudinary-storage==0.3.0
python-magic==0.4.25
python-decouple==3.6
django-jazzmin>=2.6.0
reportlab==3.6.10
whitenoise==5.3.0
gunicorn==20.1.0

// Non dependent libraries
psycopg2==2.9.2
dj-database-url==0.5.0
