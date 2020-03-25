from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from . models import*
import bcrypt


# Create your views here.
def index(request):
    return render(request,'login.html')

def takes_to_register_page(request):
    return render(request, 'register.html')

def register(request):   
    errors=User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/to_register')
    else:
        if request.POST['gender'] == 'Male':
            User.objects.gender=False
            gender = False
            
        else: 
            User.objects.gender=True
            gender = True
        pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
        first_name=request.POST['first_name'], 
        last_name=request.POST['last_name'], 
        email=request.POST['email'], 
        description=request.POST['description'],
        password=pw_hash,
        nickname=request.POST['nickname'],
        gender=gender,
        age=request.POST['age'],
        admin=True
        )
        
        if len(User.objects.all())>1:
            user.admin=False
        
        
        request.session['user_id'] = user.id
        request.session['user_first_name']=user.first_name
        request.session['user_last_name']=user.last_name
        request.session['user_email']=user.email
        
        user.save()
    
    return redirect('/dashboard')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        user = user[0]
        if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            messages.error(request, 'Passwords do not match')
            return redirect('/')
        else:
            request.session['user_id'] = user.id
            request.session['user_first_name']=user.first_name
            request.session['user_last_name']=user.last_name
            request.session['user_email']=user.email
            request.session['user_nickname']=user.nickname
        return redirect('/dashboard')
    return redirect('/')

def logout(request):
    del request.session['user_id']
    del request.session['user_email']
    del request.session['user_first_name']
    del request.session['user_last_name']
    del request.session['user_nickname']
    return redirect('/')

def dashboard(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in")
        return redirect('/')
    context= {
        'all_users': User.objects.all(),
        'current_user': User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'dashboard.html', context)

def redirects_to_add_user_page(request):
    return render (request, 'add_new_user.html')

def new_user (request):
    errors=User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/users/new')
    else:
        pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        user = User.objects.create(
        first_name=request.POST['first_name'], 
        last_name=request.POST['last_name'], 
        email=request.POST['email'], 
        password=pw_hash,
        admin=False)
        return redirect('/dashboard')

def update_user_page(request, user_id):
    context= {
        'user': User.objects.get(id=user_id),
        'current_user': User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'edit_user.html', context)

def update_info (request, user_id):
    user=User.objects.get(id=user_id)
    
    user.nickname=request.POST['nickname']
    request.session['user_nickname']=user.nickname
    
    user.email=request.POST['email']
    # errors = User.objects.info_validator(request.POST, user)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     return redirect(f'/users/update/{user.id}')
    print(request.FILES)
    print(request.POST)
    if 'myfiles' in request.FILES:
        user.photo=request.FILES['myfiles']
        print (request.FILES)
    user.save()
    
    # if request.POST['admin_status'] and request.POST['admin_status']=='Admin':
    #     user.admin=True
    # else:
    #     user.admin=False
    

    return redirect('/dashboard')

def update_description(request, user_id):
    
    user=User.objects.get(id=user_id)
    errors=User.objects.description_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/users/update/{user.id}')
    # if not user.admin in request.POST['description']:
    user.description=request.POST['description']
    user.save()
    return redirect('/dashboard')
    

def update_password(request, user_id):
    user=User.objects.get(id=user_id)
    errors = User.objects.password_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/users/update/{user.id}')
    pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user.password=pw_hash
    user.save()
    return redirect('/dashboard')

def user_profile(request, user_id):
    context={
        'current_user': User.objects.get(id = request.session['user_id']),
        'user': User.objects.get(id=user_id),
        'all_messages': Message.objects.filter(id=user_id),
        'all_comments': Profile_page.objects.all()
    }
    return render(request, 'profile.html', context)

def remove_user(request, user_id):
    user=User.objects.get(id=user_id)
    user.delete()
    return redirect('/dashboard')

def post_text(request, user_id):
    errors = Message.objects.messageValidator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect (f'/users/show/{user_id}')
    else:
        user_for=User.objects.get(id=user_id)
        user = User.objects.get(id=request.session['user_id'])
        message = Message.objects.create(message=request.POST['message'], user=user, user_page=user_for)
        return redirect(f'/users/show/{user_id}')

def comment(request, user_id, message_id):
    errors = Comment.objects.commentValidator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect (f'/users/show/{user_id}')
    else:
        user=User.objects.get(id=request.session['user_id'])
        message=Message.objects.get(id=message_id)
        comment=Comment.objects.create(
            comment=request.POST['comment'],
            user=user,
            message=message)
        return redirect(f'/users/show/{user_id}')

def delete_comment(request, comment_id, user_id):
    User.objects.get(id=request.session['user_id'])
    comment=Comment.objects.get(id=comment_id)
    if comment.user.id == request.session['user_id']:
        comment.delete()
    return redirect(f'/users/show/{user_id}')

def delete_message(request, message_id, user_id):
    User.objects.get(id=request.session['user_id'])
    message=Message.objects.get(id=message_id)
    if message.user.id == request.session['user_id']:
        message.delete()
    return redirect(f'/users/show/{user_id}')


def results_page(request):
    if request.method == 'GET':
        x = {'Female': True, 'Male': False}
        query=request.GET.get('search')
        submitbutton=request.GET.get('submit')
        if query is not None:
            results= User.objects.filter(gender = x[request.GET['search']]).distinct()
            context={'results': results,
                    'submitbutton': submitbutton}
            return render(request, 'search.html', context)
        else:
            return redirect('/dashboard')
    else:
        return render(request, 'search.html', context)


