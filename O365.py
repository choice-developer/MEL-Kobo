# Handles all Office 365 operations
from shareplum import Office365, Site


def login(url, username='flowbot@choicehumanitarian.org', password='IShouldBeHashed19!'):
    auth = Office365(share_point_site='https://choicems.sharepoint.com',
                     username=username, password=password).GetCookies()
    site = Site(site_url=url, authcookie=auth)


