from fastapi_admin.models import AbstractAdmin
from tortoise import Model, fields


class Admin(AbstractAdmin):
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}#{self.username}"


class BotSettings(Model):
    subscribe_channel = fields.CharField(max_length=30)
    subscribe_channel_url = fields.TextField()
    subscribe_channel_name = fields.TextField()
    basket_channel = fields.CharField(max_length=30)
    night_mode = fields.CharField(max_length=30, default="22:00-7:00")


class BotAdmin(Model):
    telegram_id = fields.CharField(max_length=30)
    username = fields.CharField(max_length=100)
    fullname = fields.CharField(max_length=200)


class Group(Model):
    group_id = fields.CharField(max_length=30)


class BanWords(Model):
    words = fields.TextField()


class ServiceMessages(Model):
    night_time = fields.TextField()
