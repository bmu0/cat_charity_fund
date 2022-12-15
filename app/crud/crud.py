from app.crud.base import CRUDBase
from app.models import CharityProject, Donation


class CRUDCharityProject(CRUDBase):
    pass


class CRUDDonation(CRUDBase):
    pass


charity_project_crud = CRUDCharityProject(CharityProject)
donation_crud = CRUDDonation(Donation)