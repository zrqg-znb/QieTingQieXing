from django.apps import AppConfig


class AuthorityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authority'
    verbose_name = '用户认证与授权'