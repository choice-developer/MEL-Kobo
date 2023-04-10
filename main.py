import O365
import Project

project_site = 'https://choicems.sharepoint.com/sites/chprojects/'
kpi_site = 'https://choicems.sharepoint.com/sites/MeasurementEvaluation/'
project_list = O365.login(url=project_site, list_name='Projects')
kpi_list = O365.login(url=kpi_site, list_name='MEL LIST')
p_list = []
k_list = []
for project in project_list:
    new_project = Project.Project(project_number=project['ProjectNumber'], project_name=project['Project Name'])
    p_list.append(new_project)
for project in p_list:
    print(project)