from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import requests

from ConstructTech.credentials import LipanaMpesaPpassword, MpesaAccessToken
from .models import UploadedImage
from ConstructTech.forms import QuoteForm
from .models import Contact
from .models import Quote
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def services(request):
    return render(request, 'services.html')
def projects(request):
    return render(request, 'projects.html')

@login_required
def contact(request):
    if request.method == 'POST':
        contact = Contact(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            Subject = request.POST.get('Subject'),
            Message = request.POST.get('Message'),
        )
        contact.save()
        # Redirect to a page after saving
        return redirect('ConstructTech:index')  # Adjust the redirect to your desired page
    else:
        return render(request, 'contact.html')
    



@login_required  # Ensure only logged-in users can access this view
def request_quote(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database and associate with the logged-in user
        quote = Quote(
            name=name, 
            email=email, 
            phone=phone, 
            subject=subject, 
            message=message, 
            user=request.user  # Assign the logged-in user
        )
        quote.save()

        # Redirect to a thank-you page or show a confirmation
        return redirect('ConstructTech:index')  # Adjust to your desired redirect

    return render(request, 'request_quote.html')

# Check if the user is an admin

# Show quotes (users see their quotes; admins see all)
@login_required
def show_quote(request):
    if request.user.is_superuser:  # Admin sees all quotes
        quotes = Quote.objects.all()
    else:  # Regular users see only their own quotes
        quotes = Quote.objects.filter(user=request.user)
    return render(request, 'show_quote.html', {'quotes': quotes})

# Update a quote (users can update their quotes; admins can update any quote)
@login_required
def update_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    
    # Allow admins to edit any quote or restrict users to their own quotes
    if not request.user.is_superuser and quote.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this quote.")

    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            return redirect('ConstructTech:show_quote')  # Adjust with your URL namespace
    else:
        form = QuoteForm(instance=quote)

    return render(request, 'update_quote.html', {'form': form})

# Delete a quote (users can delete their quotes; admins can delete any quote)
@login_required
def delete_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    
    # Allow admins to delete any quote or restrict users to their own quotes
    if not request.user.is_superuser and quote.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this quote.")

    if request.method == 'POST':
        quote.delete()
        return redirect('ConstructTech:show_quote')
    else:
        return HttpResponseForbidden("Invalid request method.")

# Check if the user is an admin
def is_admin(user):
    return user.is_superuser

@login_required  # Ensures that the user is logged in
@user_passes_test(is_admin)  # Only allow access if the user is an admin
def upload_image(request):


    if request.method == 'POST':
        # Retrieve data from the form
        title = request.POST.get('title')
        uploaded_file = request.FILES.get('image')

        if title and uploaded_file:
            # Save the file using FileSystemStorage
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(filename)

            # Save file information to the database
            image = UploadedImage.objects.create(title=title, image=filename)
            image.save()

            return render(request, 'upload_success.html', {'file_url': file_url})
        else:
            return render(request, 'upload_image.html', {'error': 'Please provide both a title and an image.'})

    return render(request, 'upload_image.html')


#  Adding the mpesa functions

#Display the payment form
def pay(request):
   """ Renders the form to pay """
   return render(request, 'pay.html')


# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = '1mw4dSX2lhZbkNCpiMVxgAtIrjGkEVRSrOxHU5Yzra570aAt'
    consumer_secret = 'BfqJhXNGu4wObGJaJ9MYeGZBZLoGAgpAUznOOMsfgrosV7gGpArWJEvAr1BU6QAV'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuthHandler(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request):
    """ Sends the stk push prompt """
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")