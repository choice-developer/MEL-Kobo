# A project from the Projects SharePoint list


class Project:
    def __init__(self, project):
        if 'ProjectNumber' in project:
            self.project_number = project['ProjectNumber']
        elif 'RequestNumber' in project:
            self.project_number = project['RequestNumber']
        self.project_name = project['Project Name']
        self.project_name_en = project['project_name_en']
        self.project_name_es = project['project_name_es']
        self.for_testing = project['ForTesting']
