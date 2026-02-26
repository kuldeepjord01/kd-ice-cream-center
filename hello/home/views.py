from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from home.models import Contact, Order


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        message = request.POST.get("message")
        
        contact = Contact(name=name, email=email, number=number, message=message)
        contact.save()
        messages.success(request, f"Thank you {name}! We received your message and will get back to you soon.")
        return redirect("contact")
    
    return render(request, "contact.html")


@login_required
def order(request):
    if request.method == "POST":
        flavor = request.POST.get("flavor")
        if flavor:
            Order(user=request.user, flavor=flavor).save()
            messages.success(request, f"🎉 Your order for {flavor} has been placed! Thank you for choosing KD Ice Cream.")
        return redirect("home")
    return redirect("home")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        
        # Validation
        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, "signup.html")
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")
        
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, "signup.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already taken.")
            return render(request, "signup.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "signup.html")
        
        # Create user and auto-login
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f"Welcome to KD Ice Cream, {username}! Your account has been created.")
        return redirect("home")
    
    return render(request, "signup.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        
        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, "login.html")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            # Redirect to 'next' param if it exists (from @login_required)
            next_url = request.GET.get("next") or request.POST.get("next") or "home"
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")
    
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("home")


def services(request):
    return render(request, "services.html")


def search(request):
    query = request.GET.get("q", "").strip().lower()
    results = []
    
    # Define all flavors with name, description, price
    all_flavors = [
        ("Chocolate", "Rich and indulgent chocolate ice cream made from premium cocoa", 80),
        ("Strawberry", "A delightful blend of sweet and tart, made with real strawberries", 90),
        ("Butterscotch", "Creamy butterscotch with rich caramelized butter and brown sugar", 85),
        ("Vanilla Softy", "Classic smooth vanilla softy cone — light, creamy, and refreshing", 40),
        ("Strawberry Softy", "Fruity strawberry softy with a vibrant pink swirl", 45),
        ("Chocolate Softy", "Rich chocolate softy swirl — for chocolate lovers", 45),
        ("Classic Family Pack", "500ml pack with your choice of any 2 flavors", 250),
        ("Super Family Pack", "1L pack with your choice of any 3 flavors", 450),
        ("Mega Family Pack", "2L pack with all flavors included", 800),
    ]
    
    if query:
        results = [f for f in all_flavors if query in f[0].lower() or query in f[1].lower()]
    
    context = {
        "query": query,
        "results": results,
    }
    return render(request, "search.html", context)
