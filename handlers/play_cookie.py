import os
import webapp2
import jinja2

from handlers.base import AppHandler
from google.appengine.ext import db

# class Handler(webapp2.RequestHandler):
#     def write(self, *a, **kw):
#         self.response.write(*a, **kw)
    
#     def render_str(self,template, **params):
#         t=jinja_env.get_template(template)
#         return t.render(params)
        
#     def render(self,template,**kw):
#         self.write(self.render_str(template, **kw))

# class Blogs(db.Model):
#  	subject=db.StringProperty(required=True)
#  	content=db.TextProperty(required=True)
#  	created=db.DateTimeProperty(auto_now_add=True)
   
	
class PCMainPage(AppHandler):
   
    def render_front(self,subject="",art="",error=""):
         blogs=db.GqlQuery("SELECT * FROM Blogs ORDER BY created DESC")
         self.render("blogfront.html",blogs=blogs)
    
    def get(self):
        #db.delete(Blogs.all())

        self.render_front()
    	#self.write("asciichan!!")
    	#items=self.request.get_all("food")
        

# class BlogNewPost(AppHandler):
#     def render_front(self,subject="",error=""):
#         self.render("newblogfront.html",subject=subject,error=error)#,subject=subject,art=art,error=error,arts=arts)
   
#     def get(self):
#         self.render("newblogfront.html")
	
#     def post(self):
#         subject=self.request.get("subject")
#     	content=self.request.get("content")
    	
#     	if subject and content :
#     	   a=Blogs(subject=subject,content=content)
#     	   key=a.put()
#            new_id=key.id()
#     	   self.redirect_to('blog_single', blog_id=new_id)
#     	else:
#     	   error="we need both a subject and the content"
#     	   self.render_front(subject,error=error)

# class GetBlogWithID(AppHandler):
#     def get_blog(self,blog_id):
#         eid = int(blog_id) if blog_id.isdigit() else 0

#         key = db.Key.from_path('Blogs', eid)
#         blog = Blogs.get(key)
#         #blogs=db.GqlQuery("SELECT * FROM Blogs where __key__ = KEY('Blogs', blog_id)")
#         self.render('blog_single.html', blog=blog)


        
        
# application = webapp2.WSGIApplication([
#     ('/blog', BlogMainPage),
#     ('/blog/newpost', BlogNewPost),
#     (r'/blog/(\d+)',GetBlogWithID)
# ], debug=True)