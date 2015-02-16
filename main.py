import os
import webapp2
import jinja2


from webapp2 import WSGIApplication, Route

root_dir = os.path.dirname(__file__)
template_dir = os.path.join(root_dir, 'templates')
  
application = webapp2.WSGIApplication([
    Route(r'/asciichan', handler='handlers.asciichan.AsciiMainPage', name='fs'),
    Route(r'/blog/newpost', handler='handlers.blog.BlogNewPost', name='bnp'),
    Route(r'/blog', handler='handlers.blog.BlogMainPage', name='bmp'),
    Route(r'/blog/<blog_id:\d+>', handler='handlers.blog.GetBlogWithID',
            name='blog_single', handler_method='get_blog'),
    Route(r'/playcookie', handler='handlers.play_cookie.PCMainPage', name='fs'),
], debug=True)