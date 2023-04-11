# A Kobo Toolbox xls form
import requests, copy, json

# Using Kobo api v2
API = 'https://kf.kobotoolbox.org/api/v2/'
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
        self.request = requests.get(url=API, headers=HEADERS, params=PARAMS)
        # Why do we need the version ID?
        self.version = self.request.json()['version_id']
        self.content = copy.deepcopy(self.request.json()['content'])
        self.default_language = self.content['settings']['default_language']
        # These are the choices for the multi select questions
        self.choices = self.content['choices']

    # Remove previous list of projects, goals, and kpis to make room for the current set.
    def remove_old_choices(self):

        for i, choice in enumerate(self.choices[:]):
            if choice['list_name'] == 'projects':
                self.choices.remove(choice)
            elif choice['list_name'] == 'goals':
                self.choices.remove(choice)
            elif choice['list_name'] == 'kpis':
                self.choices.remove(choice)

    # Add new choices
    def add_projects(self, projects):

        # Filter the projects by country initials
        filtered_projects = [project for project in projects if
                             project.project_number.startswith(self.country_initials)]

        for project in filtered_projects:

            # Skip test projects
            if project.for_testing == 'Yes':
                continue

            spanish_name = project.project_number + '-' + project.project_name_es
            english_name = project.project_number + '-' + project.project_name_en

            if 'English' in self.default_language:
                label = [english_name, spanish_name]
            else:
                label = [spanish_name, english_name]

            self.choices.append({'name': project.project_number, 'label': label, 'list_name': 'projects'})

    def patch_new_choices(self):

        patch = requests.patch(url=self.asset_url, headers=HEADERS, params=PARAMS,
                               data={'content': json.dumps(self.content)})

        if patch.status_code == 200:
            print(f'Successfully replaced Kobo xls form with status code {patch.status_code}')
        else:
            print(f'Failed to replace Kobo xls form with status code {patch.status_code}')
