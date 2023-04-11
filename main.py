import KPI
import O365
import Project
import Kobo_Form

# Sites containing the relevant lists
project_site = 'https://choicems.sharepoint.com/sites/chprojects/'
kpi_site = 'https://choicems.sharepoint.com/sites/MeasurementEvaluation/'

# Raw data from sharepoint
project_list = O365.login(url=project_site, list_name='Projects')
request_list = O365.login(url=project_site, list_name='Project Requests')
kpi_list = O365.login(url=kpi_site, list_name='MEL LIST')

# List of objects
p_list = []
k_list = []

# Fill list with Projects
for project in project_list:
    if 'ProjectNumber' not in project:
        continue
    new_project = Project.Project(project)
    p_list.append(new_project)

# Add requests to the project list
for request in request_list:
    if 'RequestNumber' not in request:
        continue
    new_project = Project.Project(request)
    p_list.append(new_project)

# Fill list with KPI's
for kpi in kpi_list:
    new_kpi = KPI.KPI(new_kpi)
    k_list.append(new_kpi)


sorted_projects = sorted(p_list, key=lambda x: x.project_number)
# Country Kobo forms ---------------------------------------------------------------------------------------------------
master = Kobo_Form.Kobo_Form(form_id='aSRZnHY3HetTW6aebkNcWR', country_initials='')

