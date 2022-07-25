from django.db import models

class StudentData(models.Model) :
    first_name = models.CharField(max_length = 100 , required = True)
    last_name  = models.CharField(max_length = 100 , required = True)
    age        = models.IntegerField(max_length = 100 , required = True)
    branch     = models.CharField(max_length = 100 , required = True)
    
    def __str__(self) :
        return "{} {}".format(first_name , last_name)