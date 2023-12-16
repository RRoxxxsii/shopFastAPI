from sqladmin import Admin

from src.infrastructure.admin.models.item import CategoryAdmin, ItemAdmin
from src.infrastructure.admin.models.partner import PartnerAdmin
from src.infrastructure.admin.models.user import UserAdmin, TokenAdmin


def setup_admin_models(admin_app: Admin):
    for app in [UserAdmin, PartnerAdmin, CategoryAdmin, ItemAdmin, TokenAdmin]:
        admin_app.add_view(app)
