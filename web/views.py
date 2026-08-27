from django.shortcuts import render, redirect, get_object_or_404
from .models import ProviderVerification

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

#Provider-Verification    
def provider_verification(request):
# Enforce mock session check matching users_page pattern
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')

    # Mock provider verification data
    mock_verifications = [
        {
            'id': 1,
            'name': 'John David Torres Villanueva',
            'id_photo': '/media/verifications/ids/sample1.jpg',
            'selfie': '/media/verifications/selfies/sample1.jpg',
            'plate_no': 'ABCD-123',
            'vehicle_type': 'Sedan',
            'vehicle_doc': '/media/verifications/docs/orcr_john.pdf',
            'vehicle_doc_name': 'orcr_john.pdf',
            'status': 'Pending'
        },
        {
            'id': 2,
            'name': 'Bryan Nikole Dionson',
            'id_photo': '/media/verifications/ids/sample2.jpg',
            'selfie': '/media/verifications/selfies/sample2.jpg',
            'plate_no': 'EFGH-456',
            'vehicle_type': 'SUV',
            'vehicle_doc': '/media/verifications/docs/orcr_bryan.pdf',
            'vehicle_doc_name': 'orcr_bryan.pdf',
            'status': 'Pending'
        }
    ]
    
    return render(request, 'pages/provider_verification.html', {
        'verifications': mock_verifications
    })

def approve_provider(request, pk):
    if request.method == 'POST':
        verification = get_object_or_404(ProviderVerification, pk=pk)
        verification.status = 'Approved'
        verification.save()
    return redirect('provider_verification')

def reject_provider(request, pk):
    if request.method == 'POST':
        verification = get_object_or_404(ProviderVerification, pk=pk)
        verification.status = 'Rejected'
        verification.save()
    return redirect('provider_verification')

def deliveries(request):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')

    mock_deliveries = [
        {
            'id': '1001',
            'sender': 'Jonel Jumawan',
            'provider': 'Jun Joseph Pestaño',
            'status': 'Pending',
            'emergency': 'Normal',
            'escrow_status': 'On Hold'
        },
        {
            'id': '1002',
            'sender': 'Kornel Jumao-as',
            'provider': 'Jun Joseph Pestaño',
            'status': 'Accepted',
            'emergency': 'Frozen',
            'escrow_status': 'Frozen'
        },
        {
            'id': '1003',
            'sender': 'Alucard Jungler',
            'provider': 'Moises Padriga',
            'status': 'In Transit',
            'emergency': 'Normal',
            'escrow_status': 'On Hold'
        },
        {
            'id': '1004',
            'sender': 'Hilda Roamer',
            'provider': 'Moises Padriga',
            'status': 'Completed',
            'emergency': 'Normal',
            'escrow_status': 'Released'
        },
    ]

    return render(request, 'pages/deliveries.html', {
        'deliveries': mock_deliveries
    })

# Generic placeholder view for other sections so routing works perfectly
def generic_admin_page(request, title):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')
    return render(request, 'pages/generic_placeholder.html', {'page_title': title})


def escrow_payments(request):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')

    # Get the active sub-tab from URL query parameters (defaults to 'active')
    current_tab = request.GET.get('tab', 'active')

    mock_escrow = [
        {'id': 'EID501', 'delivery_id': '1001', 'amount': '₱250', 'status': 'On Hold'},
        {'id': 'EID502', 'delivery_id': '1002', 'amount': '₱180', 'status': 'Frozen'},
        {'id': 'EID503', 'delivery_id': '1003', 'amount': '₱220', 'status': 'Released'},
    ]

    mock_transactions = [
        {'id': 'TID101', 'delivery_id': '1001', 'amount': '₱250', 'method': 'GCash', 'status': 'On Hold', 'date': '2026-03-28'},
        {'id': 'TID102', 'delivery_id': '1002', 'amount': '₱180', 'method': 'GCash', 'status': 'Frozen', 'date': '2026-03-27'},
        {'id': 'TID103', 'delivery_id': '1003', 'amount': '₱220', 'method': 'GCash', 'status': 'Completed', 'date': '2026-03-26'},
    ]

    return render(request, 'pages/escrow.html', {
        'current_tab': current_tab,
        'escrow_list': mock_escrow,
        'transactions': mock_transactions,
    })


def ratings_feedback(request):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')

    current_tab = request.GET.get('tab', 'ratings')

    mock_reviews = [
        {
            'rating': 2,
            'stars_filled': [1, 2],
            'stars_empty': [1, 2, 3],
            'provider': 'Moises P.',
            'comment': 'Package left at wrong curb...',
            'flagged': True,
            'date': '2026-03-28'
        },
        {
            'rating': 1,
            'stars_filled': [1],
            'stars_empty': [1, 2, 3, 4],
            'provider': 'Jun Joseph P.',
            'comment': 'Very unprofessional, did not...',
            'flagged': True,
            'date': '2026-03-27'
        },
        {
            'rating': 5,
            'stars_filled': [1, 2, 3, 4, 5],
            'stars_empty': [],
            'provider': 'Jun Joseph P.',
            'comment': 'Very careful with my boxex,...',
            'flagged': False,
            'date': '2026-03-26'
        },
    ]

    mock_disputes = [
        {
            'id': 'DSP-1042',
            'delivery_id': '1001',
            'reported_by': 'Jonel Jumawan - Sender',
            'issue_type': 'Damaged Item',
            'status': 'Pending'
        },
        {
            'id': 'DSP-1032',
            'delivery_id': '1001',
            'reported_by': 'Jun Joseph Pestaño -Sender',
            'issue_type': 'Missing Package',
            'status': 'Resolved'
        },
        {
            'id': 'DSP-1022',
            'delivery_id': '1003',
            'reported_by': 'Bryan Dionson - Provider',
            'issue_type': 'Unprofessional Conduct',
            'status': 'In Review'
        },
    ]

    return render(request, 'pages/ratings_feedback.html', {
        'current_tab': current_tab,
        'reviews': mock_reviews,
        'disputes': mock_disputes,
    })

def reports(request):
    return generic_admin_page(request, 'Reports')

def settings_page(request):
    return generic_admin_page(request, 'Settings')


def custom_logout(request):
    if 'is_mock_logged_in' in request.session:
        del request.session['is_mock_logged_in']
    return redirect('login')