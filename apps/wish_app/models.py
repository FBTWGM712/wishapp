from __future__ import unicode_literals

from django.db import models

import re, bcrypt

# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, postData):
        email_regex =  re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        # print(postData)
        if User.objects.filter(email = postData['email']):
            errors['email_exists'] = "An account is already associated with that email"
        if (len(postData['name']) < 1) or (len(postData['last_name']) < 1) or (len(postData['email']) < 1):
            errors["blank"] = "All fields are required and must not be blank!"
        if len(postData['name']) < 2:
            errors['name'] = "needs to be longer than 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "needs to be longer than 2 characters"
        if not email_regex.match(postData['email']):
            errors['email']="Email must be a valid format"
        if len(postData['password'])<8:
            errors['password']= "Password must be at least 8 character"
        if postData['password'] != postData['confirm']:
            errors['confirm']= "Password and Confirm must match"
        
        return errors
    def log_validator(self, postData):
        user = User.objects.filter(email= postData['email'])
        errors = {}
        if not user:
            errors['email'] = "Insert a valid email"
        return errors

class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        wish = postData["wish"]
        description = postData["description"]
        try:
            wish_check_unique = Wish.objects.get(wish=postData["wish"])
        except Wish.DoesNotExist:
            wish_check_unique = True

        if len(wish) == 0:
            errors["wish"] = "Please enter a title for the wish."
            print("wish error") 
        if len(description) == 0:
            errors["description"] = "Please enter wish description"
            print("description error")

        if (len(postData['wish']) < 1) or (len(postData['description']) < 1):
            errors["blank"] = "All fields are required and must not be blank!"
    
        if (len(postData['wish']) < 5) or (len(postData['description']) < 8):
            errors["char"] = "insufficient characters"
 
        if wish_check_unique != True:
            errors["wish"] = "Wish already exists"
            print("duplicate wish") 
        return errors

    def wish_validator_edit(self, postData):
        errors = {}
        wish = postData["form_edit_title"]
        description = postData["form_edit_desc"]
        try:
            wish_check_unique = Wish.objects.get(wish=postData["form_edit_title"])
        except Wish.DoesNotExist:
            wish_check_unique = True

        if len(wish) == 0:
            errors["wish"] = "Please enter a title for the wish."
            print("wish error") 
        if len(description) == 0:
            errors["description"] = "Please enter wish description"
            print("description error")

        if (len(postData['form_edit_title']) < 1) or (len(postData['form_edit_desc']) < 1):
            errors["blank"] = "All fields are required and must not be blank!"
    
        if (len(postData['form_edit_title']) < 5) or (len(postData['form_edit_desc']) < 8):
            errors["char"] = "insufficient characters"
 
        if wish_check_unique != True:
            errors["wish"] = "Wish already exists"
            print("duplicate wish") 
        return errors


class User(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects =UserManager()

    def __repr__(self):
        return "<User object: {} {}, {}>".format(
            self.name, self.last_name, self.email)

class Wish(models.Model):
    wish = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    submitted_by = models.ForeignKey(User, related_name="wishes_submitted", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "ID: " + str(self.id) + ", Wish: " + self.wish + ", Description: " + self.description +  ", Submitted By: " + str(self.submitted_by) + ", Date Added: "\
        + str(self.created_at)

    objects = WishManager()

class Granted(models.Model):
    user_list = models.ForeignKey(User, related_name="user_granted", on_delete=models.CASCADE)
    wish_granted = models.ForeignKey(Wish, related_name="wishes", on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wish_granted.wish +"("+ str(self.wish_granted.id)+")"