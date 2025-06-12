# from django.contrib import admin
# from .models import Questions,Disorder, DisorderSave

# # Register your models here.
# admin.site.register(Questions)
# admin.site.register(Disorder)
# admin.site.register(DisorderSave)



from django.contrib import admin
from .models import (
    Questions,
    Disorder,
    DisorderSave,
    Response,
    RegisterUser,
    ChatHistory,
)

admin.site.register(Questions)
admin.site.register(Disorder)
admin.site.register(DisorderSave)
admin.site.register(Response)
admin.site.register(RegisterUser)
admin.site.register(ChatHistory)
