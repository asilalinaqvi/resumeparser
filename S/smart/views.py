from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
import re
from forms import testForm
import os
import json
from pymongo import MongoClient
from django.core.files.storage import FileSystemStorage
import random





def parser(filename):
    os.popen("java -jar Recruit.jar %s" %filename)
    return 0

def index(request):

    return render(request, 'smart/index.html', {'returnedData': ''})

def show(request,pk):
   if pk:
       client = MongoClient()
       db = client['parsed']
       resume = db["resume"]
       pk=int(pk)

       collection=resume.find({"id":pk})
       data=collection[0]
       return render(request, 'smart/show.html', {'returnedData': data})


def results(request):
    client = MongoClient()
    db = client['parsed']
    resume = db["resume"]
    if (('name' in request.GET) and request.GET['name'].strip()) or (('education' in request.GET) and request.GET['education'].strip()) or (('experience' in request.GET) and request.GET['experience'].strip()) or (('skills' in request.GET) and request.GET['skills'].strip()) or (('contact' in request.GET) and request.GET['contact'].strip()):
        name = request.GET['name']
        education = request.GET['education']
        experience = request.GET['experience']
        skills = request.GET['skills']
        contact = request.GET['contact']
        address = request.GET['address']
        category = request.GET['category']
        query_name = "JSON.stringify(this.profile.name).indexOf('"
        query_name += name
        query_name += "')!=-1"

        query_education = "JSON.stringify(this.education).indexOf('"
        query_education += education
        query_education += "')!=-1"

        query_experience = "JSON.stringify(this.experience).indexOf('"
        query_experience += experience
        query_experience += "')!=-1"

        query_skills = "JSON.stringify(this.skills).indexOf('"
        query_skills += skills
        query_skills += "')!=-1"

        query_contact = "JSON.stringify(this.profile.contact_no).indexOf('"
        query_contact += contact
        query_contact += "')!=-1"

        query_address = "JSON.stringify(this.profile.address).indexOf('"
        query_address += address
        query_address += "')!=-1"

        query_category = "JSON.stringify(this.category).indexOf('"
        query_category += category
        query_category += "')!=-1"

        rate=request.GET["sortby"]
        rate=int(rate)
        if rate!=0:
            collection = resume.find({"$or":[{"$where":query_name},{"$where":query_education},
                                             {"$where":query_experience},{"$where":query_skills},
                                             {"$where":query_contact},{"$where":query_address},{"$where":query_category}]}).sort([('ratings',rate)])
            return render(request, 'smart/results.html', {'returnedData': collection})
        else:
            collection = resume.find({"$or": [{"$where": query_name}, {"$where": query_education},
                                              {"$where": query_experience}, {"$where": query_skills},
                                              {"$where": query_contact}, {"$where": query_address},{"$where":query_category}]})
            return render(request, 'smart/results.html', {'returnedData': collection})
    return render(request, 'smart/index.html', {'returnedData': ''})


def parsed(request):
    if os.path.exists('parsed_resume.json'):
        os.remove('parsed_resume.json')
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        name=myfile.name
        name=name.replace(" ","-")
        filename = fs.save(name, myfile)
        uploaded_file_url = fs.url(filename)
        filed = '.'+uploaded_file_url
        parser(filed)
    return render(request,'smart/parsed.html')


def parsed_result(request):
    f = open('parsed_resume.json', "r")
    jsons = json.loads(f.read().decode("utf-8","ignore").lower())
    client = MongoClient()
    db = client['parsed']
    resume=db["resume"]
    form = testForm(request.POST or None, initial={'Results': jsons})

    ratings = request.POST.get('ratings', False)
    category = request.POST.get('category', False)

    location = request.POST.get('location', False)
    website = request.POST.get('website', False)
    phone = request.POST.get('phone', False)
    email = request.POST.get('email', False)

    extra_degree = request.POST.get('extra_degree', False)
    extra_title = request.POST.get('extra_title', False)
    extra_school = request.POST.get('extra_school', False)
    extra_degree_from = request.POST.get('extra_degree_from', False)
    extra_degree_to = request.POST.get('extra_degree_to', False)
    degree_description = request.POST.get('degree_description', False)

    education_external1={"extra_degree":extra_degree,"extra_title":extra_title,"extra_school":extra_school,"extra_degree_from":extra_degree_from,
                         "extra_degree_to":extra_degree_to,"degree_description":degree_description}

    basic={"location":location,"website":website,"phone":phone,"email":email}

    company_name = request.POST.get('company_name', False)
    company_position = request.POST.get('company_position', False)
    start_date = request.POST.get('start_date', False)
    end_date = request.POST.get('end_date', False)
    comments = request.POST.get('comments', False)

    experience_external1 = {"company_name": company_name, "company_position": company_position, "start_date": start_date,
                           "end_date": end_date,
                           "comments": comments}
    if form.is_valid():
        text = form.cleaned_data['Results']
        text = json.loads(text)
        if request.method == 'POST' and request.FILES:
            picture = request.FILES["picture"]
            fs = FileSystemStorage()
            name = picture.name
            name = name.replace(" ", "-")
            filename = fs.save(name, picture)
            uploaded_file_url = fs.url(filename)
            text['image_url'] = uploaded_file_url



        text['ratings']=ratings
        text['category'] = category


        text['basic']=basic
        text['education_external1'] = education_external1
        text['experience_external1'] = experience_external1
        text['id']=random.randint(10000, 210000) * 5

        resume.insert(text,check_keys=False)
        pass
    template = 'smart/parsed_result.html'
    context={'form': form}

    return render(request,template, context)