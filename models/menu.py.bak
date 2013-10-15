# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="brand",_href="http://www.web2py.com/")
#response.title = ' '.join(
 #   word.capitalize() for word in request.application.split('_'))
response.title = 'Resume Builder'
#response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (SPAN('Home', _class='highlighted'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    r=db(auth.user_id == db.auth_membership.user_id).select(db.auth_membership.group_id)
    # useful links to internal and external resources
    if len(r) == 0:
        return
    elif r[0]['group_id'] == 1:
        response.menu += [
            (T('View Messages'), False, URL(app, 'default', 'view_msg')),
            (T('Update Profile'), False, URL(app, 'default', 'edit_student')),
            (T('Add a project'), False, URL(app, 'default', 'add_project')),
            (T('Get PDF!'), False, URL(app, 'default', 'pdf1')),
            (T('Add an Achievement'),False, URL(app, 'default', 'add_achievement')),
             ]
    elif r[0]['group_id'] == 2:
         response.menu += [
            (T('Send Message'), False, URL(app, 'default', 'send_msg')),
            (T('Update Profile'), False, URL(app, 'default', 'edit_organisation')),
            (T('Add Vacancies'), False, URL(app, 'default', 'add_vacancies')),
            (T('Search'), False, URL(app, 'default', 'search')),
             ]
if DEVELOPMENT_MENU: _()
