from django.shortcuts import render, redirect
from django.core.mail import send_mail
from . models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import make_password


def home(request):
    lockk = Restaurants.objects.filter(local_international = 'local')[:3]
    interk = Restaurants.objects.filter(local_international='international')[:3]
    abb = Aboutt.objects.all()
    o_p = Our_people.objects.all()
    mis = Mission.objects.all()
    vis = Vision.objects.all()
    w_c = Word_from_CEO.objects.all()
    return render(request,'tem/home_page2.html',{'lockk':lockk,'interk':interk,'abb':abb,'o_p':o_p,'mis':mis,'vis':vis,'w_c':w_c})


def abt_us(request):
    dvd = Aboutt.objects.all()
    return render(request,'tem/about_us.html',{'dvd':dvd})


def our_ple(request):
    dvd = Our_people.objects.all()
    return render(request,'tem/our_people.html',{'dvd':dvd})


def miss_ion(request):
    dvd = Mission.objects.all()
    return render(request,'tem/miss_ion.html',{'dvd':dvd})


def vis_ion(request):
    dvd = Vision.objects.all()
    return render(request,'tem/vis_ion.html',{'dvd':dvd})


def word_from_ceo(request):
    dvd = Word_from_CEO.objects.all()
    return render(request, 'tem/word_from_ceo.html',{'dvd':dvd})


def single_product(request, id):
    tgw = Restaurants.objects.get(id = id)
    loc_int = str(tgw.local_international)
    loc_int = loc_int.upper()
    kmk = int(tgw.id)
    request.session['single_pdt_resta'] = kmk
    ghg = Restaurant_images.objects.filter(img_resta = tgw)
    if loc_int == 'INTERNATIONAL':
        return render(request, 'tem/single_product1.html', {'tgw': tgw, 'ghg': ghg, 'loc_int': loc_int})
    return render(request, 'tem/single_product.html',{'tgw':tgw,'ghg':ghg,'loc_int':loc_int})


def website_unavailable(request):
    messages.success(request, 'Website unavailable')
    tgw = Restaurants.objects.get(id = request.session['single_pdt_resta'])
    redd = 'single_product/'+str(tgw.id)
    return redirect(redd)


def reser_unavailable(request):
    messages.success(request, 'Reservation unavailable')
    tgw = Restaurants.objects.get(id = request.session['single_pdt_resta'])
    redd = 'single_product/'+str(tgw.id)
    return redirect(redd)


def link_unavailable(request):
    tgw = Restaurants.objects.get(id = request.session['single_pdt_resta'])
    ghg = Restaurant_images.objects.filter(img_resta=tgw)
    messages.success(request, 'Reservation unavailable')
    return render(request, 'tem/single_product.html', {'tgw': tgw, 'ghg': ghg})


def link_unavailable1(request):
    messages.success(request, 'Link unavailable')
    return redirect('contact')


def restaurants(request):
    lockk = Restaurants.objects.filter(local_international='local')
    interk = Restaurants.objects.filter(local_international='international')
    return render(request,'tem/restaurants.html', {'lockk': lockk, 'interk': interk})


def reservation(request):
    return render(request, 'tem/home_page.html')


def careers(request):
    tft = Job_recruitment.objects.all()
    return render(request, 'tem/careerss1.html',{'tft':tft})


def contact(request):
    dvd = Contact_uss.objects.all()
    return render(request, 'tem/contact.html',{'dvd':dvd})


def book_table(request):
    email = "user09.wahylab@gmail.com"
    nam = request.POST.get('nam')
    emm = request.POST.get('emm')
    count = request.POST.get('count')
    dat = request.POST.get('dat')
    tim = request.POST.get('tim')
    t_a = 'Name: '+nam+', Email: '+emm+', Number of person: '+count+', Date: '+dat+', Time of arrival: '+tim+'.'
    send_mail('Table booking (Agthia)', t_a, email, [email], fail_silently=False)
    return redirect('home')


def contact_cust(request):
    tgt = Contact_uss.objects.all()
    to_emm = ''
    for t in tgt:
        emt = str(t.contact_email)
        to_emm += emt
        break
    email = "user09.wahylab@gmail.com"
    nam = request.POST.get('nam')
    emm = request.POST.get('emm')
    subj = request.POST.get('subj')
    phone = request.POST.get('phone')
    msg = request.POST.get('msg')
    t_a = 'Name: ' + nam + '\nEmail: ' + emm + '\nSubject: ' + subj + '\nPhone: ' + phone + '\nMessage: ' + msg + '.'
    send_mail('Customer message (Agthia)', t_a, email, [to_emm], fail_silently=False)
    messages.success(request, 'Mailed successfully')
    return redirect('contact')


def register_admin(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mgn = Registration.objects.all()
        for w in mgn:
            if w.user_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return redirect('register_admin')

        psw = request.POST.get('psw')
        user_name = request.POST.get('user_name')

        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('register_admin')

        user = User.objects.create_user(username=user_name, email=email, password=psw, first_name=first_name,last_name=last_name)
        user.save()

        reg = Registration()
        reg.password = psw
        reg.user_role = 'admin'
        reg.user = user
        reg.save()
        messages.success(request, 'You have successfully registered as admin')
        return redirect('home')
    else:
        return render(request, 'tem/register_admin.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username = username, password = password)
        if user is None:
            messages.success(request, 'Invalid credentials')
            return render(request, 'tem/login.html')
        auth.login(request, user)
        if Registration.objects.filter(user = user, password = password).exists():
            logs = Registration.objects.filter(user = user, password = password)
            for value in logs:
                user_id = value.id
                usertype  = value.user_role
                if usertype == 'admin':
                    request.session['logg'] = user_id
                    return redirect('admin_home')
                elif usertype == 'user':
                    request.session['logg'] = user_id
                    return redirect('user_home')
                else:
                    messages.success(request, 'Your access to the website is blocked. Please contact admin')
                    return redirect('login')
        else:
            messages.success(request, 'Username or password entered is incorrect')
            return redirect('login')
    else:
        return render(request, 'tem/login1.html')


@never_cache
@login_required
def admin_home(request):
    return render(request,'tem/admin_panel/index.html')


@never_cache
@login_required
def careers_adm(request):
    if request.method == 'POST':
        restaurantName = request.POST.get('restaurantName')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        salaryRange = request.POST.get('salaryRange')
        ageLimit = request.POST.get('ageLimit')
        employmentType = request.POST.get('employmentType')
        place = request.POST.get('place')
        gnk = Job_recruitment()
        gnk.restaurant = restaurantName
        gnk.department = department
        gnk.designation = designation
        gnk.salary_range = salaryRange
        gnk.age_limit = ageLimit
        gnk.employment_type = employmentType
        gnk.place = place
        gnk.save()
        messages.success(request,'Job details added successfully')
        return redirect('admin_home')
    return render(request, 'tem/careers_adm1.html')


@never_cache
@login_required
def view_vacancy_adm(request):
    hyh = Job_recruitment.objects.all()
    return render(request,'tem/view_vacancy_adm1.html',{'hyh':hyh})


@never_cache
@login_required
def delete_vacancy_adm(request, id):
    Job_recruitment.objects.get(id = id).delete()
    return redirect('view_vacancy_adm')


@never_cache
@login_required
def search_job(request):
    query = request.POST.get('srch')
    if query:
        results = Job_recruitment.objects.filter(Q(restaurant__icontains=query) | Q(department__icontains=query) |
                                                 Q(designation__icontains=query) | Q(salary_range__icontains=query) |
                                                 Q(age_limit__icontains=query) | Q(employment_type__icontains=query) |
                                                 Q(place__icontains=query) )
    else:
        results = Job_recruitment.objects.all()
    return render(request,'tem/view_vacancy_adm.html',{'hyh':results})


@never_cache
@login_required
def edit_vacancy_adm(request, id):
    gnk = Job_recruitment.objects.get(id = id)
    if request.method == 'POST':
        restaurantName = request.POST.get('restaurantName')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        salaryRange = request.POST.get('salaryRange')
        ageLimit = request.POST.get('ageLimit')
        employmentType = request.POST.get('employmentType')
        place = request.POST.get('place')
        gnk.restaurant = restaurantName
        gnk.department = department
        gnk.designation = designation
        gnk.salary_range = salaryRange
        gnk.age_limit = ageLimit
        gnk.employment_type = employmentType
        gnk.place = place
        gnk.save()
        messages.success(request, 'Job details edited successfully')
        return redirect('view_vacancy_adm')
    return render(request, 'tem/edit_vacancy_adm1.html', {'gh': gnk})


@never_cache
def apply_job(request, id):
    rkt = Job_recruitment.objects.get(id = id)
    if request.method == "POST":
        fullName = request.POST.get('fullName')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        resume = request.FILES['resume']
        fs = FileSystemStorage()
        resume_path = fs.save(resume.name, resume)

        gnk = Job_application()
        gnk.full_name = fullName
        gnk.phone = phone
        gnk.email = email
        gnk.address = address
        gnk.resume = resume_path
        gnk.apl_rec = rkt
        gnk.save()
        messages.success(request, 'Applied successfully')
        return redirect('home')
    return render(request, 'tem/apply_job.html',{'rkt':rkt})


@never_cache
@login_required
def view_job_apls(request):
    rkt = Job_application.objects.all()
    return render(request, 'tem/view_job_apls1.html', {'rkt': rkt})


@never_cache
@login_required
def search_job_apls(request):
    query = request.POST.get('srch')
    if query:
        rs_lst = []
        res = Job_recruitment.objects.filter(Q(restaurant__icontains=query) | Q(department__icontains=query) |
                                                 Q(designation__icontains=query) | Q(salary_range__icontains=query) |
                                                 Q(age_limit__icontains=query) | Q(employment_type__icontains=query) |
                                                 Q(place__icontains=query) )
        for t in res:
            gj = int(t.id)
            rs_lst.append(gj)
        results = Job_application.objects.filter(Q(full_name__icontains=query) | Q(phone__icontains=query) |
                                                 Q(email__icontains=query) | Q(address__icontains=query) |
                                                 Q(resume__icontains=query) | Q(apl_rec__in=rs_lst))
    else:
        results = Job_application.objects.all()
    return render(request, 'tem/view_job_apls1.html', {'rkt': results})


@never_cache
@login_required
def delete_apln_adm(request, id):
    Job_application.objects.get(id = id).delete()
    return redirect('view_job_apls')


def media_page(request):
    dvd = Latest_news.objects.all()
    return render(request, 'tem/media_page1.html',{'dvd':dvd})


@never_cache
@login_required
def mnge_restaurants_adm(request):
    hth = Restaurants.objects.all()
    return render(request, 'tem/mnge_restaurants_adm2.html',{'hth':hth})


@never_cache
@login_required
def descr_restau_adm(request, id):
    hth = Restaurants.objects.get(id = id)
    return render(request, 'tem/descr_restau_adm1.html', {'hth': hth})


@never_cache
@login_required
def descr_contact_adm(request, id):
    hth = Contact_uss.objects.get(id=id)
    return render(request, 'tem/descr_contact_adm.html', {'hth': hth})


@login_required
def images_restau_adm(request, id):
    request.session['restau_idd'] = int(id)
    jyg = Restaurants.objects.get(id = id)
    hyh = Restaurant_images.objects.filter(img_resta = jyg)
    return render(request, 'tem/images_restau_adm1.html', {'hyh': hyh})


@never_cache
@login_required
def edit_img_resta_adm(request, id):
    request.session['resta_img_idd'] = int(id)
    hyh = Restaurant_images.objects.get(id=id)
    if request.method == 'POST':
        try:
            resta_img = request.FILES['resta_img']
            image_path = os.path.join(settings.MEDIA_ROOT, hyh.image.path)
            if os.path.isfile(image_path):
                os.remove(image_path)

            fs = FileSystemStorage()
            image_path = fs.save(resta_img.name, resta_img)
            hyh.image = image_path
            hyh.save()
            resta_id = request.session['restau_idd']
            resta_id = int(resta_id)
            redd="/images_restau_adm/"+str(resta_id)
            return redirect(redd)
        except:
            resta_id = request.session['restau_idd']
            resta_id = int(resta_id)
            redd = "/images_restau_adm/" + str(resta_id)
            return redirect(redd)

    return render(request, 'tem/edit_img_resta_adm1.html', {'hyh': hyh})


@never_cache
@login_required
def delete_img_resta_adm(request, id):
    rty = request.session['restau_idd']
    rty = int(rty)
    Restaurant_images.objects.get(id = id).delete()
    redd = "/images_restau_adm/"+str(rty)
    return redirect(redd)


@never_cache
@login_required
def add_img_resta_adm(request):
    dtd = Restaurants.objects.get(id = request.session['restau_idd'])
    if request.method == 'POST':
        resta_img = request.FILES.get('resta_img')
        fs = FileSystemStorage()
        if resta_img:
            resta_img_path = fs.save(resta_img.name, resta_img)
        hyh = Restaurant_images()
        hyh.image = resta_img_path
        hyh.img_resta = dtd
        hyh.save()
        resta_id = int(dtd.id)
        redd = "/images_restau_adm/" + str(resta_id)
        return redirect(redd)
    return render(request,'tem/add_img_resta_adm1.html')


@never_cache
@login_required
def edit_resta_adm(request, id):
    dvd = Restaurants.objects.get(id = id)
    if request.method == 'POST':
        new_logo = request.FILES.get('new_logo')
        new_image = request.FILES.get('new_image')

        fs = FileSystemStorage()

        if new_logo:
            logo_path = os.path.join(settings.MEDIA_ROOT, dvd.logo.path)
            if os.path.isfile(logo_path):
                os.remove(logo_path)
            logo_path = fs.save(new_logo.name, new_logo)
            dvd.logo = logo_path

        if new_image:
            image_path = os.path.join(settings.MEDIA_ROOT, dvd.image.path)
            if os.path.isfile(image_path):
                os.remove(image_path)
            image_path = fs.save(new_image.name, new_image)
            dvd.image = image_path

        name = request.POST.get('name')
        brandType = request.POST.get('brandType')
        brand_parag = request.POST.get('brand_parag')
        brand_parag1 = request.POST.get('brand_parag1')
        res_url = request.POST.get('res_url')
        ins_url = request.POST.get('ins_url')
        fac_url = request.POST.get('fac_url')
        twi_url = request.POST.get('twi_url')
        dvd.name = name
        dvd.local_international = brandType
        dvd.brand_paragraph = brand_parag

        if brand_parag1 and (brand_parag1 != 'None'):
            dvd.brand_paragraph1 = brand_parag1
        else:
            dvd.brand_paragraph1 = None

        if res_url and (res_url != 'None'):
            dvd.url = res_url
        else:
            dvd.url = None

        if ins_url and (ins_url != 'None'):
            dvd.instagram_link = ins_url

        if fac_url and (fac_url != 'None'):
            dvd.facebook_link = fac_url

        if twi_url and (twi_url != 'None'):
            dvd.twitter_link = twi_url

        dvd.save()
        messages.success(request,'Restaurant details edited successfully')
        return redirect('mnge_restaurants_adm')

    return render(request,'tem/edit_resta_adm1.html',{'dvd':dvd})


@never_cache
@login_required
def delete_resta_adm(request, id):
    kmk = Restaurants.objects.get(id=id)
    logo_path = os.path.join(settings.MEDIA_ROOT, kmk.logo.path)
    if os.path.isfile(logo_path):
        os.remove(logo_path)
    image_path = os.path.join(settings.MEDIA_ROOT, kmk.image.path)
    if os.path.isfile(image_path):
        os.remove(image_path)
    Restaurants.objects.get(id=id).delete()
    messages.success(request,'Restaurant details deleted successfully')
    return redirect('mnge_restaurants_adm')


@never_cache
@login_required
def add_resta_adm(request):
    if request.method == 'POST':
        new_logo = request.FILES.get('new_logo')
        new_image = request.FILES.get('new_image')

        # File storage
        fs = FileSystemStorage()

        # Save the new logo and get its path
        if new_logo:
            logo_path = fs.save(new_logo.name, new_logo)

        # Save the new image and get its path
        if new_image:
            image_path = fs.save(new_image.name, new_image)

        name = request.POST.get('name')
        name = name.upper()
        brandType = request.POST.get('brandType')
        brand_parag = request.POST.get('brand_parag')
        brand_parag1 = request.POST.get('brand_parag1')
        res_url = request.POST.get('res_url')
        ins_url = request.POST.get('ins_url')
        fac_url = request.POST.get('fac_url')
        twi_url = request.POST.get('twi_url')
        dvd = Restaurants()
        dvd.logo = logo_path if new_logo else None
        dvd.image = image_path if new_image else None
        dvd.name = name
        dvd.local_international = brandType
        dvd.brand_paragraph = brand_parag
        if res_url:
            dvd.url = res_url
        else:
            dvd.url = None
        if brand_parag1:
            dvd.brand_paragraph1 = brand_parag1
        else:
            dvd.brand_paragraph1 = None

        if ins_url and (ins_url != 'None'):
            dvd.instagram_link = ins_url
        else:
            dvd.instagram_link = None

        if fac_url and (fac_url != 'None'):
            dvd.facebook_link = fac_url
        else:
            dvd.facebook_link = None

        if twi_url and (twi_url != 'None'):
            dvd.twitter_link = twi_url
        else:
            dvd.twitter_link = None

        dvd.save()
        messages.success(request,'Restaurant details added successfully')
        return redirect('mnge_restaurants_adm')
    return render(request, 'tem/add_resta_adm1.html')


@never_cache
@login_required
def search_resta(request):
    query = request.POST.get('srch')
    if query:
        results = Restaurants.objects.filter(Q(name__icontains=query) | Q(local_international__icontains=query) |
                                                 Q(brand_paragraph__icontains=query) )
    else:
        results = Restaurants.objects.all()
    return render(request,'tem/mnge_restaurants_adm2.html',{'hth':results})


def cust_subscr(request):
    emm = request.GET.get('emm')
    trt = Subscriptions()
    trt.email = emm
    trt.save()
    messages.success(request, 'Subscribed successfully')
    return redirect('home')


@never_cache
@login_required
def view_subscr_adm(request):
    hyh = Subscriptions.objects.all()
    return render(request, 'tem/view_subscr_adm1.html', {'hyh':hyh})


@never_cache
@login_required
def search_subscr(request):
    query = request.POST.get('srch')
    if query:
        results = Subscriptions.objects.filter(email__icontains=query)
    else:
        results = Subscriptions.objects.all()
    return render(request, 'tem/view_subscr_adm.html', {'hyh': results})


@never_cache
@login_required
def delete_subscr_adm(request, id):
    Subscriptions.objects.get(id = id).delete()
    messages.success(request, 'Email deleted successfully')
    return redirect('view_subscr_adm')


@never_cache
@login_required
def about_adm(request):
    hth = Aboutt.objects.all()
    return render(request, 'tem/about_adm2.html',{'hth':hth})


@never_cache
@login_required
def add_about_adm(request):
    if request.method == 'POST':
        dvd = Aboutt()
        about_parag = request.POST.get('about_parag')
        if about_parag and (about_parag != 'None'):
            dvd.description = about_parag

        about_parag1 = request.POST.get('about_parag1')
        if about_parag1 and (about_parag1 != 'None'):
            dvd.description1 = about_parag1

        dvd.save()
        return redirect('about_adm')
    return render(request, 'tem/add_about_adm1.html')


@never_cache
@login_required
def edit_about_adm(request, id):
    dvd = Aboutt.objects.get(id=id)
    if request.method == 'POST':
        about_parag = request.POST.get('about_parag')
        if about_parag and (about_parag != 'None'):
            dvd.description = about_parag

        about_parag1 = request.POST.get('about_parag1')
        if about_parag1 and (about_parag1 != 'None'):
            dvd.description1 = about_parag1

        dvd.save()
        return redirect('about_adm')

    return render(request, 'tem/edit_about_adm1.html', {'dvd': dvd})


@never_cache
@login_required
def delete_about_adm(request, id):
    Aboutt.objects.get(id=id).delete()
    return redirect('about_adm')


@never_cache
@login_required
def our_ple_adm(request):
    hth = Our_people.objects.all()
    return render(request, 'tem/our_ple_adm1.html',{'hth':hth})


@never_cache
@login_required
def add_our_ple_adm(request):
    if request.method == 'POST':
        dvd = Our_people()
        ourple_parag = request.POST.get('ourple_parag')
        if ourple_parag and (ourple_parag != 'None'):
            dvd.description = ourple_parag

        dvd.save()
        return redirect('our_ple_adm')
    return render(request, 'tem/add_our_ple_adm1.html')


@never_cache
@login_required
def edit_our_ple_adm(request, id):
    dvd = Our_people.objects.get(id=id)
    if request.method == 'POST':
        ourple_parag = request.POST.get('ourple_parag')
        if ourple_parag and (ourple_parag != 'None'):
            dvd.description = ourple_parag
        dvd.save()
        return redirect('our_ple_adm')

    return render(request, 'tem/edit_our_ple_adm1.html', {'dvd': dvd})


@never_cache
@login_required
def delete_our_ple_adm(request, id):
    Our_people.objects.get(id=id).delete()
    return redirect('our_ple_adm')


@never_cache
@login_required
def mission_adm(request):
    hth = Mission.objects.all()
    return render(request, 'tem/mission_adm1.html',{'hth':hth})


@never_cache
@login_required
def add_mission_adm(request):
    if request.method == 'POST':
        dvd = Mission()
        mission_parag = request.POST.get('mission_parag')
        if mission_parag and (mission_parag != 'None'):
            dvd.description = mission_parag

        dvd.save()
        return redirect('mission_adm')
    return render(request, 'tem/add_mission_adm1.html')


@never_cache
@login_required
def edit_mission_adm(request, id):
    dvd = Mission.objects.get(id=id)
    if request.method == 'POST':
        mission_parag = request.POST.get('mission_parag')
        if mission_parag and (mission_parag != 'None'):
            dvd.description = mission_parag
        dvd.save()
        return redirect('mission_adm')
    return render(request, 'tem/edit_mission_adm1.html', {'dvd': dvd})


@never_cache
@login_required
def delete_mission_adm(request, id):
    Mission.objects.get(id=id).delete()
    return redirect('mission_adm')



@never_cache
@login_required
def vision_adm(request):
    hth = Vision.objects.all()
    return render(request, 'tem/vision_adm1.html',{'hth':hth})


@never_cache
@login_required
def add_vision_adm(request):
    if request.method == 'POST':
        dvd = Vision()
        vision_parag = request.POST.get('vision_parag')
        if vision_parag and (vision_parag != 'None'):
            dvd.description = vision_parag
        dvd.save()
        return redirect('vision_adm')
    return render(request, 'tem/add_vision_adm1.html')


@never_cache
@login_required
def edit_vision_adm(request, id):
    dvd = Vision.objects.get(id=id)
    if request.method == 'POST':
        vision_parag = request.POST.get('vision_parag')
        if vision_parag and (vision_parag != 'None'):
            dvd.description = vision_parag
        dvd.save()
        return redirect('vision_adm')
    return render(request, 'tem/edit_vision_adm1.html', {'dvd': dvd})


@never_cache
@login_required
def delete_vision_adm(request, id):
    Vision.objects.get(id=id).delete()
    return redirect('vision_adm')


@never_cache
@login_required
def word_ceo_adm(request):
    hth = Word_from_CEO.objects.all()
    return render(request, 'tem/word_ceo_adm1.html',{'hth':hth})


@never_cache
@login_required
def add_word_ceo_adm(request):
    if request.method == 'POST':
        dvd = Word_from_CEO()
        wfc_parag = request.POST.get('wfc_parag')
        if wfc_parag and (wfc_parag != 'None'):
            dvd.description = wfc_parag
        dvd.save()
        return redirect('word_ceo_adm')
    return render(request, 'tem/add_word_ceo_adm1.html')


@never_cache
@login_required
def edit_word_ceo_adm(request, id):
    dvd = Word_from_CEO.objects.get(id=id)
    if request.method == 'POST':
        wfc_parag = request.POST.get('wfc_parag')
        if wfc_parag and (wfc_parag != 'None'):
            dvd.description = wfc_parag
        dvd.save()
        return redirect('word_ceo_adm')
    return render(request, 'tem/edit_word_ceo_adm1.html', {'dvd': dvd})


@never_cache
@login_required
def delete_word_ceo_adm(request, id):
    Word_from_CEO.objects.get(id = id).delete()
    return redirect('word_ceo_adm')

@never_cache
@login_required
def news_adm(request):
    hth = Latest_news.objects.all()
    return render(request, 'tem/news_adm1.html',{'hth':hth})


@never_cache
@login_required
def add_media_adm(request):
    if request.method == 'POST':
        dvd = Latest_news()
        media_title = request.POST.get('media_title')
        if media_title and (media_title != 'None'):
            dvd.news_title = media_title

        media_content = request.POST.get('media_content')
        if media_content and (media_content != 'None'):
            dvd.description = media_content

        dvd.save()
        return redirect('news_adm')
    return render(request, 'tem/add_media_adm1.html')


@never_cache
@login_required
def edit_media_adm(request, id):
    dvd = Latest_news.objects.get(id=id)
    if request.method == 'POST':
        media_title = request.POST.get('media_title')
        if media_title and (media_title != 'None'):
            dvd.news_title = media_title

        media_content = request.POST.get('media_content')
        if media_content and (media_content != 'None'):
            dvd.description = media_content

        dvd.save()
        return redirect('news_adm')
    return render(request, 'tem/edit_media_adm1.html', {'dvd': dvd})


@never_cache
@login_required
def delete_media_adm(request, id):
    Latest_news.objects.get(id = id).delete()
    return redirect('news_adm')


@never_cache
@login_required
def contact_us_adm(request):
    hth = Contact_uss.objects.all()
    return render(request, 'tem/contact_us_adm1.html', {'hth': hth})


@never_cache
@login_required
def add_contact_adm(request):
    if request.method == 'POST':
        titlee = request.POST.get('title')
        titlee = titlee.title()
        descr = request.POST.get('descr')
        plac = request.POST.get('plac')
        plac = plac.upper()
        emm = request.POST.get('emm')
        emm = emm.upper()
        phone = request.POST.get('phone')
        ins_url = request.POST.get('ins_url')
        fac_url = request.POST.get('fac_url')
        twi_url = request.POST.get('twi_url')
        pinn_url = request.POST.get('pinn_url')
        c_emm = request.POST.get('c_emm')
        dvd = Contact_uss()
        dvd.title = titlee
        dvd.description = descr
        dvd.place = plac
        dvd.email = emm
        dvd.phone = phone
        dvd.instagram_link = ins_url
        dvd.twitter_link = twi_url
        dvd.facebook_link = fac_url
        dvd.pinterest_link = pinn_url
        dvd.contact_email = c_emm
        dvd.save()
        messages.success(request, 'Contact details added successfully')
        return redirect('contact_us_adm')
    return render(request, 'tem/add_contact_adm1.html')


@never_cache
@login_required
def edit_contact_adm(request, id):
    dvd = Contact_uss.objects.get(id = id)
    if request.method == 'POST':
        titlee = request.POST.get('title')
        titlee = titlee.title()
        descr = request.POST.get('descr')
        plac = request.POST.get('plac')
        plac = plac.upper()
        emm = request.POST.get('emm')
        emm = emm.upper()
        phone = request.POST.get('phone')
        ins_url = request.POST.get('ins_url')
        fac_url = request.POST.get('fac_url')
        twi_url = request.POST.get('twi_url')
        pinn_url = request.POST.get('pinn_url')
        c_emm = request.POST.get('c_emm')

        dvd.title = titlee
        dvd.place = plac
        dvd.phone = phone
        dvd.email = emm
        dvd.contact_email = c_emm
        if descr and (descr != 'None'):
            dvd.description = descr
        else:
            dvd.description = None

        if ins_url and (ins_url != 'None'):
            dvd.instagram_link = ins_url

        if fac_url and (fac_url != 'None'):
            dvd.facebook_link = fac_url

        if twi_url and (twi_url != 'None'):
            dvd.twitter_link = twi_url

        if pinn_url and (pinn_url != 'None'):
            dvd.pinterest_link = pinn_url
        dvd.save()
        messages.success(request, 'Contact details edited successfully')
        return redirect('contact_us_adm')
    return render(request, 'tem/edit_contact_adm1.html',{'dvd':dvd})


@never_cache
@login_required
def delete_contact_adm(request, id):
    Contact_uss.objects.get(id=id).delete()
    return redirect('contact_us_adm')


@never_cache
@login_required
def change_pswd_adm(request):
    tdr = Registration.objects.get(id = request.session['logg'])
    rfy = tdr.user.pk
    um = User.objects.get(id=rfy)
    new_password = request.POST.get('new_password')
    passwords = make_password(new_password)
    u = User.objects.get(id=rfy)
    u.password = passwords
    u.save()
    user_name = str(um.username)
    user = auth.authenticate(username = user_name, password = new_password)
    auth.login(request, user)

    b = tdr.id
    m = int(b)
    request.session['logg'] = m

    tdr.password = new_password
    tdr.save()
    messages.success(request, 'Password changed successfully')
    return redirect('admin_home')


def logout(request):
    auth.logout(request)
    return redirect('home')
