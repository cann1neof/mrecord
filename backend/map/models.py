from django.db import models

class DeliveryMap(models.Model):
    name = models.CharField(max_length=48)
    additional = models.TextField()
    coords = models.CharField(max_length=48)

    def get_map_obj(self):
        return {
            'coords': [float(i) for i in self.coords.split(', ')],
            'text': self.additional,
            'headline': self.name
        }
