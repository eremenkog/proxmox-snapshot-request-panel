from django.apps import AppConfig


class RequestSnapshotAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'request_snapshot_app'
    
    def ready(self):
        import request_snapshot_app.signals