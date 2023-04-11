import KPI
import O365
import Project
import Kobo_Form

# Sites containing the relevant lists
project_site = 'https://choicems.sharepoint.com/sites/chprojects/'
kpi_site = 'https://choicems.sharepoint.com/sites/MeasurementEvaluation/'

# Raw data from sharepoint
print('Getting Projects list')
project_list = O365.login(url=project_site, list_name='Projects')
print('Getting Project Requests list')
request_list = O365.login(url=project_site, list_name='Project Requests')
print('Getting MEL LIST')
kpi_list = O365.login(url=kpi_site, list_name='MEL LIST')

# List of objects
p_list = []
k_list = []

# Fill list with Projects
print('Filling list with Projects')
for project in project_list:
    if 'ProjectNumber' not in project:
        continue
    new_project = Project.Project(project)
    p_list.append(new_project)

# Add requests to the project list
print('Filling list with Requests')
for request in request_list:
    if 'RequestNumber' not in request:
        continue
    new_project = Project.Project(request)
    p_list.append(new_project)

# Fill list with KPI's
print("Filling list with KPI's")
for kpi in kpi_list:
    new_kpi = KPI.KPI(kpi)
    k_list.append(new_kpi)

print('Sorting projects')
sorted_projects = sorted(p_list, key=lambda x: x.project_number, reverse=True)
# Country Kobo forms ---------------------------------------------------------------------------------------------------
countries = []
master = {'form_id': 'aSRZnHY3HetTW6aebkNcWR', 'country_initials': 'BO'}
countries.append(master)
bolivia = {'form_id': 'aQ9dbQp39aifjsdGAT2nzw', 'country_initials': 'BO'}
countries.append(bolivia)
ecuador = {'form_id': 'aHk7b4jAy25B9oJZ4xmtNV', 'country_initials': 'EC'}
countries.append(ecuador)
guatemala = {'form_id': 'aKYhWCXVCLrCUSnhZC9WrE', 'country_initials': 'GT'}
countries.append(guatemala)
kenya = {'form_id': 'aCBfp4doT8NCnB2rhr3JVj', 'country_initials': 'KE'}
countries.append(kenya)
mexico = {'form_id': 'aAoCzjyX6Q8SfhR5FstrgS', 'country_initials': 'MX'}
countries.append(mexico)
nepal = {'form_id': 'aEAdZTnffjhYqiSgkXotU3', 'country_initials': 'NP'}
countries.append(nepal)
navajo = {'form_id': 'aGzHbMRVGkFY6uNgp27UBT', 'country_initials': 'NV'}
countries.append(navajo)
peru = {'form_id': 'aScuYamPgmcPbWENwAoJgF', 'country_initials': 'PE'}
countries.append(peru)

for country in countries:
    print(f'Country: {country["country_initials"]}')
    new_form = Kobo_Form.Kobo_Form(form_id=country['form_id'], country_initials=country['country_initials'])
    new_form.remove_old_choices()
    new_form.add_projects(projects=sorted_projects)
    new_form.add_goals_and_kpis(mel_list=k_list)
    new_form.patch_new_choices()
    new_form.deploy_new_form()

