from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Avtor(models.Model):
    ime = models.CharField(max_length=50)
    prezime = models.CharField(max_length=50)
    image = models.FileField(upload_to="files/", null=True, blank=True)
    interest = models.CharField(max_length=100, null=True, blank=True)
    skills = models.CharField(max_length=100, null=True, blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.ime+" "+self.prezime

class Post(models.Model):
    naslov = models.CharField(max_length=50)
    avtor = models.ForeignKey(Avtor, on_delete=models.CASCADE)
    sodrzina = models.TextField(null=True, blank=True)
    datum_created = models.DateField(auto_now_add=True)
    datum_last_modified = models.DateField(auto_now_add=True)
    blocked_users = models.ManyToManyField(User, related_name='blocked_posts', blank=True)
    file = models.FileField(upload_to="files/", null=True, blank=True)

    def __str__(self):
        return self.naslov

class Komentar(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Avtor, on_delete=models.CASCADE)
    sodrzina = models.TextField(null=True, blank=True)
    datum_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sodrzina

class Blok(models.Model):
   bloker = models.ForeignKey(Avtor, on_delete=models.CASCADE, related_name="user_bloker")
   blokiran = models.ForeignKey(Avtor, on_delete=models.CASCADE, related_name="user_blokiran")
  # blokirani_posts = models.ManyToManyField(Post, blank=True)

   def __str__(self):
        return str(self.bloker) + " blocked " + str(self.blokiran)
