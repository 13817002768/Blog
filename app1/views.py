from django.shortcuts import render, redirect
from .models import User, Blog, Category, Comment
from django.http import HttpResponse
from json import dumps
# Create your views here.
def index(request):
    return render(request, 'index.html')


# 登录功能
def login(request):
    if(request.method == 'POST'):
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        user = User.objects.filter(username=username)
        if(user):
            user = User.objects.get(username=username)
            print(user.password)
            if(str(password)==str(user.password)):

                request.session['IS_LOGIN'] = True
                request.session['username'] = username

                #return render(request,'home.html',{'user':user})
                return redirect('/home')
            else:
                return render(request, 'login.html', {'error': '密码错误!'})
        else:
            return render(request, 'login.html', {'error': '用户名不存在!'})

    else:
        return render(request, 'login.html')

# 注册功能，成功注册返回登录页面
def register(request):
    if(request.method=="POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        
        if(User.objects.filter(username=username)):
            return render(request, 'register.html', {'error': '该用户已存在!'})
        if(password != password2):
            return render(request, 'register.html', {'error': '两次密码不一致，请重新输入！'})
        user = User()
        user.username = username
        user.password = password
        user.email = email

        user.save()

        return render(request, 'login.html')



    return render(request, 'register.html')

def base(request):
    return render(request, 'base.html')

def message(request):
    return render(request, 'message.html')


def home(request):

    if(request.session.get('IS_LOGIN')):
        username = request.session.get('username')
        blogs = Blog.objects.all()


        comment_nums = []
        for blog in blogs:
            comments = Comment.objects.filter(article = blog).count()
            blog.comment_num = comments

        categorys = Category.objects.all()
        return render(request, 'home.html', {'blogs': blogs, 'categorys': categorys, 'username': username})

    else:
        return redirect('/login')

# 退出功能，退出时清除session并返回登录页
def logout(request):
    request.session.flush()
    return redirect('/login')

# 分类查询博客
def find_by_category(request, category):

    username = request.session.get('username')
    #category = request.GET.get('category')
    blogs = Blog.objects.filter(category = Category.objects.get(name = category))

    comment_nums = []
    for blog in blogs:
        comments = Comment.objects.filter(article = blog).count()
        comment_nums.append(comments)

    categorys = Category.objects.all()
    return render(request, 'home.html', {'blogs': blogs, 'categorys': categorys, 'comment_nums': comment_nums, 'username':username})

# 通过博客的id查询博客的详细信息
def blog_detail(request, blog_id):
    if(request.session.get('IS_LOGIN')):
        username = request.session.get('username')

        blog = Blog.objects.get(blog_id = blog_id)
        comments = Comment.objects.filter(article = blog)
        print('blog',blog)
        return render(request, 'blog_detail.html', {'blog':blog, 'comments':comments, 'username':username})
    else:
        return redirect('/login')

# 评论功能
def add_comment(request):
    username = request.POST.get('username')
    article = request.POST.get('article')
    content = request.POST.get('comment')
    
    
    blog = Blog.objects.get(blog_id=article)
    user = User.objects.get(username=username)

    comment = Comment(article=blog,author=user,body=content)
    comment.save()
    
    return HttpResponse('12')

# 查找所有我的个人博客
def my_blog(request, username):
    user = User.objects.get(username=username)
    blogs = Blog.objects.filter(author=user)
    comment_nums = []
    for blog in blogs:
        comments = Comment.objects.filter(article = blog).count()
        blog.comment_num = comments

    categorys = Category.objects.all()

    return render(request, 'my_blog.html', {'blogs':blogs, 'categorys':categorys, 'username':username})
    
# 删除博客
def del_blog(request, blog_id):
    Blog.objects.filter(blog_id=blog_id).delete()

    username = request.session.get('username')
    user = User.objects.get(username=username)
    blogs = Blog.objects.filter(author=user)
    comment_nums = []
    for blog in blogs:
        comments = Comment.objects.filter(article = blog).count()
        blog.comment_num = comments

    categorys = Category.objects.all()

    return render(request, 'my_blog.html', {'blogs':blogs, 'categorys':categorys, 'username':username})

# 新增博客
def add_blog(request):
    if(request.method == "POST"):
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        username = request.session.get('username')

        user = User.objects.get(username=username)
        blog = Blog()
        blog.title = title
        blog.content = content
        blog.category = Category.objects.get(name=category)
        blog.author = user
        blog.blog_id = '444'
        blog.save()

        blogs = Blog.objects.filter(author=user)
        comment_nums = []
        for blog in blogs:
            comments = Comment.objects.filter(article = blog).count()
            blog.comment_num = comments

        categorys = Category.objects.all()

        return render(request, 'my_blog.html', {'blogs':blogs, 'categorys':categorys, 'username':username})

    else:
        username = request.session.get('username')
        categorys = Category.objects.all()
        return render(request, 'add_blog.html', {'username':username, 'categorys':categorys})

# 修改博客
def update_blog(request, blog_id):
    if(request.method == 'POST'):
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        username = request.session.get('username')

        blog = Blog.objects.get(blog_id=blog_id)
        blog.title = title
        blog.content = content
        blog.category = Category.objects.get(name=category)
        blog.save()

        return redirect('/my_blog/' + username)
    else:
        blog = Blog.objects.get(blog_id=blog_id)
        username = request.session.get('username')
        categorys = Category.objects.all()
        return render(request, 'update_blog.html', {'username':username, 'categorys':categorys, 'blog':blog})

# 修改登录密码
def update_password(request):
    username = request.session.get('username')
    if(request.method == 'POST'):
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        password3 = request.POST.get('password3')

        user = User.objects.get(username=username)
        if(user.password != password):
            hint = '原密码输入错误'
            return render(request, 'update_password.html', {'username':username, 'hint':hint})
        if(password2 != password3):
            hint = '两次新密码输入不一致'
            return render(request, 'update_password.html', {'username':username, 'hint':hint})
        user.password = password2
        user.save()
        return render(request, 'update_password.html', {'username':username, 'hint':"密码修改成功"})

    else:
        return render(request, 'update_password.html', {'username':username})

# 通过标题模糊查询博客
def find_by_title(request, title):
    username = request.session.get('username')
    blogs = Blog.objects.filter(title__contains=title)
    comment_nums = []
    for blog in blogs:
        comments = Comment.objects.filter(article = blog).count()
        blog.comment_num = comments

    categorys = Category.objects.all()
    return render(request, 'home.html', {'blogs': blogs, 'categorys': categorys, 'username': username})
