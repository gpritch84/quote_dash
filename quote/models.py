from django.db import models
import re

class UserManager(models.Manager):
    def register_validator(self,postData):
        errors= {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if postData['password'] != postData ['con_pass']:
            errors['con_pass'] = "Passwords must match!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] =  "Invalid email address"
        if len(postData['password']) < 8:
            errors['password'] = "Password must have at least 8 characters"
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must have at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must have at least 2 characters"
        return errors

    def login_validator(self,postData):
        errors= {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['login'] = "Invalid Email/Password"
        if len(postData['login_password'])<8:
            errors['password'] = "Invalid Email/Password"
        return errors

    def edit_validator(self,postData):
        errors= {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['edit_email']):
            errors['edit_email'] =  "Invalid email address"
        if len(postData['edit_first_name']) < 2:
            errors['edit_first_name'] = "First name must have at least 2 characters"
        if len(postData['edit_last_name']) < 2:
            errors['edit_last_name'] = "Last name must have at least 2 characters"
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self,postData):
        errors={}
        if len(postData['author'])==0:
            errors['author'] = "An author is required."
        if len(postData['quote'])==0:
            errors['quote'] = "A qoute is required."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name='quotes', on_delete = models.CASCADE)
    users = models.ManyToManyField(User, related_name='many_quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()