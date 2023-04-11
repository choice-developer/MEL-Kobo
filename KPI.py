# A KPI from the MEL SharePoint list


class KPI:

    def __init__(self, kpi):
        self.measure_name = kpi['Title']
        self.measure_id = kpi['Measure_ID']
        self.kpi_name = kpi['KPI']
        self.kpi_id = kpi['KPI_Id']
        self.goal_name = kpi['Goal']
        self.goal_id = kpi['Goal_Id']
        self.area_name = kpi['Area']
        self.area_id = kpi['Area_Id']


