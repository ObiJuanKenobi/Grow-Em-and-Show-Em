from django.contrib.admin import AdminSite
from pga import models

class PGAAdminSite(AdminSite):
    site_header = 'Prison Garden Application Administration'

admin_site = PGAAdminSite(name='pgaadmin')