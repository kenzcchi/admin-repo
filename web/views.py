from django.shortcuts import render, redirect, get_object_or_404
from .models import ProviderVerification
from django.contrib import messages
from django.db import connection
import json

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

    current_tab = request.GET.get('tab', 'active')

    mock_escrow_list = [
        {
            'id': 'EID501',
            'delivery_id': '1001',
            'sender_id': 'USR-201',
            'provider_id': 'PRV-501',
            'amount': '₱250.00',
            'status': 'On Hold',
            'bc_escrow_tx_hash': '0x71c...a89f',
            'emergency_frozen': False,
            'created_at': '2026-03-28 10:15 AM'
        },
        {
            'id': 'EID502',
            'delivery_id': '1002',
            'sender_id': 'USR-204',
            'provider_id': 'PRV-503',
            'amount': '₱180.00',
            'status': 'Frozen',
            'bc_escrow_tx_hash': '0x32b...f11e',
            'emergency_frozen': True,
            'created_at': '2026-03-27 02:40 PM'
        },
        {
            'id': 'EID503',
            'delivery_id': '1003',
            'sender_id': 'USR-210',
            'provider_id': 'PRV-508',
            'amount': '₱220.00',
            'status': 'Released',
            'bc_escrow_tx_hash': '0x88f...c401',
            'emergency_frozen': False,
            'created_at': '2026-03-26 09:10 AM'
        },
    ]

    mock_transactions = [
        {
            'id': 'TID101',
            'escrow_id': 'EID501',
            'delivery_id': '1001',
            'base_amount': '₱200.00',
            'service_fee': '₱30.00',
            'penalty_fee': '₱20.00',
            'total_amount': '₱250.00',
            'method': 'GCash',
            'status': 'On Hold',
            'processed_at': '2026-03-28 10:16 AM'
        },
        {
            'id': 'TID102',
            'escrow_id': 'EID502',
            'delivery_id': '1002',
            'base_amount': '₱150.00',
            'service_fee': '₱30.00',
            'penalty_fee': '₱0.00',
            'total_amount': '₱180.00',
            'method': 'GCash',
            'status': 'Frozen',
            'processed_at': '2026-03-27 02:42 PM'
        },
        {
            'id': 'TID103',
            'escrow_id': 'EID503',
            'delivery_id': '1003',
            'base_amount': '₱190.00',
            'service_fee': '₱30.00',
            'penalty_fee': '₱0.00',
            'total_amount': '₱220.00',
            'method': 'GCash',
            'status': 'Completed',
            'processed_at': '2026-03-26 09:12 AM'
        },
    ]

    return render(request, 'pages/escrow_payments.html', {
        'current_tab': current_tab,
        'escrow_list': mock_escrow_list,
        'transactions': mock_transactions,
    })


def ratings_feedback(request):
    current_tab = request.GET.get('tab', 'overview')
    
    # ------------------------------------------------------------------
    # 1. HANDLE POST ACTIONS (Remove Review / Resolve Dispute)
    # ------------------------------------------------------------------
    if request.method == 'POST':
        action = request.POST.get('action')
        review_id = request.POST.get('review_id')

        if action == 'remove' and review_id:
            # Example raw SQL or ORM deletion:
            # with connection.cursor() as cursor:
            #     cursor.execute("DELETE FROM ratings_reviews WHERE review_id = %s", [review_id])
            messages.success(request, f"Review #REV-{review_id} has been successfully removed.")
            
        elif action == 'resolve' and review_id:
            # Example update status if you have a status/flagged column:
            # with connection.cursor() as cursor:
            #     cursor.execute("UPDATE ratings_reviews SET status = 'Active' WHERE review_id = %s", [review_id])
            messages.success(request, f"Dispute for Review #REV-{review_id} has been marked as resolved.")

        return redirect(f"{request.path}?tab={current_tab}")

    # ------------------------------------------------------------------
    # 2. FETCH DATA FROM DATABASE OR FALLBACK MOCK DATA
    # ------------------------------------------------------------------
    reviews_list = []
    disputes_list = []

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    review_id, 
                    rating, 
                    review_text, 
                    bc_rating_tx_hash, 
                    delivery_id, 
                    reviewer_id, 
                    reviewee_id, 
                    created_at 
                FROM ratings_reviews 
                ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()

            for row in rows:
                item = {
                    'review_id': row[0],
                    'rating': row[1],
                    'review_text': row[2],
                    'bc_rating_tx_hash': row[3],
                    'delivery_id': row[4],
                    'reviewer_id': row[5],
                    'reviewee_id': row[6],
                    'created_at': row[7].strftime('%Y-%m-%d') if row[7] else '—',
                    'status': 'Flagged' if row[1] <= 2 else 'Active'  # Example condition for demo
                }
                
                reviews_list.append(item)
                if item['status'] == 'Flagged':
                    disputes_list.append(item)

    except Exception:
        # Fallback sample data matching your schema fields if DB table is empty or unpopulated
        reviews_list = [
            {
                'review_id': 101,
                'rating': 2,
                'review_text': 'Package left at wrong location and delayed by 2 hours.',
                'bc_rating_tx_hash': '0x8f2a9b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a',
                'delivery_id': 5001,
                'reviewer_id': 301,
                'reviewee_id': 402,
                'created_at': '2026-03-28',
                'status': 'Flagged'
            },
            {
                'review_id': 102,
                'rating': 1,
                'review_text': 'Very unprofessional handler. Item box was dented.',
                'bc_rating_tx_hash': '0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b',
                'delivery_id': 5002,
                'reviewer_id': 302,
                'reviewee_id': 403,
                'created_at': '2026-03-27',
                'status': 'Flagged'
            },
            {
                'review_id': 103,
                'rating': 5,
                'review_text': 'Very careful with my package. Arrived earlier than expected!',
                'bc_rating_tx_hash': '0x3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d',
                'delivery_id': 5003,
                'reviewer_id': 303,
                'reviewee_id': 403,
                'created_at': '2026-03-26',
                'status': 'Active'
            },
        ]
        
        disputes_list = [r for r in reviews_list if r['status'] == 'Flagged']

    # ------------------------------------------------------------------
    # 3. RENDER TEMPLATE
    # ------------------------------------------------------------------
    context = {
        'current_tab': current_tab,
        'reviews_list': reviews_list,
        'disputes_list': disputes_list,
    }
    
    return render(request, 'pages/ratings_feedback.html', context)

def reports(request):
    selected_month = request.GET.get('month', 'October')

    revenue_data = {
        'labels': ['5k', '10k', '15k', '20k', '25k', '30k', '35k', '40k', '45k', '50k', '55k', '60k'],
        'gross_transactions': [22, 32, 30, 28, 52, 38, 88, 40, 64, 36, 54, 18],
        'net_revenue': [20, 68, 38, 30, 42, 50, 30, 54, 25, 48, 88, 20]
    }

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(total_amount), 0) AS total_gtv,
                    COALESCE(SUM(service_fee), 0) AS total_net
                FROM transactions 
                WHERE escrow_status = 'Released'
            """)
            row = cursor.fetchone()
            
            cursor.execute("SELECT COUNT(*) FROM deliveries WHERE delivery_status = 'Completed'")
            completed_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) 
                FROM deliveries 
                WHERE tx_pickup_hash IS NOT NULL AND tx_dropoff_hash IS NOT NULL
            """)
            verified_blockchain_count = cursor.fetchone()[0]

    except Exception:
        row = (184250, 27637)
        completed_count = 1420
        verified_blockchain_count = 1412

    context = {
        'selected_month': selected_month,
        'revenue_json': json.dumps(revenue_data),
        'total_gtv': f"₱{row[0]:,.2f}" if row and row[0] else "₱0.00",
        'net_revenue': f"₱{row[1]:,.2f}" if row and row[1] else "₱0.00",
        'completed_deliveries': f"{completed_count:,}",
        'blockchain_proofs': f"{verified_blockchain_count:,}",
    }
    
    return render(request, 'pages/reports.html', context)

def settings_page(request):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')

    # Default initial values
    settings_data = {
        'door_to_door': '20.00',
        'platform_commission': '8.5',
        'base_fare': '49.00',
        'per_km_rate': '14.50'
    }

    if request.method == 'POST':
        # Grab updated values from form submit
        settings_data['door_to_door'] = request.POST.get('door_to_door', settings_data['door_to_door'])
        settings_data['platform_commission'] = request.POST.get('platform_commission', settings_data['platform_commission'])
        settings_data['base_fare'] = request.POST.get('base_fare', settings_data['base_fare'])
        settings_data['per_km_rate'] = request.POST.get('per_km_rate', settings_data['per_km_rate'])

        # Show success toast or message
        messages.success(request, 'Settings updated successfully!')

    return render(request, 'pages/settings.html', {
        'settings': settings_data
    })


def custom_logout(request):
    if 'is_mock_logged_in' in request.session:
        del request.session['is_mock_logged_in']
    return redirect('login')

def messages_view(request):
    conversations = []
    current_tab = request.GET.get('tab', 'all')
    context = {
        'conversations': conversations,
        'current_tab': current_tab,
    }
    return render(request, 'messages.html', context)

def message_thread_api(request, room_id):
    return JsonResponse({'messages': [], 'delivery_id': 0})

def send_message_api(request, room_id):
    return JsonResponse({'status': 'success'})