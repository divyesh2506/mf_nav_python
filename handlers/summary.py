from __future__ import division
import os
import webapp2
import jinja2
import re 
import sys
sys.path.insert(0, 'libs')

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

class SummaryTool(object):
    def stemming(self, array):
        from stemming.porter2 import stem
        words=[]
        for word in array:
            words.append(stem(word))

        return words



    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        return content.split(". ")
 

    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")
 
    def sentences_intersection(self, sent1, sent2):
        # split the sentence into words/tokens
        s1 = set(self.stemming(sent1.split(" ")))
        s2 = set(self.stemming(sent2.split(" ")))
 
        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0
 
        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)
 
    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence
 
    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
    def get_sentences_ranks(self, content): 
    # Split the content into sentences
        sentences = self.split_content_to_sentences(content)
 
    # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])
 
# Build the sentences dictionary
# The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sentence(sentences[i])] = score
        return sentences_dic
 
    # Return the best sentence in a paragraph
    def get_best_sentence(self, paragraph, sentences_dic):
        # Split the paragraph into sentences
        sentences = self.split_content_to_sentences(paragraph)
 
        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""
 
        # Get the best sentence according to the sentences dictionary
        bbs1=""
        bs2=""
        bs3=""
        bs4=""
        mv1=0
        mv2=0
        mv3=0
        mv4=0
        best_sentence = ""

        max_value = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                val=sentences_dic[strip_s]
                if  val> mv1:
                    mv1 = sentences_dic[strip_s]
                    bs1 = s
                elif  val> mv2:
                    mv2 = sentences_dic[strip_s]
                    bs2 = s
                elif  val> mv3:
                    mv3 = sentences_dic[strip_s]
                    bs3 = s
                elif  val> mv4:
                    mv4 = sentences_dic[strip_s]
                    bs4 = s

        best_sentence=bs1+".\n"+bs2+".\n"+bs3+".\n"+bs4
        return best_sentence
 
    # Build the summary
    def get_summary(self, title, content, sentences_dic): 
        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)
 
        # Add the title
        summary = []
        summary.append(title.strip())
        summary.append("")
 
        # Add the best sentence from each paragraph
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)
 
        return ("\n").join(summary) 

   
    
class SummaryPage(AppHandler):
   
    def render_front(self,title="",content="",error="",summary=""):
        self.render("summary.html",title=title,content=content,error=error,summary=summary)
    
    def get(self):
        #db.delete(Blogs.all())
        self.render_front()
        #self.write("asciichan!!")
        #items=self.request.get_all("food")
    def post(self):
        title=self.request.get("title")
        content=self.request.get("content")
        
        if title and content :
            st=SummaryTool()
            sentences_dic = st.get_sentences_ranks(content)
            summary = st.get_summary(title, content, sentences_dic)
            self.render_front(title,content,"",summary)

        else:
            error="we need both a title and the content"
            self.render_front(title,content,error=error)
    
        
# application = webapp2.WSGIApplication([
#     ('/blog', BlogMainPage),
#     ('/blog/newpost', BlogNewPost),
#     (r'/blog/(\d+)',GetBlogWithID)
# ], debug=True)