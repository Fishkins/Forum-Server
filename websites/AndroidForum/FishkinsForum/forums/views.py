from django.shortcuts import render_to_response
from forums.models import Thread, Post
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

def getData(request):
    if request.META["HTTP_USER_AGENT"] == "7a3acdfef4bc49b461827b01f365ba":
        load_type = request.GET["loadType"]
        data_dict = {}
    
        if load_type == "Threads":
            thread_list = Thread.objects.all()
            thread_dict = {}
        
            for thread in thread_list:
                thread_dict = {"name": thread.name, "posted_by": str(thread.posted_by.id)}
                data_dict[thread.id] = thread_dict
                
        elif load_type == "Thread":
            post_list = Post.objects.filter(thread=request.GET["ID"])
            post_dict = {}

            for post in post_list:
                post_dict = {"name": post.name,
                             "posted_by": str(post.posted_by.id),
                             "username": post.posted_by.username,
                             "message": post.message,
                             "created_on": post.created_on.strftime("%m/%d/%Y %H:%M %p")}
                
                data_dict[post.id] = post_dict
                
        elif load_type == "Post":
            post = Post.objects.get(pk=request.GET["ID"])
            
            data_dict["name"] = post.name
            data_dict["message"] = post.message
            data_dict["created_on"] = post.created_on.strftime("%m/%d/%Y %H:%M %p")
            data_dict["posted_by"] = str(post.posted_by.id)
            data_dict["username"] = post.posted_by.username

        elif load_type == "User":
            try:
                user = User.objects.get(username__iexact=request.GET["UserName"])
                
                if user.check_password(request.GET["Password"]): 
                    data_dict["id"] = str(user.id)
                    data_dict["is_admin"] = str(user.is_staff)
                else:
                    data_dict["Success"] = "false"

            except:
                data_dict["Success"] = "false"

        elif load_type == "ConfirmUser":
            try:
                user = User.objects.get(id=request.GET["UserID"])

            except:
                data_dict["Success"] = "false"

            else:
                data_dict["Success"] = "true"
                data_dict["username"] = user.username
                data_dict["is_admin"] = str(user.is_staff)

        return render_to_response('forums/get.html', {'json_data': json.dumps(data_dict)})

@csrf_exempt
def postData(request):
    if request.META["HTTP_USER_AGENT"] == "7a3acdfef4bc49b461827b01f365ba":
        post_data = json.loads(request.raw_post_data)

        operation = post_data["Type"]

        if operation == "Post":
            post_user = User.objects.get(pk=post_data["postedby"])
            post_thread = Thread.objects.get(pk=post_data["threadid"])
            new_post = Post(name=post_data["name"], message=post_data["message"], posted_by=post_user, thread=post_thread)
            new_post.save()
            
        elif operation == "PostDel":
            Post.objects.filter(pk=post_data["id"]).delete()
            
        elif operation == "PostEdit":
            edit_post = Post.objects.get(pk=post_data["id"])
            edit_post.name = post_data["name"]
            edit_post.message = post_data["message"]
            edit_post.save()

        elif operation == "ThreadRename":
            edit_thread = Thread.objects.get(pk=post_data["id"])
            edit_thread.name = post_data["name"]
            edit_thread.save()

        elif operation == "ThreadDel":
            del_thread = Thread.objects.filter(pk=post_data["id"])
            Post.objects.filter(thread=del_thread).delete()
            del_thread.delete()

        elif operation == "Thread":
            post_user = User.objects.get(pk=post_data["postedby"])
            new_thread = Thread(name=post_data["name"], posted_by=post_user)
            new_thread.save()
        
        return render_to_response('forums/post.html')
