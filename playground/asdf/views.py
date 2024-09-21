from django.shortcuts import render, redirect
from asdf.models import Users, Posts, Messages
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import random, time



def Index_Page(request):
    return render(request, "index.html")


def Signup_Page(request):
    return render(request, "signup.html")


def Login_Page(request):
    return render(request, "login.html")


def Signup_Action(request):
    # 입력받은 값 정의
    var_user_id = request.POST.get('input_user_id')
    var_password = request.POST.get('input_password')
    var_name = request.POST.get('input_name')
    var_email = request.POST.get('input_email')

    # 빈 필드가 없는지 검증
    if var_user_id and var_password and var_name and var_email:

        # 입력받은 아이디, 이메일이 db에 존재하는지 검증
        if Users.objects.filter(user_id = var_user_id).exists():
            return redirect('Signup_Page')
    
        if Users.objects.filter(email = var_email).exists():
            return redirect('Signup_Page')
        
        # db에 입력받은 유저 정보 저장
        Users.objects.create(
            user_id = var_user_id,
            password = var_password,
            name = var_name,
            email = var_email
        )
        
        return render(request, "login.html")

    else:
        return redirect('Signup_Page')
    

def Login_Action(request):
    # 입력받은 값 정의
    var_user_id = request.POST.get('input_user_id')
    var_password = request.POST.get('input_password')

    # 빈 필드가 없는지 검증
    if var_user_id and var_password:

        select_user = Users.objects.filter(user_id = var_user_id).first()

        if select_user:
      
            if select_user.password == var_password:
                # 사용자를 로그인한다
                login(request, select_user)

                return render(request, 'index.html')

            else:
                return redirect('Login_Page')
        
        else:
            return redirect('Login_Page')
    

def Logout(request):
    request.session.flush()

    return redirect('Index_Page')


@login_required
def Board_Page(request):
    posts_object = Posts.objects.all()

    return render(request, 'board.html', {'posts' : posts_object})


def Post_Writing_Page(request):
    var_name = request.user.name

    return render(request, 'post_writing.html', {"name" : var_name})


def Post_Writing_Action(request):
    var_title = request.POST.get('input_title')
    var_content = request.POST.get('input_content')
    var_author = request.POST.get('input_author')
    user_object = Users.objects.get(id = request.user.id)
    
    if var_title and var_content:

        Posts.objects.create(
            title = var_title,
            content = var_content,
            author = var_author,
            connected_user = user_object
        )

    else:
        return redirect('Post_Writing_Page')
        
    return redirect('Board_Page')
    

def Post_Detail_Page(request, post_id):
    post_object = Posts.objects.get(id = post_id)

    return render(request, 'post_detail.html', {'post' : post_object})


def Myaccount_Page(request):
    var_posts = request.user.posts.all()

    return render(request, 'myaccount.html', {'posts' : var_posts})


def Edit_Info(request):
    var_user_id = request.POST.get('input_user_id')
    var_name = request.POST.get('input_name')
    var_email = request.POST.get('input_email')

    if var_user_id and var_name and var_email:

        if Users.objects.filter(user_id = var_user_id).exists():
            
            return redirect('Myaccount_Page')
        
        elif Users.objects.filter(email = var_email).exists():
            
            return redirect('Myaccount_Page')
        
        else:
            user = Users.objects.filter(id = request.user.id).first()
            user.user_id = var_user_id
            user.name = var_name
            user.email = var_email
            user.save()

            return render(request, 'myaccount.html')
    
    else:
        return redirect('Myaccount_Page')



def User_Detail_Page(request, connected_user_id):
    user_object = Users.objects.get(id = connected_user_id)

    return render(request, 'user_detail.html', {'user' : user_object})


def Delete_Post(request, post_id):
    post_object = Posts.objects.get(id = post_id)
    post_object.delete()

    return redirect('Board_Page')


def Message_Box_Page(request):
    messages_object = Messages.objects.all()

    return render(request, 'message_box.html', {'messages' : messages_object})


def Message_Writing_Page(request):

    return render(request, 'message_writing.html')


def Message_Writing_Action(request):
    var_recipient = request.POST.get('input_recipient')
    var_title = request.POST.get('input_title')
    var_content = request.POST.get('input_content')
    user_object = Users.objects.get(id = request.user.id)

    if var_recipient and var_title and var_content:

        if Users.objects.filter(user_id = var_recipient).exists():

            Messages.objects.create(
                recipient = var_recipient,
                title = var_title,
                content = var_content,
                connected_user = user_object
            )

            return redirect('Message_Box_Page')
            
        else:
            return redirect('Message_Writing_Page')
    
    else:
        return redirect('Message_Writing_Page')
    

def Message_Detail_Page(request, message_id):
    message_object = Messages.objects.get(id = message_id)

    return render(request, 'message_detail.html', {'message' : message_object})


def Message_Reply_Page(request, connected_user_id):
    user_object = Users.objects.get(id = connected_user_id)

    return render(request, 'message_reply.html', {'user' : user_object})


def Message_Delete(request, message_id):
    message_object = Messages.objects.get(id = message_id)
    message_object.delete()

    return redirect('Message_Box_Page')


def Sword_Page(request):
    user_object = Users.objects.get(id = request.user.id)
    dictionary = {
        'sword_level' : user_object.sword_level,
        'user' : user_object
    }

    return render(request, 'sword.html', dictionary)


def Sword_Upgrade(request):
    user_object = Users.objects.get(id = request.user.id)
    a = random.randint(1, 10)

    if user_object.money >= 500:
        user_object.money -= 500
        
        if a % 3 == 0:
            user_object.sword_level += 1
            user_object.save()
    else:
        messages.error(request, '소지금이 부족합니다.')

    return redirect('Sword_Page')


def Sword_Sell(request, sword_level):
    user_object = Users.objects.get(id = request.user.id)
    user_object.money += sword_level*1000
    user_object.sword_level = 0
    user_object.save()

    return redirect('Sword_Page')


def Money_Reset(request):
    user_object = Users.objects.get(id = request.user.id)
    user_object.money = 5000
    user_object.save()

    return redirect('Sword_Page')


def Raising_Bagger_Page(request):
    user_object = Users.objects.get(id = request.user.id)

    return render(request, 'raising_bagger.html', {'user': user_object})


def Raising_Bagger_Start(request):
    user_object = Users.objects.get(id = request.user.id)
    while True:
        user_object.money += 500
        time.sleep(3)
        
        if user_object.money > 10000:
            break

    return redirect('Raising_bagger_Page')


