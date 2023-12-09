from src.domain.shop.dto.auth import CreateUserDTO
from src.domain.shop.dto.partner import PartnerDTO, UserPartnerDTO
from src.domain.shop.exceptions.partner import DataNotValid, PartnerExists
from src.domain.shop.exceptions.user import UserExists
from src.domain.shop.usecases.partner.base import PartnerUseCase
from src.infrastructure.database.models.partner import Partner
from src.infrastructure.secure.pwd import hash_password


class CreatePartnerUserDoesNotExists(PartnerUseCase):

    async def __call__(self, partner_dto: PartnerDTO, user_dto: CreateUserDTO) -> Partner:
        async with self.uow:
            if await self.uow.user_repo.get_user_or_none(user_dto.email):
                raise UserExists('User with this credentials already exists')
            if await self.uow.partner_repo.get_partner_or_none(partner_dto):
                raise PartnerExists('Partner with this credentials already exists')
            if not await self.api_client.call(partner_dto):
                raise DataNotValid('Data you provided is not valid')
            user = await self.uow.user_repo.create(
                hashed_password=hash_password(user_dto.password1), **user_dto.model_dump(
                    include={'name', 'surname', 'email'},
                )
            )
            partner = await self.uow.partner_repo.create(user_id=user.id, **partner_dto.model_dump())
            await self.uow.commit()
            return partner


class CreatePartnerUserExists(PartnerUseCase):

    async def __call__(self, dto: UserPartnerDTO) -> Partner:
        async with self.uow:
            if await self.uow.partner_repo.get_partner_or_none(dto):
                raise PartnerExists('Partner with this credentials already exists')
            if not await self.api_client.call(dto):
                raise DataNotValid('Data you provided is not valid')
            partner = await self.uow.partner_repo.create(**dto.model_dump())
            await self.uow.commit()
            return partner
