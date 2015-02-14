import os
import webapp2
import jinja2

from handlers.base import AppHandler
from google.appengine.ext import db

#template_dir= os.path.join(os.path.dirname(__file__), 'templates')
#jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
#                             autoescape=True)

class Art(db.Model):
    title=db.StringProperty(required=True)
    art=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)

class AsciiMainPage(AppHandler):
    def render_front(self,title="",art="",error=""):
        arts=db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("front.html",title=title,art=art,error=error,arts=arts)
    
    def get(self):
        self.render_front()
        #self.write("asciichan!!")
        #items=self.request.get_all("food")
        
    
    def post(self):
        title=self.request.get("title")
        art=self.request.get("art")
        
        if title and art :
           a=Art(title=title,art=art)
           a.put()
           self.redirect('/asciichan')
        else:
           error="we need both a title and an artwork"
           self.render_front(title,art,error=error)
   
