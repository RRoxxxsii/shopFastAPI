from sqladmin import ModelView

from src.infrastructure.database.models.partner import Partner


class PartnerAdmin(ModelView, model=Partner):
    column_list = [
        Partner.id,
        Partner.user,
        Partner.user_id,
        Partner.mobile,
        Partner.company_name,
        Partner.company_description,
        Partner.time_created,
        Partner.additional,
        Partner.is_approved
    ]
