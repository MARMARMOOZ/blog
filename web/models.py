from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#Topics model
class Topic(models.Model):
    #id of topic
    id = models.IntegerField(primary_key=True)
    #title of topic
    title = models.CharField(max_length=30)
    #published date of topic
    datepublished = models.DateField()
    #content of topic(included tags and DTL)
    textn_tags = models.TextField()
    #publisher user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
#User Token model
class Token(models.Model):
    #user object stored in variable to being linked to token
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #actual token is a Hash SHA1 Random Charachters
    token = models.CharField(max_length=40)
    def __str__(self):
        return self.user.username
#Comments model
class Comments(models.Model):
    #The Id of comment topic
    topic_id = models.IntegerField()
    #object of User Token
    user_token = models.ForeignKey(Token, on_delete=models.CASCADE)
    #Charfield of comment
    comment = models.CharField(max_length=50)
    def __str__(self):
        return self.comment