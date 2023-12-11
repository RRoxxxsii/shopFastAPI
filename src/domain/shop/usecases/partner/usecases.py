from src.domain.shop.dto.auth import UserDTO
from src.domain.shop.dto.item import ItemDTO
from src.domain.shop.dto.partner import PartnerDTO, UserPartnerDTO
from src.domain.shop.exceptions.category import CategoryDoesNotExist, CategoryDataDoesNotMatch
from src.domain.shop.exceptions.item import ItemExists
from src.domain.shop.exceptions.partner import DataNotValid, PartnerExists
from src.domain.shop.exceptions.user import UserExists
from src.domain.shop.usecases.base import BaseExtendedUseCase
from src.domain.shop.usecases.partner.base import PartnerUseCase
from src.infrastructure.database.models.item import Item
from src.infrastructure.database.models.partner import Partner
from src.infrastructure.secure.pwd import hash_password


class CreatePartnerUserDoesNotExists(PartnerUseCase):
    async def __call__(self, partner_dto: PartnerDTO, user_dto: UserDTO) -> Partner:
        async with self.uow:
            if await self.uow.user_repo.get_user_or_none(user_dto.email):
                raise UserExists("User with this credentials already exists")
            if await self.uow.partner_repo.get_partner_or_none(partner_dto):
                raise PartnerExists("Partner with this credentials already exists")
            if not await self.api_client.call(partner_dto):
                raise DataNotValid("Data you provided is not valid")
            user = await self.uow.user_repo.create(
                hashed_password=hash_password(user_dto.password1),
                **user_dto.model_dump(
                    include={"name", "surname", "email"},
                )
            )
            partner = await self.uow.partner_repo.create(user_id=user.id, **partner_dto.model_dump())
            await self.uow.commit()
            return partner


class CreatePartnerUserExists(PartnerUseCase):
    async def __call__(self, dto: UserPartnerDTO) -> Partner:
        async with self.uow:
            if await self.uow.partner_repo.get_partner_or_none(dto):
                raise PartnerExists("Partner with this credentials already exists")
            if not await self.api_client.call(dto):
                raise DataNotValid("Data you provided is not valid")
            partner = await self.uow.partner_repo.create(**dto.model_dump())
            await self.uow.commit()
            return partner


class CreateItem(BaseExtendedUseCase):

    async def __call__(self, dto: ItemDTO) -> Item:
        async with self.uow:
            item = await self.uow.item_repo.get_item_or_none(dto)
            if item:
                raise ItemExists('Item with a field from your request already exists')
            category = await self.uow.category_repo.get_by_id(pk=dto.category_id)
            if not category:
                raise CategoryDoesNotExist('Can not find is not valid')
            if category.data.keys() == dto.data.keys():
                item = await self.uow.item_repo.create(**dto.model_dump())
            else:
                raise CategoryDataDoesNotMatch('Data from your input does not match the category')
            await self.uow.commit()
            return item
