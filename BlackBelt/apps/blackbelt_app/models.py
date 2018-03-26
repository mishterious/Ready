from __future__ import unicode_literals

from django.db import models
import re, datetime, time
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        errors = {}
        email = postData['email'].lower()
        if len(postData['first_name']) < 2 or (postData['first_name'].isalpha()) != True:
            errors['first_name'] = "Your first name should be at least 2 letters long and should only be letters"
        if len(postData['last_name']) < 2 or (postData['last_name'].isalpha()) != True:
            errors['last_name'] = "Your first name should be at least 2 letters long and should only be letters"
        if len(email) < 1:
            errors['email'] = "Please enter an e-mail address"
        if not EMAIL_REGEX.match(email):
            errors['email2'] = "Please enter a Valid e-mail address"
        if re.search('[0-9]', postData['password']) is None:
            errors['numpass'] = "You need to enter at least one number to make your password Valid"
        if re.search('[A-Z]', postData['password']) is None:
            errors['capspass'] = "You will need to enter at least one capital letter"
        if len(postData['password']) < 8:
            errors['lenpass'] = "Your password needs to be at least 8 character to be Valid"
        elif postData['password'] != postData['confirm']:
            errors['mispass'] = "Your passwords do not match"
        if len(postData['birthday']) < 1:
            errors['lenday'] = "Please enter a valid birthday"
        if postData['birthday'] > timestamp:
            errors['future'] = "Please enter a date in the Past"
        user = User.objects.filter(email=email)
        if len(user) > 0:
            errors['user'] = "User already exists in the database"

        return errors

    def login_validator(self, postData):
        errors = {}
        checkpass = postData['password']
        email = postData['email'].lower()
        if len(email) < 1:
            errors['email'] = "Please enter an e-mail address"
        if not EMAIL_REGEX.match(email):
            errors['email2'] = "Please enter a Valid e-mail address"
        if len(checkpass) < 1:
            errors['lenpass'] = "Please enter your password"
        if len(errors):
            return errors
            
        if len(User.objects.filter(email=email)) < 1:
            errors['checkuser'] = "Your username or password is incorrect"
        else:
            a = User.objects.get(email=email).password 
            if bcrypt.checkpw(checkpass.encode(), a.encode()) == False:
                errors['mispass'] = "Your username or password is incorrect"
        return errors
            
        
        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()
    
    def __repr__(self):
        return "<User object: {} {}, {}, {}>".format(self.first_name, self.last_name, self.email, self.birthday)


class Post(models.Model):
    post = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="myposts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<Post object: {} {}, {}, {}>".format(self.post, self.user)
