from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.Profile)
admin.site.register(models.CommunityUser)
admin.site.register(models.CommunityFollow)
admin.site.register(models.CommunityProfile)
admin.site.register(models.CommunityLike)
admin.site.register(models.CommunityPost)
admin.site.register(models.SavePost)