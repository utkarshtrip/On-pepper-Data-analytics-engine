from django.db import models

class XBRLFile(models.Model):
    file = models.FileField(upload_to='xbrl_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
