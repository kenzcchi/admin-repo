from django.shortcuts import render, redirect

def admin_login(request):
    # If already logged in, go straight to the dashboard
    if request.session.get('is_mock_logged_in'):
        return redirect('dashboard')
        
    error_message = None
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        if u == 'admin' and p == 'admin':
            request.session['is_mock_logged_in'] = True
            return redirect('dashboard')
        else:
            error_message = "Invalid credentials. Please use admin / admin."
            
    return render(request, 'pages/login.html', {'error_message': error_message})


def dashboard(request):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')
    return render(request, 'pages/dashboard.html')


def users_page(request):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')

    current_tab = request.GET.get('tab', 'all')

    # Updated mock data: All are now Providers, and Pending providers default to 'Inactive'
    mock_users = [
        {
            'id': 'USI1', 'name': 'Rendell James Luminous', 'email': 'rjlumindas@gmail.com',
            'role': 'Provider', 'status1': 'Pending', 'status2': 'Inactive',
            'phone': '09223567589', 'addr_primary': 'Poblacion, Jagna, Bohol', 
            'addr_other': 'Mabini Street, corner of Vicente Gullas Street, Cebu City'
        },
        {
            'id': 'USI2', 'name': 'Jun Joseph Pestaño', 'email': 'junjlabdan@gmail.com',
            'role': 'Provider', 'status1': 'Verified', 'status2': 'Active',
            'phone': '09123456789', 'addr_primary': 'Talamban, Cebu City', 
            'addr_other': 'None'
        },
        {
            'id': 'USI3', 'name': 'Moises Padriga', 'email': 'seawater@gmail.com',
            'role': 'Provider', 'status1': 'Pending', 'status2': 'Inactive',
            'phone': '09334567890', 'addr_primary': 'Mandaue City', 
            'addr_other': 'None'
        },
        {
            'id': 'USI4', 'name': 'Bryan Nikole Dionson', 'email': 'driandionson@gmail.com',
            'role': 'Provider', 'status1': 'Pending', 'status2': 'Inactive',
            'phone': '09445678901', 'addr_primary': 'Lapu-Lapu City', 
            'addr_other': 'None'
        }
    ]

    # Filter data based on the selected tab
    if current_tab == 'verified':
        filtered_users = [u for u in mock_users if u['status1'] == 'Verified']
    elif current_tab == 'pending':
        filtered_users = [u for u in mock_users if u['status1'] == 'Pending']
    else:
        # Show all providers for the "All Providers" tab
        filtered_users = [u for u in mock_users if u['role'] == 'Provider']

    return render(request, 'pages/users.html', {
        'users': filtered_users,
        'current_tab': current_tab
    })
    
# Generic placeholder view for other sections so routing works perfectly
def generic_admin_page(request, title):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')
    return render(request, 'pages/generic_placeholder.html', {'page_title': title})

def provider_verification(request):
    return generic_admin_page(request, 'Provider Verification')

def vehicle_documents(request):
    return generic_admin_page(request, 'Vehicle Documents')

def deliveries(request):
    return generic_admin_page(request, 'Deliveries')

def escrow_payments(request):
    return generic_admin_page(request, 'Escrow & Payments')

def transactions(request):
    return generic_admin_page(request, 'Transactions')

def ratings_feedback(request):
    return generic_admin_page(request, 'Ratings and Feedback')

def reports(request):
    return generic_admin_page(request, 'Reports')

def settings_page(request):
    return generic_admin_page(request, 'Settings')


def custom_logout(request):
    if 'is_mock_logged_in' in request.session:
        del request.session['is_mock_logged_in']
    return redirect('login')