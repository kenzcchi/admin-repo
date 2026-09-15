from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import ProviderVerification
from django.contrib import messages
from django.db import connection
from django.template.exceptions import TemplateDoesNotExist
import json

# ==========================================
# MOCK DATA FOR MESSAGES INBOX
# ==========================================
MOCK_CONVERSATIONS = [
    {
        'room_id': 'room_1001',
        'delivery_id': '1001',
        'sender': 'Jonel Jumawan',
        'provider': 'Jun Joseph Pestaño',
        'last_message': 'Please ensure contactless handover if possible.',
        'updated_at': '10:14 AM',
        'messages': [
            {'sender_id': 301, 'sender_name': 'Jonel Jumawan', 'sender_role': 'sender', 'message': 'Hello, is my delivery confirmed?', 'sent_at': '10:10 AM'},
            {'sender_id': 402, 'sender_name': 'Jun Joseph Pestaño', 'sender_role': 'provider', 'message': 'Yes, accepting it now.', 'sent_at': '10:12 AM'},
            {'sender_id': 0, 'sender_name': 'Admin', 'sender_role': 'admin', 'message': 'Please ensure contactless handover if possible.', 'sent_at': '10:14 AM'}
        ]
    },
    {
        'room_id': 'room_1002',
        'delivery_id': '1002',
        'sender': 'Kornel Jumao-as',
        'provider': 'Jun Joseph Pestaño',
        'last_message': 'Escrow frozen temporarily while investigating.',
        'updated_at': 'Yesterday',
        'messages': [
            {'sender_id': 402, 'sender_name': 'Jun Joseph Pestaño', 'sender_role': 'provider', 'message': 'Route is blocked due to roadwork.', 'sent_at': 'Yesterday 2:30 PM'},
            {'sender_id': 0, 'sender_name': 'Admin', 'sender_role': 'admin', 'message': 'Escrow frozen temporarily while investigating.', 'sent_at': 'Yesterday 2:40 PM'}
        ]
    }
]

def admin_login(request):
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

    if current_tab == 'verified':
        filtered_users = [u for u in mock_users if u['status1'] == 'Verified']
    elif current_tab == 'pending':
        filtered_users = [u for u in mock_users if u['status1'] == 'Pending']
    else:
        filtered_users = [u for u in mock_users if u['role'] == 'Provider']

    return render(request, 'pages/users.html', {
        'users': filtered_users,
        'current_tab': current_tab
    })

def provider_verification(request):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')

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
    
    if request.method == 'POST':
        action = request.POST.get('action')
        review_id = request.POST.get('review_id')

        if action == 'remove' and review_id:
            messages.success(request, f"Review #REV-{review_id} has been successfully removed.")
            
        elif action == 'resolve' and review_id:
            messages.success(request, f"Dispute for Review #REV-{review_id} has been marked as resolved.")

        return redirect(f"{request.path}?tab={current_tab}")

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
                    'status': 'Flagged' if row[1] <= 2 else 'Active'
                }
                
                reviews_list.append(item)
                if item['status'] == 'Flagged':
                    disputes_list.append(item)

    except Exception:
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

    context = {
        'current_tab': current_tab,
        'reviews_list': reviews_list,
        'disputes_list': disputes_list,
    }
    
    return render(request, 'pages/ratings_feedback.html', context)

def reports(request):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')

    current_tab = request.GET.get('tab', 'overview')
    selected_period = request.GET.get('period', 'this_month')

    delivery_type = request.GET.get('delivery_type', '')
    status_filter = request.GET.get('status', '')
    payment_method = request.GET.get('payment_method', '')
    role_filter = request.GET.get('role', '')
    proof_type = request.GET.get('proof_type', '')

    base_completed = 96
    base_net_revenue = 22780
    base_gmv = 152400
    base_total_req = 128

    period_multiplier = 1.0
    if selected_period == 'last_month':
        period_multiplier = 0.88
    elif selected_period == 'last_3_months':
        period_multiplier = 2.75
    elif selected_period == 'this_year':
        period_multiplier = 11.2

    active_filters = sum(1 for f in [delivery_type, status_filter, payment_method, role_filter, proof_type] if f)
    filter_factor = (0.75 ** active_filters) if active_filters > 0 else 1.0

    comp_deliveries = int(base_completed * period_multiplier * filter_factor)
    net_rev = int(base_net_revenue * period_multiplier * filter_factor)
    gmv = int(base_gmv * period_multiplier * filter_factor)
    total_req = int(base_total_req * period_multiplier * filter_factor)

    revenue_data = {
        'labels': ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        'gross_transactions': [int(82000 * period_multiplier), int(94500 * period_multiplier), int(108200 * period_multiplier), int(121400 * period_multiplier), int(138900 * period_multiplier), gmv],
        'net_revenue': [int(12400 * period_multiplier), int(14100 * period_multiplier), int(16800 * period_multiplier), int(18900 * period_multiplier), int(21600 * period_multiplier), net_rev]
    }

    context = {
        'current_tab': current_tab,
        'selected_period': selected_period,
        'delivery_type': delivery_type,
        'status_filter': status_filter,
        'payment_method': payment_method,
        'role_filter': role_filter,
        'proof_type': proof_type,
        'revenue_json': json.dumps(revenue_data),
        'ov_completed': str(comp_deliveries),
        'ov_net_revenue': f"₱{net_rev:,}",
        'del_total': str(total_req),
        'fin_gmv': f"₱{gmv:,}",
        'fin_net': f"₱{net_rev:,}",
    }
    
    return render(request, 'pages/reports.html', context)

def settings_page(request):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')

    settings_data = {
        'door_to_door': '20.00',
        'platform_commission': '8.5',
        'base_fare': '49.00',
        'per_km_rate': '14.50'
    }

    if request.method == 'POST':
        settings_data['door_to_door'] = request.POST.get('door_to_door', settings_data['door_to_door'])
        settings_data['platform_commission'] = request.POST.get('platform_commission', settings_data['platform_commission'])
        settings_data['base_fare'] = request.POST.get('base_fare', settings_data['base_fare'])
        settings_data['per_km_rate'] = request.POST.get('per_km_rate', settings_data['per_km_rate'])

        messages.success(request, 'Settings updated successfully!')

    return render(request, 'pages/settings.html', {
        'settings': settings_data
    })


def custom_logout(request):
    if 'is_mock_logged_in' in request.session:
        del request.session['is_mock_logged_in']
    return redirect('login')

# ==========================================
# RESTORED MESSAGES VIEWS
# ==========================================
def messages_view(request):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')
    
    current_tab = request.GET.get('tab', 'all')
    selected_room_id = request.GET.get('room_id') or (MOCK_CONVERSATIONS[0]['room_id'] if MOCK_CONVERSATIONS else '')
    
    conversations = MOCK_CONVERSATIONS
    if current_tab == 'active':
        conversations = [c for c in MOCK_CONVERSATIONS if '1002' in c['delivery_id']] 
        
    active_conversation = next((c for c in MOCK_CONVERSATIONS if c['room_id'] == selected_room_id), MOCK_CONVERSATIONS[0] if MOCK_CONVERSATIONS else None)

    context = {
        'conversations': conversations,
        'current_tab': current_tab,
        'active_room_id': selected_room_id,
        'active_conversation': active_conversation,
    }
    
    # Try finding the template in /pages/ first, fallback to root if not found
    try:
        return render(request, 'pages/messages.html', context)
    except TemplateDoesNotExist:
        return render(request, 'messages.html', context)

def message_thread_api(request, room_id):
    if not request.session.get('is_mock_logged_in'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    conv = next((c for c in MOCK_CONVERSATIONS if c['room_id'] == str(room_id) or c['room_id'] == f"room_{room_id}"), None)
    if not conv:
        return JsonResponse({'messages': [], 'delivery_id': 0})
        
    return JsonResponse({
        'room_id': conv['room_id'],
        'delivery_id': conv['delivery_id'],
        'sender': conv['sender'],
        'provider': conv['provider'],
        'messages': conv['messages']
    })

def send_message_api(request, room_id):
    if not request.session.get('is_mock_logged_in'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_text = data.get('message', '').strip()
            if not message_text:
                return JsonResponse({'error': 'Empty message'}, status=400)
                
            conv = next((c for c in MOCK_CONVERSATIONS if c['room_id'] == str(room_id) or c['room_id'] == f"room_{room_id}"), None)
            if conv:
                new_msg = {
                    'sender_id': 0,
                    'sender_name': 'Admin',
                    'sender_role': 'admin',
                    'message': message_text,
                    'sent_at': 'Just now'
                }
                conv['messages'].append(new_msg)
                conv['last_message'] = message_text
                conv['updated_at'] = 'Just now'
                return JsonResponse({'status': 'success', 'message': new_msg})
                
            return JsonResponse({'error': 'Room not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid method'}, status=405)


def admin_support_view(request):
    if not request.session.get('is_mock_logged_in'):
        return redirect('login')

    # Try finding the template in /pages/ first, fallback to root if not found
    try:
        return render(request, 'pages/admin_support_inbox.html')
    except TemplateDoesNotExist:
        return render(request, 'admin_support_inbox.html')