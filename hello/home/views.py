from django.shortcuts import redirect, render
from django.contrib import messages
from home.models import Contact, Order


def index(request):
    context = {
        "name": "King",
        "age": 22,
        "hobbies": ["Reading", "Traveling", "Gaming"],
    }
    return render(request, "index.html", context)


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


def order(request):
    if request.method == "POST":
        flavor = request.POST.get("flavor")
        if flavor:
            Order(flavor=flavor).save()
            messages.success(request, f"🎉 Your order for {flavor} has been placed! Thank you for choosing KD Ice Cream.", extra_tags="success")
        return redirect("home")
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
