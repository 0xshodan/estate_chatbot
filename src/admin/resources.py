from fastapi_admin.app import app
from fastapi_admin.resources import Link, Model, ToolbarAction, Field
from fastapi_admin.widgets import inputs
from fastapi_admin.file_upload import FileUpload
import os

from starlette.requests import Request

from fastapi_admin.enums import Method
from fastapi_admin.i18n import _
from .models import BotSettings, BotAdmin, BanWords
from fastapi import Depends

from fastapi_admin.depends import get_resources
from fastapi_admin.template import templates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
upload = FileUpload(uploads_dir=os.path.join(BASE_DIR, "static", "uploads"))


@app.get("/")
async def home(
    request: Request,
    resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "dashboard.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Dashboard",
            "page_pre_title": "overview",
            "page_title": "Dashboard",
        },
    )


@app.register
class Home(Link):
    label = "Home"
    icon = "fas fa-home"
    url = "/admin"


@app.register
class BotSettingsResource(Model):
    label = "Настройки бота"
    model = BotSettings
    page_title = "Настройки бота"

    async def get_toolbar_actions(self, request: Request) -> list[ToolbarAction]:
        return [
            ToolbarAction(
                label=_("create"),
                icon="fas fa-plus",
                name="create",
                method=Method.GET,
                ajax=False,
                class_="btn-dark",
            ),
            ToolbarAction(
                label=_("import"),
                icon="fas fa-plus",
                name="import",
                method=Method.GET,
                ajax=False,
                class_="btn-success",
            ),
        ]


@app.register
class BotAdminResource(Model):
    label = "Админы"
    model = BotAdmin
    page_title = "Админы"
    fields = [
        "telegram_id",
        "username",
        "fullname",
    ]
