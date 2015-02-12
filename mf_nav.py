import webapp2
import urllib2
import os
import cgi

form="""
<form method="post" >
    Tell us your birthday!
<br>
<label>Date
    <input type="text" name="date" placeholder="DD" value="%(day)s">
</label>
<label>Month
    <input type="text" name="month" placeholder="MM" value="%(month)s">
</label>
<label>Year
    <input type="text" name="year" placeholder="YYYY" value="%(year)s">
</label>
<div style="color: red">%(error)s</div>
<span>

</span>
<br>
<input type="submit">
</form>
"""
months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December'];

def valid_month(month):
    if month:
        month=month.capitalize();
        if month in months:
            return month
        
def valid_day(day):
    if day and day.isdigit():
        day=int(day)
        if day<=31 and day >=1 :
            return day

def valid_year(year):
    if year and year.isdigit():
        year =int(year)
        if year<2100 and year>=1800 :
            return year

def html_escape(s):
    return cgi.escape(s, quote = True)
    
class MainPage(webapp2.RequestHandler):
    def write_form(self,error="",day="",month="",year=""):
        self.response.write(form % {"error":error,
                                    "day":html_escape(day),
                                    "month":html_escape(month),
                                    "year":html_escape(year)})
        
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.write_form();
        
    def post(self):
        user_month=self.request.get('month')
        user_year=self.request.get('year')
        user_day=self.request.get('date')
        
        month=valid_month(user_month)
        day=valid_day(user_day)
        year=valid_year(user_year)
        if not (month and year and day):
            self.write_form("invalid input",user_day,user_month,user_year)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")

class TestHandler(webapp2.RequestHandler):
    def post(self):
        q=self.request.get("q")
        self.response.out.write(q)
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(self.request);



class DwnldFile():
    def __init__(self):
        getextFile=urllib2.urlopen('http://portal.amfiindia.com/spages/NAV0.txt')
        csv=getextFile.read()
        print csv
    
    
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/testform', TestHandler),
    ('/thanks', ThanksHandler)
    #('/downloadNAV',DwnldFile),
], debug=True)
