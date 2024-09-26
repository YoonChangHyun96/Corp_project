from django.shortcuts import render, redirect
from asdf.models import Users, Posts, Messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

import random



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


#ych

# 전투 페이지 뷰 함수
def battle_page(request, level):
    if 'player_hp' not in request.session:
        request.session['player_hp'] = 200
        request.session['opponent_hp'] = 211
        request.session['battle_logs'] = []
        request.session['turn_counter'] = 1

    player_hp = request.session['player_hp']
    opponent_hp = request.session['opponent_hp']
    battle_logs = request.session['battle_logs']
    turn_counter = request.session['turn_counter']

    if request.method == 'POST':
        attack_type = request.POST.get('attack_type')

        if attack_type == 'strong':
            player_damage = 50
            battle_logs.append(f"{turn_counter}번째 턴: 플레이어가 강한 공격으로 {player_damage}의 피해를 입혔습니다!")
        else:
            player_damage = 20
            battle_logs.append(f"{turn_counter}번째 턴: 플레이어가 약한 공격으로 {player_damage}의 피해를 입혔습니다!")

        opponent_hp -= player_damage
        if opponent_hp <= 0:
            opponent_hp = 0

        if opponent_hp > 0:
            opponent_damage = 30
            battle_logs.append(f"{turn_counter}번째 턴: 상대방이 강한 공격으로 {opponent_damage}의 피해를 입혔습니다!")
            player_hp -= opponent_damage
            if player_hp <= 0:
                player_hp = 0

        turn_counter += 1

        request.session['player_hp'] = player_hp
        request.session['opponent_hp'] = opponent_hp
        request.session['battle_logs'] = battle_logs
        request.session['turn_counter'] = turn_counter

    # 플레이어 HP가 0이면 패배 페이지 렌더링, level을 context에 포함
    if player_hp == 0:
        return render(request, 'fail_page.html', {'level': level})

    # 상대방 HP가 0이면 승리 페이지 렌더링, level을 context에 포함
    if opponent_hp == 0:
        return render(request, 'clear_page.html', {'level': level})

    context = {
        'player_hp': player_hp,
        'opponent_hp': opponent_hp,
        'battle_logs': battle_logs,
        'level': level  # 이 부분도 추가
    }

    return render(request, 'battle_page.html', context)



# 레벨 선택 페이지 뷰 함수
def challenge_level_selection(request):
    cleared_levels = [1]  # 1단계만 클리어한 상태
    max_level = max(cleared_levels)  # 클리어한 최대 레벨 계산
    next_level = max_level + 1  # 다음 도전할 레벨 계산
    context = {
        'cleared_levels': cleared_levels,
        'max_level': max_level,
        'next_level': next_level,
        'levels': reversed(range(1, 11))  # 1단계와 2단계만 표시 (테스트용)
    }

    return render(request, 'challenge_level_selection.html', context)

# 전투 상태 초기화 뷰
def reset_battle(request, level):
    # 전투 상태를 초기화
    request.session['player_hp'] = 200
    request.session['opponent_hp'] = 211
    request.session['battle_logs'] = []
    request.session['turn_counter'] = 1

    # 초기화 후 해당 레벨의 전투 페이지로 이동
    return redirect('battle_page', level=level)
