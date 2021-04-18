from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if 'id' in request.session.keys():
        return redirect ('/wishes')
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
            print(pw_hash)   

            new_user = User.objects.create(
                name=request.POST['name'], 
                last_name=request.POST['last_name'], 
                email=request.POST['email'], 
                password=pw_hash)
            print(new_user)
            request.session['user_id'] = new_user.id
            request.session['email'] = new_user.email
            request.session['user_name'] = f"{new_user.name}"
            request.session['status'] = "registered"
            request.session['isloggedin'] = True

        return redirect("/wishes") # nunca renderizar en una publicación, ¡siempre redirigir!
    return redirect("/")

def login(request):
    if request.method == 'POST':
        errors = User.objects.log_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.filter(email=request.POST['email'])
            if user:
                logged_user = user[0] #solo hay un usuario con ese email, por lo que se usa [0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['user_id'] = logged_user.id
                    request.session['email'] = logged_user.email
                    request.session['user_name'] = f"{logged_user.name}"
                    request.session['status'] = "Logged in"
                    request.session['isloggedin'] = True
            
                    return redirect('/wishes')
                else: 
                    messages.error(request, "password invalid")
        return redirect("/")

def logout(request):
    request.session.clear()
    request.session['isloggedin'] = False
    return redirect('/')
# ************************************** main page

def wishes(request):
    if not request.session['isloggedin']:
        return redirect('/')
    else:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        all_wish = Granted.objects.all()
        current_user = User.objects.get(email=request.session["email"])
        wishes = Wish.objects.all()
        context = {
                'wishes' : wishes,
                "user": user,
                "current_user": current_user,
                "all_wish": all_wish,
                }
        print(wishes)
        print(all_wish)
        return render(request, 'wish.html', context)

def addwish(request):
    if not request.session['isloggedin']:
        return redirect('/')
    else:
        return render(request, 'addwish.html')

#add job to db
def add_wish_to_db(request):
    if not request.session['isloggedin']:
        return redirect('/')
    else:
        errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/wishes/new')

    else:
        wish = request.POST["wish"]
        description = request.POST["description"]
        this_user = User.objects.get(email=request.session['email'])

        this_wish = Wish.objects.create(
            wish = wish,
            description = description,
            submitted_by = this_user,
        )
        return redirect('/wishes')

#***************************editar wishes
def edit_wish(request, id):
    if not request.session['isloggedin']:
        return redirect('/')
    else:
        this_wish = Wish.objects.get(id=id)
        context = {
            "wish" : this_wish,
        }
        print('page ready')
        return render(request, 'editwish.html', context)

def edit_wish_to_db(request, id):
    if not request.session['isloggedin']:
        print('not logged')
        return redirect('/')
    else:
        errors = Wish.objects.wish_validator_edit(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print('errors found')
            return redirect('/edit/'+str(id))
    else:
        current_wish = Wish.objects.get(id=id)
        new_title = request.POST['form_edit_title']
        new_desc = request.POST['form_edit_desc']

        current_wish.wish = new_title
        current_wish.description = new_desc
        current_wish.save()
        print('wish saved')
        return redirect('/wishes')

# ********************** delete
def delete(request, id):
    
    wish_delete = Wish.objects.get(id=id)
    wish_delete.delete()
    
    return redirect("/wishes")

#view Wishes ; pending and granted TERMINAR Y REVISAR!
def stats(request):
    if not request.session['isloggedin']:
        return redirect('/')
    else:
        all_granted = Granted.objects.count()
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        wish_amt = Wish.objects.filter(submitted_by=request.session["user_id"]).count()
        grant_amt = Granted.objects.filter(user_list=request.session["user_id"]).count()
        count = int(wish_amt) - int(grant_amt)



        context = {
            "all_granted": all_granted,
            "granted": grant_amt,
            "pending": count,

        }


        return render(request, 'stats.html', context)


# ********************** add to job list
def granted_wish(request,id):
    user = User.objects.get(id=request.session["user_id"])
    this_wish = Wish.objects.get(id=id)

    if not user.user_granted.filter(wish_granted=this_wish) :
        Granted.objects.create(user_list=user, wish_granted=this_wish)
    print("SUBMITTING TO DB")
    return redirect('/wishes')


# ******************************* like y contador
def like(request):
    pass
    
    return redirect("/wishes")
