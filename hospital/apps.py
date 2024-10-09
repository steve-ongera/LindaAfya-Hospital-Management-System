from django.apps import AppConfig


#class HospitalConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    #name = 'hospital'

class HospitalConfig(AppConfig):
    name = 'hospital'

    def ready(self):
        import hospital.signals