from flask import Flask, request, redirect, render_template,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog-2:build-a-blog-2@localhost:8889/build-a-blog-2'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, name):
        self.name = name
        self.completed = False


#blogs = []


@app.route('/', methods = ['POST','GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods = ['POST','GET'])
def blog():
    if request.method == "POST":
        title_error_message = ""
        content_error_message = ""

        blog_title = request.form['blog_title']         # pull the blog title from the newpost form
        blog_contents = request.form['blog_contents']       

        if blog_title =="" and blog_contents == "":
            title_error_message = "Please enter a title for your blog"
            content_error_message = "Please enter content for your blog"
            return redirect('/newpost?title_error_message=' + title_error_message + '&content_error_message=' + content_error_message)
        elif blog_title == "":
            title_error_message = "Please enter a title for your blog"
            return redirect('/newpost?title_error_message=' + title_error_message + '&content_error_message=' +  content_error_message +
            '&blog_title=' + blog_title + '&blog_contents=' + blog_contents)  
        elif blog_contents == "":
            content_error_message = "Please enter content for your blog" 
            return redirect('/newpost?title_error_message=' + title_error_message + '&content_error_message=' +  content_error_message +
            '&blog_title=' + blog_title + '&blog_contents=' + blog_contents)  

        #new_blog_title = Blog(blog_title)    # create a new Blog object
        #db.session.add(new_blog_title)       # add the blog object to the session
        #db.session.commit()                  # commit the above blog object to the database

        blogs = Blog.query.all()              

        #blogs.append(blog_title)
        #blogs.append(blog_contents)
       
    return render_template('blog.html',title = "Build A Blog", header = "Build A Blog",blogs = blogs, 
        blog_content_list = blog_content_list) 

@app.route('/newpost', methods = ['POST','GET'])
def newpost():
    title_error_message = request.args.get('title_error_message')
    content_error_message = request.args.get('content_error_message')
    blog_title = request.args.get('blog_title')
    blog_contents = request.args.get('blog_contents')
    if title_error_message == None:
        title_error_message = ""  
    if content_error_message == None:
        content_error_message    = ""  
    if blog_title == None:
        blog_title = ""  
    if blog_contents == None:
        blog_contents = ""      
 
    return render_template('newpost.html', title = "Build A Blog", header = "Build A Blog", blog_title = blog_title,
    blog_contents = blog_contents,title_error_message = title_error_message, content_error_message = content_error_message)



if __name__ == '__main__':
    app.run()