from __future__ import unicode_literals
from django.db import models
import re, bcrypt


class UserManager(models.Manager):
    def validate(self, PostData):
        errors=[] #if anything goes wrong, we push to the errors list
        if len(PostData["first_name"])==0:
            errors.append("Missing First Name!")
        elif len(PostData["first_name"]) < 3:
            errors.append("First_name can't be less than three characters")
        elif not re.search(r'^[A-Za-z]+$', PostData["first_name"]):
            errors.append("Humans dont have numbers in their first name...")
        if len(PostData["last_name"]) == 0:
            errors.append("Missing Last Name!")
        elif len(PostData["last_name"]) < 3:
            errors.append("Last Name can't be less than three characters")
        elif not re.search(r'^[A-Za-z]+$', PostData["last_name"]):
            errors.append("Humans dont have numbers in their last name...")
        if len(PostData["email"]) == 0:
            errors.append("Missing Email!")
        elif len(PostData["email"]) < 2:
            errors.append("Email can't be less than two characters")
        elif not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', PostData["email"]):
            errors.append("Incorrect email format")
        if len(PostData["password"]) == 0:
            errors.append("Missing Password!")
        elif len(PostData["password"]) < 8:
            errors.append("Password has to be longer than 8 characters long")
        elif not re.search(r'^[a-zA-Z0-9]+$', PostData["password"]):
            errors.append("Incorrect password format")
        if PostData["password_confirm"] != PostData["password"]:
            errors.append("Passwords do not match up")
        if len(errors) == 0:
            Users = self.create(first_name = PostData['first_name'], last_name = PostData['last_name'], email = PostData['email'], password = bcrypt.hashpw(PostData['password'].encode(), bcrypt.gensalt()))
            return(True, Users)
        else:
            return(False, errors)

    def authenticate(self, postData):
        if "email" in postData and "password" in postData:
            try:
                user = User.objects.get(email=postData["email"])
            except:
                return (False, "Invalid email or password")
            if bcrypt.hashpw(postData['password'].encode(), user.password.encode()) == user.password.encode():
                return (True, user)
            else:
                return (False, "Invalid email or password")
        else:
            return (False, "Please enter login information")



class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
