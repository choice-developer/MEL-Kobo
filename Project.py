# A project from the Projects SharePoint list


class Project:
    def __init__(self, project):
        if 'ProjectNumber' in project:
            self.project_number = project['ProjectNumber']
        elif 'RequestNumber' in project:
            self.project_number = project['RequestNumber']
        self.project_name = project['Project Name']
        if 'project_name_en' in project:
            self.project_name_en = project['project_name_en']
        else:
            self.project_name_en = project['Project Name']
        if 'project_name_es' in project:
            self.project_name_es = project['project_name_es']
        else:
            self.project_name_es = project['Project Name']
        if 'ForTesting' in project:
            self.for_testing = project['ForTesting']
        else:
            self.for_testing = '-'
