import os
import webapp2
import jinja2
import urllib2

from handlers.base import AppHandler
from google.appengine.ext import db

#template_dir= os.path.join(os.path.dirname(__file__), 'templates')
#jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
#                             autoescape=True)

# class Art(db.Model):
#     title=db.StringProperty(required=True)
#     art=db.TextProperty(required=True)
#     created=db.DateTimeProperty(auto_now_add=True)

class MFdb(db.Model):
	scheme_code = db.StringProperty(required = True)
	scheme_name = db.StringProperty(required = True)
	nav = db.StringProperty(required = True)
	repurchase_price = db.StringProperty(required = True)
	sale_price = db.StringProperty(required = True)
	date = db.StringProperty(required = True)
	sponsor = db.StringProperty(required = True)
	scheme_type = db.StringProperty(required = True)

class IndexPage(AppHandler):
    def get(self):
        code=self.request.get("code")
        if code:
          nav=db.GqlQuery("SELECT * FROM MFdb WHERE scheme_code = :c",c=code).get()
          self.render("mf_nav_front.html",code=code,nav=nav)
        else:
          self.render("mf_nav_front.html",code='',nav='')
        #self.response.write(nav)


class DataPopulatePage(AppHandler):
    def get(self):
        response_local=urllib2.urlopen('http://portal.amfiindia.com/spages/NAV0.txt')
        text=response_local.read()
        rows=text.split('\n')
        sponsor=''
       	scheme_type=''
       	i=1
       	while i<len(rows):
       		row=rows[i]
       		if row.find(';')!=-1:
       			data=row.split(";")
       			code=data[0]
       			name=data[3]
       			nav=data[4]
       			repurchase=data[5]
       			sale=data[6]
       			date=data[7]
       			a=MFdb(scheme_code=code,scheme_name=name,nav=nav,repurchase_price=repurchase,sale_price=sale,date=date,sponsor=sponsor,scheme_type=scheme_type)
        		a.put()
        	elif row.find("Mutual Fund")!=-1:
        		sponsor=row
        	elif len(row)>5:
        		scheme_type=row
        	i=i+1
        	
        #items=self.request.get_all("food")
        
    
    # def post(self):
    #     title=self.request.get("title")
    #     art=self.request.get("art")
        
    #     if title and art :
    #        a=Art(title=title,art=art)
    #        a.put()
    #        self.redirect('/asciichan')
    #     else:
    #        error="we need both a title and an artwork"
    #        self.render_front(title,art,error=error)