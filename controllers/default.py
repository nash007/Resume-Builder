# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
#@auth.requires_verify_email()
def index():
    r=db(auth.user_id == db.auth_membership.user_id).select(db.auth_membership.group_id)
    s=db(auth.user_id == db.details.myid).select(db.details.myid)
    j=db(auth.user_id == db.organisation.myid).select(db.organisation.myid)
    t=db(auth.user_id == db.details.myid).select()
    n = len(s)
    m=len(j)
	#if auth.user_id == db.auth_membership.user_id and db.auth_membership.group_id == 1:
    if r[0]['group_id'] == 1 and n == 0:
        redirect(URL(add_student))
    elif r[0]['group_id'] == 1 and n!=0:
        return dict(message=T('Welcome to Resume Builder!!'),t=t)
    elif r[0]['group_id'] == 2 and m!=0:
#		return dict(message=T('Choose your students!'))
        redirect(URL(index1))
    elif r[0]['group_id'] == 2 and m == 0:
        redirect(URL(add_organisation))
    else:
		#return dict(message=T('Your account has not been activated yet!'))
        redirect(URL(index2))

@auth.requires_login()
def index1():
    return dict(message=T('Choose Your students!'))

@auth.requires_login()
def index2():
    return dict(message=T('Your account has not been activated by our admin yet!'))
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@auth.requires_login()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
    
@auth.requires_login()
@auth.requires_membership('Student')
def add_student():
    form = SQLFORM(db.details)			#use SQLFORM if you want to insert it as a record too. SQLFORM.factory won't insert. It just shows the form and uses it as a query.
    r=db(auth.user_id==db.auth_user.id).select(db.auth_user.first_name,db.auth_user.last_name)
    form.vars.name=r[0]['first_name']+' '+r[0]['last_name']
    form.vars.myid=auth.user_id
    form.vars.picture="photo.jpg"
    if form.accepts(request.vars,session):
	#redirect(URL(r=request, f='student_details?rollno=%d' % form.vars.rollno))
        #return dict(message=T('Welcome to Resume Builder!!'))
        redirect(URL(index))
	#redirect(URL(student_details))
    elif form.errors:
        response.flash='Errors in form'
    return dict(form=form)

@auth.requires_login()
@auth.requires_membership('Student')
def edit_student():
    #studentid = int(request.args(0)) # or int(request.vars.studentid)fpff
    r=db(auth.user_id==db.details.myid).select(db.details.id)
    myid=r[0]['id']
    form = SQLFORM(db.details, myid, showid=False, upload=URL('download'))
    r=db(auth.user_id==db.auth_user.id).select(db.auth_user.first_name,db.auth_user.last_name)
    form.vars.name=r[0]['first_name']+' '+r[0]['last_name']
    form.vars.picture="photo.jpg"
    if form.accepts(request.vars,session):
        #redirect(URL(r=request, f='student_details?rollno=%d' % form.vars.rollno))
        redirect(URL(index))
    elif form.errors:
        response.flash='Errors in form'
    return dict(form=form)
    
@auth.requires_login()    
@auth.requires_membership('Student')
def student_details():
	return dict(details = db(auth.user_id==db.details.myid).select(db.details.name, db.details.cg))

@auth.requires_login()
@auth.requires_membership('Organisation')
def send_msg():
    form=SQLFORM(db.msg)
    temp=db(auth.user_id == db.auth_user.id).select(db.auth_user.first_name, db.auth_user.last_name)
    company=temp[0]['first_name'] + ' ' + temp[0]['last_name']
    form.vars.sender=company
    form.vars.senderid=auth.user_id
    if form.accepts(request.vars,session):
        redirect(URL(index))
        session.flash='Message Successfully sent'
    #else:
     #   response.flash='Error in filling form!'
    return dict(form=form)

@auth.requires_login()
@auth.requires_membership('Student')
def view_msg():
    r=db((auth.user_id == db.details.myid) & (db.details.id == db.msg.name)).select(db.msg.senderid, db.msg.sender, db.msg.sub, db.msg.msg)
    print r
    dict_companies={}
    for i in r:
        if i.sender in dict_companies.keys():
            dict_companies[i.sender].append(i)
        else:
            dict_companies[i.sender]=[]
            dict_companies[i.sender].append(i)
    return dict(r=r,dict_companies=dict_companies)

@auth.requires_login()
@auth.requires_membership('Student')
def add_project():
    form=SQLFORM(db.project)
    form.vars.myid=auth.user_id
    if form.accepts(request.vars,session):
        redirect(URL(index))
    #else:
     #   response.flash='Error(s) in filling form'
    return dict(form=form)

@auth.requires_login()
@auth.requires_membership('Organisation')
def add_organisation():
    r=db(auth.user_id==db.auth_user.id).select(db.auth_user.first_name,db.auth_user.last_name)
    form=SQLFORM(db.organisation)
    form.vars.name=r[0]['first_name']+' '+r[0]['last_name']
    form.vars.myid=auth.user_id
    form.vars.logo="photo.jpg"
    if form.accepts(request.vars,session):
        redirect(URL(index))
    #else:
     #   response.flash='Error(s) in filling form'
    return dict(form=form)
    
@auth.requires_login()
@auth.requires_membership('Organisation')
def edit_organisation():
    r=db(auth.user_id==db.organisation.myid).select(db.organisation.id)
    myid=r[0]['id']
    form = SQLFORM(db.organisation, myid, showid=False, upload=URL('download'))
    r=db(auth.user_id==db.auth_user.id).select(db.auth_user.first_name,db.auth_user.last_name)
    form.vars.name=r[0]['first_name']+' '+r[0]['last_name']
    if form.accepts(request.vars,session):
        #redirect(URL(r=request, f='student_details?rollno=%d' % form.vars.rollno))
        redirect(URL(index))
    elif form.errors:
        response.flash='Errors in form'
    return dict(form=form)
    
@auth.requires_login()
@auth.requires_membership('Organisation')    
def add_vacancies():
    form=SQLFORM(db.vacancies)
    form.vars.myid=auth.user_id
    if form.accepts(request.vars,session):
        redirect(URL(index))
    #else:
     #   response.flash='Error(s) in filling form'
    return dict(form=form)
    
@auth.requires_login()
@auth.requires_membership('Organisation')
def search():
    db.details.name.readable=True
    db.details.myid.readable=False
    grid=SQLFORM.grid(db.details,left=db.project.on(db.project.myid == db.details.myid),sortable=True,deletable=False,create=False,editable=False,fields=[db.details.current_year,db.details.name,db.details.cg,db.details.college,db.details.myid],links=[lambda row:A('Download Resume',_href=URL('default','mypdf3',args=[row.myid]))],csv=False)
    #grid=SQLFORM.smartgrid(db.details,linked_tables=['project'],editable=False,create=False,deletable=False,fields=[db.details.current_year,db.details.name,db.details.cg,db.details.college,db.project.org])
    return dict(grid=grid)


@auth.requires_login()
@auth.requires_membership('Student')
def add_achievement():
    form=SQLFORM(db.achievements)
    form.vars.myid=auth.user_id
    if form.accepts(request.vars,session):
        redirect(URL(index))
    #else:
     #   response.flash='Error(s) in filling form'
    return dict(form=form)
    
def single_company_msg():
    raq=db((request.args(0)==db.msg.senderid) & (db.msg.name == auth.user_id)).select(db.msg.msg_date,db.msg.sub,db.msg.msg)
    #for msg in dict_companies[i]:
        #print 'hi!'
    return dict(r=raq)   
    
def mypdf():
    r=db(auth.user_id==db.details.myid).select()
    s=db(auth.user_id==db.project.myid).select()
    t=db(auth.user_id==db.achievements.myid).select()
    u=db(db.auth_user.id==auth.user_id).select(db.auth_user.email)
    from gluon.contrib.pyfpdf import FPDF, HTMLMixin
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font('Arial','BU',40)
    #pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
    pdf.set_text_color(100,0,100)
    pdf.cell(w=80,h=30,txt="Curriculum Vitae",ln=2,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,0)
    pdf.set_font('Arial','BU',30)
    pdf.set_text_color(0,0,100)
    pdf.cell(w=80,h=30,txt="Biodata",ln=1,border=2,align='L',fill='0')
    pdf.set_font('Arial','',15)
    pdf.set_text_color(0,0,0)
    pdf.cell(w=60,h=10,txt="Name  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].name,ln=1,border=2,align='L',fill='0')
    
    
    
    pdf.set_text_color(0,0,0)
    pdf.cell(w=60,h=10,txt="Current Year  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].current_year,border=2,ln=1,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="CGPA  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=str(r[0].cg),ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="College  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].college,border=2,ln=1,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="Branch  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].branch,border=2,ln=1,align='L',fill='0')
    
    pdf.set_text_color(0,0,0)  
     
    #pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_font('Arial','BU',30)
    pdf.set_text_color(0,0,100)
    if len(s) != 0:
        pdf.cell(w=60,h=10,txt="Projects/Interns    ",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="                                          ",ln=1,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,0)
    for i in s:
        pdf.set_font('Arial','BI',20)
        pdf.cell(w=60,h=10,txt=i.name,ln=1,border=2,align='L',fill='0')
        pdf.set_font('Arial','',15)
        pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="Mentor  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.mentor,ln=1,border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="Organistion  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.org,ln=1,border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="Description  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.Description,ln=1,border=2,align='L',fill='3')
        pdf.cell(w=60,h=10,txt="Skills Used  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.skills_used,ln=1,border=2,align='L',fill='3')
        pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
        #pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_font('Arial','BU',30)
    pdf.set_text_color(0,0,100)
    if len(s) != 0:
        pdf.cell(w=60,h=10,txt="Achievements    ",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="                                          ",ln=1,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,0)
    for i in t:
        pdf.set_font('Arial','',15)
        pdf.cell(w=60,h=10,txt=i.what,ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_font('Arial','BU',30)
    pdf.set_text_color(0,0,100)
    pdf.cell(w=60,h=10,txt="Contact Details",ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,0)
    pdf.set_font('Arial','',15)
    #pdf.cell(w=40,h=10,txt="Email  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=u[0].email,ln=1,border=2,align='L',fill='0')
    #pdf.cell(w=40,h=10,txt="Address  :",border=2,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
    if len(r[0].address)!=0:
        pdf.cell(w=60,h=10,txt=r[0].address+', ',border=2,ln=1,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=r[0].city+', '+r[0].cstate,border=2,ln=1,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt=r[0].cstate,border=2,ln=1,align='L',fill='0')
    response.headers['Content-Type']='application/pdf'
    return pdf.output(dest="S")
    
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
    
def mypdf1():
    r=db(auth.user_id==db.details.myid).select()
    s=db(auth.user_id==db.project.myid).select()
    t=db(auth.user_id==db.achievements.myid).select()
    u=db(db.auth_user.id==auth.user_id).select(db.auth_user.email)
    from gluon.contrib.pyfpdf import FPDF, HTMLMixin
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font('Arial','BU',40)
    pdf.set_text_color(0,0,0)
    pdf.cell(w=50,h=10,txt="",border=2,align='L',fill='0')
    pdf.set_font('Arial','BU',40)
    pdf.set_text_color(0,0,100)
    pdf.cell(w=80,h=30,txt=r[0].name,ln=1,border=2,align='C',fill='0')
    pdf.set_font('Arial','',10)
    pdf.set_text_color(0,0,0)
    pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=u[0].email,ln=1,border=2,align='C',fill='0')
    pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].address+', '+r[0].city+', '+r[0].cstate,ln=1,border=2,align='C',fill='0')
    pdf.set_text_color(0,0,100)
    pdf.set_font('Arial','BU',30)
    pdf.cell(w=60,h=10,txt="Education    ",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="                                          ",ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,0)
    pdf.set_font('Arial','',15)
    pdf.cell(w=20,h=10,txt="",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="Current Year  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].current_year,border=2,ln=1,align='L',fill='0')
    pdf.cell(w=20,h=10,txt="",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="CGPA  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=str(r[0].cg),ln=1,border=2,align='L',fill='0')
    pdf.cell(w=20,h=10,txt="",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="College  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].college,border=2,ln=1,align='L',fill='0')
    pdf.cell(w=20,h=10,txt="",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="Branch  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].branch,border=2,align='L',fill='0')
    
    pdf.set_text_color(0,0,0)  
     
    pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,100)
    pdf.set_font('Arial','BU',30)
    if len(s) != 0:
        pdf.cell(w=60,h=10,txt="Projects/Interns    ",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="                                          ",ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,0)
    for i in s:
        pdf.set_font('Arial','BI',20)
        pdf.cell(w=60,h=10,txt=i.name.capitalize(),ln=1,border=2,align='L',fill='0')
        pdf.set_font('Arial','',15)
        pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
        pdf.cell(w=20,h=10,txt="",border=2,align='L',fill='0')
        pdf.cell(w=40,h=10,txt="Mentor  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.mentor,ln=1,border=2,align='L',fill='0')
        pdf.cell(w=20,h=10,txt="",border=2,align='L',fill='0')
        pdf.cell(w=40,h=10,txt="Organistion  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.org,ln=1,border=2,align='L',fill='0')
        pdf.cell(w=20,h=10,txt="",border=2,align='L',fill='0')
        pdf.cell(w=40,h=10,txt="Description  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.Description,ln=1,border=2,align='L',fill='3')
        pdf.cell(w=20,h=10,txt="",border=2,align='L',fill='0')
        pdf.cell(w=40,h=10,txt="Skills Used  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.skills_used,ln=1,border=2,align='L',fill='3')
        pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_font('Arial','BU',30)
    pdf.set_text_color(0,0,100)
    pdf.set_font('Arial','BU',30)
    if len(s) != 0:
        pdf.cell(w=60,h=10,txt="Achievements    ",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="                                          ",ln=1,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,0)
    for i in t:
        pdf.set_font('Arial','',15)
        pdf.cell(w=60,h=10,txt="               "+i.what,ln=1,border=2,align='L',fill='0')

    response.headers['Content-Type']='application/pdf'
    return pdf.output(dest="S")


def pdf1():
    r=db(auth.user_id==db.details.myid).select()
    return dict(r=r)

@auth.requires_login()
@auth.requires_membership('Organisation')
def mypdf3():
    
    r=db(request.args[0]==db.details.myid).select()
    s=db(request.args[0]==db.project.myid).select()
    t=db(request.args[0]==db.achievements.myid).select()
    u=db(db.auth_user.id==request.args[0]).select(db.auth_user.email)
    from gluon.contrib.pyfpdf import FPDF, HTMLMixin
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font('Arial','BU',40)
    #pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
    pdf.set_text_color(100,0,100)
    pdf.cell(w=80,h=30,txt="Curriculum Vitae",ln=2,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,0)
    pdf.set_font('Arial','BU',30)
    pdf.set_text_color(0,0,100)
    pdf.cell(w=80,h=30,txt="Biodata",ln=1,border=2,align='L',fill='0')
    pdf.set_font('Arial','',15)
    pdf.set_text_color(0,0,0)
    pdf.cell(w=60,h=10,txt="Name  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].name,ln=1,border=2,align='L',fill='0')
    
    
    
    pdf.set_text_color(0,0,0)
    pdf.cell(w=60,h=10,txt="Current Year  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].current_year,border=2,ln=1,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="CGPA  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=str(r[0].cg),ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="College  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].college,border=2,ln=1,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="Branch  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].branch,border=2,ln=1,align='L',fill='0')
    
    pdf.set_text_color(0,0,0)  
     
    #pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_font('Arial','BU',30)
    pdf.set_text_color(0,0,100)
    if len(s) != 0:
        pdf.cell(w=60,h=10,txt="Projects/Interns    ",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="                                          ",ln=1,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,0)
    for i in s:
        pdf.set_font('Arial','BI',20)
        pdf.cell(w=60,h=10,txt=i.name,ln=1,border=2,align='L',fill='0')
        pdf.set_font('Arial','',15)
        pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="Mentor  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.mentor,ln=1,border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="Organistion  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.org,ln=1,border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="Description  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.Description,ln=1,border=2,align='L',fill='3')
        pdf.cell(w=60,h=10,txt="Skills Used  :",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt=i.skills_used,ln=1,border=2,align='L',fill='3')
        pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
        #pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_font('Arial','BU',30)
    pdf.set_text_color(0,0,100)
    if len(s) != 0:
        pdf.cell(w=60,h=10,txt="Achievements    ",border=2,align='L',fill='0')
        pdf.cell(w=60,h=10,txt="                                          ",ln=1,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,0)
    for i in t:
        pdf.set_font('Arial','',15)
        pdf.cell(w=60,h=10,txt=i.what,ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_font('Arial','BU',30)
    pdf.set_text_color(0,0,100)
    pdf.cell(w=60,h=10,txt="Contact Details",ln=1,border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt="",ln=1,border=2,align='L',fill='0')
    pdf.set_text_color(0,0,0)
    pdf.set_font('Arial','',15)
    #pdf.cell(w=40,h=10,txt="Email  :",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=u[0].email,ln=1,border=2,align='L',fill='0')
    #pdf.cell(w=40,h=10,txt="Address  :",border=2,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].address+', ',border=2,ln=1,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
    pdf.cell(w=60,h=10,txt=r[0].city+', '+r[0].cstate,border=2,ln=1,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt="",border=2,align='L',fill='0')
    #pdf.cell(w=60,h=10,txt=r[0].cstate,border=2,ln=1,align='L',fill='0')
  
    response.headers['Content-Type']='application/pdf'
    return pdf.output(dest="S")
