from flask import Flask, request, redirect, render_template,flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '123456789'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000)) 
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))  

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner
         

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)     # 'unique = True' prevents a username to be used twice
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog',backref='owner')

    def __init__(self,username,password):        
        self.username = username
        self.password = password

@app.before_request                                  # a special route decorator that runs before anything else, a way to filter incoming requests
def require_login():
    allowed_routes = ['login','signup','blog','index']   # these are the names of the functions, not routes...allowing a user to access the routes even if they haven't logged in
    if request.endpoint not in allowed_routes and 'username' not in session:   # if the request is something other than what's in the allowed_routes list and
        return redirect ('/login')                                          # the user hasn't logged in, force the user to the login page

@app.route('/')
def index():
    users = User.query.all()   
    return render_template('index.html', header = "Blog users!", users = users)    
    #return render_template('login.html')
 
    

@app.route('/signup', methods = ['POST','GET'])
def validate_signup():
    if request.method == "POST":
        username_error = ''
        password_error = ''
        verifypassword_error = '' 

        username = request.form['username']
        password = request.form['password']
        verifypassword = request.form['verifypassword']

 

        if username == "" and password == '' and verifypassword == '':
            username_error = "Please type a username"
            password_error = "Please type a password"
            verifypassword_error = "Please verify your password"
            return render_template('signup.html', username_error = username_error, password_error = password_error,
                verifypassword_error = verifypassword_error)
        elif len(username) < 3 or len(username) > 20 or ' ' in username:
            username_error = "That's not a valid username"
            return render_template('signup.html', username_error = username_error)        
        
        if  password == '' and verifypassword == '':       
            password_error = "Please type a password"
            verifypassword_error = "Please verify your password"
            return render_template('signup.html',password_error = password_error,
                verifypassword_error = verifypassword_error, username = username)
        elif len(password) < 3 or len(password) > 20 or ' ' in password:
            password_error = "That's not a valid password"
            return render_template('signup.html', password_error = password_error, username = username)         

        # if verify password box is left blank or it doesn't match the password box then display error message
        if  verifypassword == '' or verifypassword != password:    
            verifypassword_error = "Passwords don't match"
            return render_template('signup.html',verifypassword_error = verifypassword_error, username = username) 

        existing_user = User.query.filter_by(username=username).first()  # check to see if the username already exists

        if not existing_user:                            # if it doesn't exist, then
            new_user = User(username,password)           # create a new User object
            db.session.add(new_user)                     # add the user object to the session
            db.session.commit()                          # commit the above user object to the database 
            session['username'] = username               # session needed to be imported from Flask; it's a dictionary; setting the key
            #return redirect ('/newpost')                # of username to the value of username...a way to 'remember' the user has logged in
        if existing_user:
            username_error = "Username already exists"
            return render_template('signup.html', username_error = username_error, password_error = password_error,
                verifypassword_error = verifypassword_error)    

 

    return render_template('signup.html')

@app.route('/login', methods = ['POST', 'GET'])
def signup():
    if request.method == "POST":
        username_error = ''
        password_error = ''        

        username = request.form['username']
        password = request.form['password'] 
        user = User.query.filter_by(username=username).first()  # if the username entered exists, then assign this database row to variable user
        if user and user.password == password:
            session['username'] = username                    # 'remember' that the user has logged in until he logs out
            return redirect ('/newpost') 
        if user == None:
            username_error = "Username doesn't exist"  
            return render_template('login.html', username_error = username_error, password_error = password_error)        
    

        if username == "" and password == '' :
            username_error = "Please type a username"
            password_error = "Please type a password"           
            return render_template('login.html', username_error = username_error, password_error = password_error)
        elif len(username) < 3 or len(username) > 20 or ' ' in username:
            username_error = "That's not a valid username"
            return render_template('login.html', username_error = username_error)        
        
        if  password == '':       
            password_error = "Please type a password"           
            return render_template('login.html',password_error = password_error, username = username)
        elif password != user.password:
            password_error = "Passord is incorrect"  
            return render_template('login.html',password_error = password_error, username = username)
        elif len(password) < 3 or len(password) > 20 or ' ' in password:
            password_error = "That's not a valid password"
            return render_template('login.html', password_error = password_error, username = username)
       

       
    return render_template('login.html')



@app.route('/blog', methods = ['POST','GET'])
def blog():
    
    if request.method == "POST":
        title_error_message = ""
        content_error_message = ""

        blog_title = request.form['blog_title']         # pull the blog title from the newpost form
        blog_contents = request.form['blog_contents']   # pull the blog contents from the newpost form

        # error code    
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

        user = User.query.filter_by(username=session['username']).first()   # get the current session's username and find it in the user table
        single_blog = Blog(blog_title,blog_contents,user)    # create a new Blog object; the user argument will generate the user's id because this is how the class is set up
        db.session.add(single_blog)                     # add the blog object to the session
        db.session.commit()                          # commit the above blog object to the database
        return render_template('individual.html', single_blog = single_blog ) # after creating a blog post, display the individual post
        
    blogs = Blog.query.all()                         # get all the rows of the blog table  
    users = User.query.all()                        # get all the users in the users table

    if request.args.get('id') != None:               # if a query parameter with the name 'id' exists
        id = request.args.get('id')                  # assign the value of the query parameter to the id variable
        single_blog = Blog.query.get(id)             # assign the blog object with the id to a variable
        user = User.query.filter_by(id = id).first()
        return render_template('individual.html', single_blog = single_blog, user = user)  # pass this blog object to the template

    if request.args.get('user') != None:               # if a query parameter with the name 'user' exists
        user = request.args.get('user')                  # assign the user name from the query parameter to a user variable
        selected_user = User.query.filter_by(username = user).first()            # assign the blog object with the id to a variable               
        return render_template('singleUser.html', header = "Blog posts!", users = users, selected_user = selected_user, user = user,
            blogs = blogs)    

    return render_template('blog.html',title = "Blogz", header = "Blog posts!",blogs = blogs,users = users)
             

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
 
    return render_template('newpost.html', title = "Blogz", header = "Build a Blog", blog_title = blog_title,
    blog_contents = blog_contents,title_error_message = title_error_message, content_error_message = content_error_message)

#@app.route('/index')
#def index():
#    users = User.query.all()   
#    return render_template('index.html', header = "Blog users!", users = users)      

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()