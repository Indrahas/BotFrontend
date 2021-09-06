from django.shortcuts import render
from . import session_manager
# Create your views here.
user_id=""
def index(request):
    try:
        user_pay1_id = request.GET["user_pay1_id"]
        user_id = user_pay1_id
        token = request.GET["token"]
        session_details = session_manager.SessionManager(user_pay1_id,token)
        session = session_details.validate_session()
        print (session)
        print(user_id)
        if session:
            return render(request,"chatroom.html")
        else:
            return render(request,"errorpage.html")
    except:
        return render(request,"errorpage.html")
def user():
    return user_id