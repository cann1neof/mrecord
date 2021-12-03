from django.urls import path
from .views.view_auth import Authorization, StartAuthSession
from .views.view_octopus import (
    OctopusModerator,
    OctopusRecord,
    OctopusDoctor,
    OctopusRecordDoctor,
    OctopusRecordAmbulance,
    OctopusChild,
    RecordOctopus
)
from .views.view_creator import Creator
from .views.view_disease import Disease
from .views.view_edit import Editor, ChildEditor
from .views.view_reg import Registration
from .views.view_doctor import DoctorApi
from .views.view_migration import ChildMigration, StartChildMigration
from .views.view_newpartner import NewPartner

app_name = "records"

urlpatterns = [
    path('startauthsession/', StartAuthSession.as_view(), name="StartAuthSession"),
    path('authorize/', Authorization.as_view(), name="Authorization"),
    path('octopus/<str:token>/m/', OctopusModerator.as_view(), name="OctopusM"),
    path('octopus/<str:token>/r/', OctopusRecord.as_view(), name="OctopusR"),
    path('octopus/<str:token>/d/', OctopusDoctor.as_view(), name="OctopusD"),
    path('octopus/<str:token>/rd/', OctopusRecordDoctor.as_view(), name="OctopusRD"),
    path('octopus/<str:token>/ra/', OctopusRecordAmbulance.as_view(), name="OctopusRA"),
    path('octopus/<str:token>/c/', OctopusChild.as_view(), name="OctopusC"),
    path('octopus/getrecord/', RecordOctopus.as_view(), name="OctopusRecordCodes"),
    path('register/', Registration.as_view(), name="Registration"),
    path('editor/', Editor.as_view(), name="Editor"),
    path('editor/child/', ChildEditor.as_view(), name='ChildEditor'),
    path('disease/<str:disease>/', Disease.as_view(), name='DiseaseGetter'),
    path('creator/<str:meta>/', Creator.as_view(), name="TheCreator"),
    path('doctor/', DoctorApi.as_view(), name="DoctorApi"),
    path('startmigrationsession/', StartChildMigration.as_view(), name="StartChildMigration"),
    path('migrate/', ChildMigration.as_view(), name="ChildMigration"),
    path('newpartner/', NewPartner.as_view(), name="NewPartnerForm"),
]
