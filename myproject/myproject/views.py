from django.shortcuts import render

#write your code from here

def custom_page_not_found(request, exception ):
    return render(request,'404.html',status=404)
