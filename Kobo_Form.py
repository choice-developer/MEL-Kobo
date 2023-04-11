# A Kobo Toolbox xls form
import copy
import json
import requests
import time

# Using Kobo api v2
API = 'https://kobo.humanitarianresponse.info/api/v2/'
# Kobo Toolbox api token
TOKEN = '4bf304fdf1a88abdbff91d99977376ab9eb0c353'
HEADERS = {'Authorization': f'Token {TOKEN}'}
PARAMS = {'format': 'json'}


class Kobo_Form:

    def __init__(self, form_id, country_initials):
        self.form_id = form_id
        self.country_initials = country_initials
        # The url for the current form
        self.asset_url = f'{API}assets/{form_id}/'
        self.request = requests.get(url=self.asset_url, headers=HEADERS, params=PARAMS)
        # Why do we need the version ID?
        self.version = self.request.json()['version_id']
        self.content = copy.deepcopy(self.request.json()['content'])
        self.default_language = self.content['settings']['default_language']
        self.survey = self.content['survey']
        # These are the choices for the multi select questions
        self.choices = self.content['choices']

    # Remove previous list of projects, goals, and kpis to make room for the current set.
    def remove_old_choices(self):

        print('Removing old choices')
        for i, choice in enumerate(self.choices[:]):
            if choice['list_name'] == 'projects':
                self.choices.remove(choice)
            elif choice['list_name'] == 'goals':
                self.choices.remove(choice)
            elif choice['list_name'] == 'kpis':
                self.choices.remove(choice)

    # Add new choices
    def add_projects(self, projects):

        print('Adding projects')
        # Filter the projects by country initials
        filtered_projects = [project for project in projects if
                             project.project_number.startswith(self.country_initials)]

        # Keep track of project numbers that have already been encountered
        encountered_project_numbers = set()
        for project in filtered_projects:

            # Skip test projects
            if project.for_testing == 'Yes':
                continue
            # Skip project if its project number has already been encountered
            if project.project_number in encountered_project_numbers:
                continue
            else:
                encountered_project_numbers.add(project.project_number)

            spanish_name = project.project_number + '-' + project.project_name_es
            english_name = project.project_number + '-' + project.project_name_en

            if 'English' in self.default_language:
                label = [english_name, spanish_name]
            else:
                label = [spanish_name, english_name]

            self.choices.append({'name': project.project_number, 'label': label, 'list_name': 'projects'})

    def add_goals_and_kpis(self, mel_list):
        print('Adding Goals')
        goals = {}
        kpis = {}
        for measure in mel_list:
            if measure.goal_id not in goals:
                goals[measure.goal_id] = measure.goal_name
            if measure.kpi_id not in kpis:
                kpis[measure.kpi_id] = measure.kpi_name

        for goal_id, goal in goals.items():
            self.choices.append({'name': goal_id, 'label': [goal_id + ' ' + goal, goal_id + ' ' + goal],
                                 'list_name': 'goals'})

        for kpi_id, kpi in kpis.items():
            self.choices.append({'name': kpi_id, 'label': [kpi_id + ' ' + kpi, kpi_id + ' ' + kpi],
                                 'list_name': 'kpis', 'goal': kpi_id[:5]})

    def patch_new_choices(self):

        print('Patching new choices')
        patch = requests.patch(url=self.asset_url, headers=HEADERS, params=PARAMS,
                               data={'content': json.dumps(self.content)})

        if patch.status_code == 200:
            print(f'Successfully replaced Kobo xls form with status code {patch.status_code}')
        else:
            print(f'Failed to replace Kobo xls form with status code {patch.status_code}')

    def deploy_new_form(self):

        """Need to re-get the assets after the new form was patched."""
        deploy = requests.get(self.asset_url, headers=HEADERS, params=PARAMS)
        """Need to get the new version that includes the changes from the patch function"""
        self.version = deploy.json()['version_id']

        time.sleep(5)
        deploy = requests.patch(self.asset_url + 'deployment/', headers=HEADERS,
                                data={'version_id': self.version})

        if deploy.status_code == 200:
            print(f'Deployed with status code {deploy.status_code}')
        else:
            print(f'Failed to deploy with status code {deploy.status_code}')
