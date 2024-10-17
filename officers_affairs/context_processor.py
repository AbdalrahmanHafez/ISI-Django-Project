from django.core.handlers.wsgi import WSGIRequest
from .forms import BranchForm,  JobForm, OffUnitStatusForm, OfficerStatusForm,RankForm, SectionForm, UnitForm, WeaponForm

def sidebarforms(request: WSGIRequest) -> dict:
    return {
        'formweapon':WeaponForm(),
        'formunit':UnitForm(),
        'formbranch':BranchForm(),
        'formsection':SectionForm(),
        'formjob':JobForm(),
        'formrank':RankForm(),
        'formoffunitstat':OffUnitStatusForm(),
        'formoffstat':OfficerStatusForm(),
    }