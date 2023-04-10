import O365

project_site = 'https://choicems.sharepoint.com/sites/chprojects/'
kpi_site = 'https://choicems.sharepoint.com/sites/MeasurementEvaluation/'
O365.login(url=project_site)
O365.login(url=kpi_site)