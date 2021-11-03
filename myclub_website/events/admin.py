from django.contrib import admin
from .models import Venue, MyClubUser, Event


# admin.site.register(Venue, VenueAdmin)
# admin.site.register(Venue)
admin.site.register(MyClubUser)
# admin.site.register(Event)

'''
Personalizando o admin do django neste caso abaico em 
relação ao Venue, é mostrado na tela name, address, phone
'''
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name','address','phone') # lista na tela este campos
    ordering = ('name',) # ordena na ordem alfabetica se -name  inverte  
    search_fields = ('name','address') # realiza busca por estes dois campos
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name','venue'),'event_date','description','manager') # campos que irão aparecer na tela de cadastro
    list_display = ('name','event_date','venue')
    list_filter = ('event_date','venue') # criar o filtro lateral com estes campos definidos
    ordering = ('-event_date',)