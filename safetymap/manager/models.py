from django.db import models

class Alltimeshop(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return f"Alltimeshop: {self.lon}, {self.lat}"

class Securitycenter(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return f"Securitycenter: {self.lon}, {self.lat}"

class Cctv(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return f"Cctv: {self.lon}, {self.lat}"

class Loadpoint(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return f"Loadpoint: {self.lon}, {self.lat}"

class Lamp(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return f"Lamp: {self.lon}, {self.lat}"
