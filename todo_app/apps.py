from django.apps import AppConfig


class TodoAppConfig(AppConfig):
    name = 'todo_app'

    def ready(self):
        import todo_app.tasks
        import todo_app.signals
