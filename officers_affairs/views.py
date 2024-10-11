from datetime import date, datetime
from django.contrib import messages
from venv import logger
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Case, When, Value, IntegerField
from django.db.models.functions import Cast


from .models import *
from .forms import BranchForm,  JobForm, LeaveRequestForm, OffUnitStatusForm, OfficerForm, OfficerStatusForm,RankForm, SectionForm, UnitForm, WeaponForm
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy, reverse
import json
from . import filters
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.db.models import Q
from django.utils import timezone
import re

def extract_numeric(s):
    # Extract the numeric part of the string using regular expressions
    numbers = re.findall(r'\d+', s)
    return int(numbers[0]) if numbers else float('inf')  # Return infinity if no number is found

@permission_required('officers_affairs.view_rank', raise_exception=True)
def officers_home_view(request):
    today = timezone.localtime().date()
    # Count officers with the status 'موجود', currently outside, and with a different status
    total_officers = Officer.objects.filter(status__name='قوة').count()
    inside_officers = DailyAttendance.objects.filter(status__name='موجود',date=today).count()
    outside_officers = DailyAttendance.objects.exclude(status__name='موجود').filter(date=today).count()
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    if request.method == 'POST':
        # Check which form was submitted
        if 'add_weapon' in request.POST:
            add_weapon = WeaponForm(request.POST)
            if add_weapon.is_valid():
                add_weapon.save()
                return redirect('home')  # Redirect after form submission        

        if 'add_unit' in request.POST:
            add_unit = UnitForm(request.POST)
            if add_unit.is_valid():
                add_unit.save()
                return redirect('home')  # Redirect after form submission
            
        if 'add_branch' in request.POST:
            add_branch = BranchForm(request.POST)
            if add_branch.is_valid():
                add_branch.save()
                return redirect('home')  # Redirect after form submission
            
            
        if 'add_section' in request.POST:
            add_section = SectionForm(request.POST)
            if add_section.is_valid():
                add_section.save()
                return redirect('home')  # Redirect after form submission
 
        if 'add_job' in request.POST:
            add_job = JobForm(request.POST)
            if add_job.is_valid():
                add_job.save()
                return redirect('home')  # Redirect after form submission            
            
        if 'add_rank' in request.POST:
            add_rank = RankForm(request.POST, request.FILES)
            if add_rank.is_valid():
                add_rank.save()
                return redirect('home')  # Redirect after form submission
        
        elif 'add_off_unit_status' in request.POST:
            add_off_unit_status = OffUnitStatusForm(request.POST)
            if add_off_unit_status.is_valid():
                add_off_unit_status.save()
                return redirect('home')  # Redirect after form submission
        
        elif 'add_off_status' in request.POST:
            add_off_status = OfficerStatusForm(request.POST)
            if add_off_status.is_valid():
                add_off_status.save() 
                return redirect('home')  # Redirect after form submission           
            
    officerFilterDefault = {
        'status': OfficerStatus.objects.filter(name="قوة"),
    }

    context= {
        'ranks':Rank.objects.all(),
        'form': OfficerForm(),
        'officers_filter': filters.OfficerFilter(request.GET or officerFilterDefault),
        'count_officers_total': Officer.objects.count(),
        'count_officers_availble': Officer.objects.filter(unit_status__name="موجود").count(),
        'formweapon':WeaponForm(),
        'formunit':UnitForm(),
        'formbranch':BranchForm(),
        'formsection':SectionForm(),
        'formjob':JobForm(),
        'formrank':RankForm(),
        'formoffunitstat':OffUnitStatusForm(),
        'formoffstat':OfficerStatusForm(),
        
        'unread_notifications': unread_notifications,
        'today':today,
        'total_officers':total_officers,
        'inside_officers':inside_officers,
        'outside_officers': outside_officers,
    }

    return render(request, 'officers_affairs/home.html', context)


def officer_detail(request, pk):
    officer = get_object_or_404(Officer, pk=pk)
    return render(request, 'officers_affairs/officer_detail.html', {'officer': officer})


@login_required
@permission_required('officers_affairs.add_officer', raise_exception=True)
def officers_add(request, pk= None): # creates or Updates an officer
    if pk:
        officer = get_object_or_404(Officer, pk= pk)
        if request.method == "POST":
            form = OfficerForm(request.POST, request.FILES, instance= officer)
            if form.is_valid():
                form.instance.updated_by = request.user
                form.save()
                return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "showMessage": "تم تعديل ضابط",
                            "officer_list_changed": None
                        })
                    })
        else: # GET
            form = OfficerForm(instance= officer)
    
    # No PK, Create New
    else:  # Create new officer
        if request.method == "POST":
            form = OfficerForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.created_by = request.user  # Set created_by only when creating
                form.instance.updated_by = request.user
                form.save()
                return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "showMessage": "تم اضافة ضابط",
                            "officer_list_changed": None
                        })
                    })

        else: # Empty Create
           form = OfficerForm()


    return render(request, "officers_affairs/officer_add.html", {'form': form})



def officers_view(request):
    officers=Officer.objects.order_by('rank')
    title = None
  
    if 'search_name' in request.GET:
        title = request.GET.get('search_name')
        if title:
            officers = officers.filter(full_name__icontains=title)
            
    # Pagination logic
   
    paginator = Paginator(officers, 10)  # 10 officers per page

    page_number = request.GET.get('page', 1)  # Default to page 1
    try:
        officers = paginator.page(page_number)
    except PageNotAnInteger:
        officers = paginator.page(1)  # If page is not an integer, deliver first page
    except EmptyPage:
        officers = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page
    
    if request.method == 'POST':
        # Check which form was submitted
        if 'add_weapon' in request.POST:
            add_weapon = WeaponForm(request.POST)
            if add_weapon.is_valid():
                add_weapon.save()
                return redirect('officers')  # Redirect after form submission        

        if 'add_unit' in request.POST:
            add_unit = UnitForm(request.POST)
            if add_unit.is_valid():
                add_unit.save()
                return redirect('officers')  # Redirect after form submission
            
        if 'add_branch' in request.POST:
            add_branch = BranchForm(request.POST)
            if add_branch.is_valid():
                add_branch.save()
                return redirect('officers')  # Redirect after form submission
            
            
        if 'add_section' in request.POST:
            add_section = SectionForm(request.POST)
            if add_section.is_valid():
                add_section.save()
                return redirect('officers')  # Redirect after form submission
 
        if 'add_job' in request.POST:
            add_job = JobForm(request.POST)
            if add_job.is_valid():
                add_job.save()
                return redirect('officers')  # Redirect after form submission            
            
        if 'add_rank' in request.POST:
            add_rank = RankForm(request.POST, request.FILES)
            if add_rank.is_valid():
                add_rank.save()
                return redirect('officers')  # Redirect after form submission
        
        elif 'add_off_unit_status' in request.POST:
            add_off_unit_status = OffUnitStatusForm(request.POST)
            if add_off_unit_status.is_valid():
                add_off_unit_status.save()
                return redirect('officers')  # Redirect after form submission
        
        elif 'add_off_status' in request.POST:
            add_off_status = OfficerStatusForm(request.POST)
            if add_off_status.is_valid():
                add_off_status.save() 
                return redirect('officers')  # Redirect after form submission
            
                
    context ={
        'ranks':Rank.objects.all(),
        'officers': officers,
        'formweapon':WeaponForm(),
        'formunit':UnitForm(),
        'formbranch':BranchForm(),
        'formsection':SectionForm(),
        'formjob':JobForm(),
        'formrank':RankForm(),
        'formoffunitstat':OffUnitStatusForm(),
        'formoffstat':OfficerStatusForm(),
        'paginator': paginator,
     
        
        

    }
    return render(request, 'officers_affairs/officers.html', context)


class officers_delete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = ('officers_affairs.delete_officer', )

    model = Officer

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse( status=204, headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": "تم حذف ضابط",
                        "officer_list_changed": None,
                        
                    }) })
        

def officers_list(request):
    
    officerFilterDefault = {
        'status': OfficerStatus.objects.filter(name="قوة"),
    }

    ctx={
        'ranks':Rank.objects.all(),
        'officers_filter': filters.OfficerFilter(request.GET or officerFilterDefault),
    }
    return render(request, 'officers_affairs/officer_list.html', ctx)



def partial_officers(request):
    officers=Officer.objects.order_by('rank')
    ctx={
        'officers':officers,
    }
    return render(request, 'officers_affairs/partial_officer.html',ctx)


def about(request):
    return render(request, 'about.html')




def get_final_approver():
    # Get the officer (user) with the role 'المدير' regardless of branch
    return Officer.objects.filter(role='المدير').first().user

def get_initial_approver(officer_profile):
    # Get the branch leader who is the first approver
    return Officer.objects.filter(branch=officer_profile.branch, is_leader=True).first().user



from django.utils import timezone
import datetime
from .models import LeaveRequest

def get_remaining_days(officer, leave_type):
    today = timezone.now().date()  # التأكد من أن today هو كائن date
    
    # تحديد فترة النصف الأول والنصف الثاني من السنة
    start_of_first_half = datetime.date(today.year, 1, 1)  # تحويل إلى datetime.date
    end_of_first_half = datetime.date(today.year, 6, 30)   # تحويل إلى datetime.date
    start_of_second_half = datetime.date(today.year, 7, 1) # تحويل إلى datetime.date
    end_of_second_half = datetime.date(today.year, 12, 31) # تحويل إلى datetime.date

    # رصيد الإجازات السنوية والعارضة
    annual_leave_full_days = 15 if today <= end_of_first_half else 15
    casual_leave_full_days = 7  # الإجازة العارضة طوال السنة

    # البحث عن آخر إجازة تمت الموافقة عليها من نفس النوع
    start_date_filter = start_of_first_half if leave_type == LeaveRequest.ANNUAL_LEAVE else datetime.date(today.year, 1, 1)
    
    last_approved_leave = LeaveRequest.objects.filter(
        officer=officer, 
        leave_type=leave_type, 
        status=LeaveRequest.APPROVED, 
        start_date__gte=start_date_filter
    ).order_by('-end_date').first()

    # إذا كانت هناك إجازة سابقة من نفس النوع، استرجاع الأيام المتبقية
    if last_approved_leave:
        remaining_days = last_approved_leave.remaining_days
    else:
        # إذا لم يكن هناك إجازات، يتم إعطاء الرصيد الكامل حسب نوع الإجازة
        if leave_type == LeaveRequest.ANNUAL_LEAVE:
            remaining_days = annual_leave_full_days
        elif leave_type == LeaveRequest.CASUAL_LEAVE:
            remaining_days = casual_leave_full_days
        else:
            remaining_days = None  # لباقي الأنواع التي لا تحتوي على حد

    return remaining_days


def create_update_leave_request(request, pk=None):
    try:
        officer_profile = request.user.officer_profile
    except Officer.DoesNotExist:
        return render(request, 'officers_affairs/error.html', {
            'error_message': "لا يوجد لديك ملف ضابط مرتبط بحسابك."
        })


    remaining_days_per_type = {}
    for (leave_type, display_name) in LeaveRequest.LEAVE_TYPES:
        v = get_remaining_days(officer_profile, leave_type)
        if v == None: continue
        remaining_days_per_type[leave_type] = v

    # GET or UPDATE LeaveRequest
    if pk != None and not can_officer_edit_leave_request(officer_profile, get_object_or_404(LeaveRequest, pk= pk)):
        return HttpResponseForbidden("ليس لديك صلاحية تعديل هذا الطلب")

    if request.method == 'POST':
        if pk != None: # update
            form = LeaveRequestForm(request.POST, instance= get_object_or_404(LeaveRequest, pk= pk))

        else: # create
            form = LeaveRequestForm(request.POST)

        if form.is_valid():
            leave_type = form.cleaned_data['leave_type']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            days_taken = (end_date - start_date).days + 1

            if leave_type != LeaveRequest.INSTEAD_OF_REST:
                form.cleaned_data['compensation_date'] = None

            # Don't add two leave requests of the same type if one is still PENDING.
            if pk == None: # Create
                existing_pending_request = LeaveRequest.objects.filter(
                    officer=officer_profile,
                    leave_type=leave_type,
                    status=LeaveRequest.PENDING
                ).exists()

                if existing_pending_request:
                    form.add_error(None, "لا يمكنك تقديم طلب إجازة من نفس النوع في حين أن هناك طلب معلق.")
                    return render(request, 'officers_affairs/vacations/create_leave_request.html', {'form': form, 'remaining_days_per_type': remaining_days_per_type})
            else:
                # Update
                # check if any other request has the same type of new request, then reject change
                originalLeaveRequest = get_object_or_404(LeaveRequest, pk= pk)
                target_type = form.cleaned_data['leave_type']
                if target_type != originalLeaveRequest.leave_type:
                    for leave_request in LeaveRequest.objects.filter(officer= officer_profile, status= LeaveRequest.PENDING):
                        if leave_request.leave_type == target_type:
                            form.add_error(None, "لا يمكنك تعديل نوع طلب اجازة ولديك طلب بنفس النوع")
                            return render(request, 'officers_affairs/vacations/create_leave_request.html', {'form': form, 'remaining_days_per_type': remaining_days_per_type})
                        

            # استرجاع الأيام المتبقية من وظيفة get_remaining_days
            remaining_days = get_remaining_days(officer_profile, leave_type)

            if remaining_days is not None and days_taken > remaining_days:
                form.add_error(None, "عدد الأيام المطلوبة يتجاوز الرصيد المتبقي.")
                return render(request, 'officers_affairs/vacations/create_leave_request.html', {'form': form, 'remaining_days_per_type': remaining_days_per_type})

            # Validate the dates
            if end_date < start_date:
                form.add_error('end_date', "تاريخ الانتهاء يجب أن يكون بعد تاريخ البدء.")
                return render(request, 'officers_affairs/vacations/create_leave_request.html', {'form': form, 'remaining_days_per_type': remaining_days_per_type})
            
                
            if pk == None: # Create
                initial_approver = get_initial_approver(officer_profile)
                
                # Check if the current officer is the initial approver
                if request.user == initial_approver:
                    # Automatically go to the next approver
                    next_approver = get_next_approver(initial_approver, None)
                    if not next_approver:
                        return render(request, 'officers_affairs/error.html', {
                            'error_message': "لا يوجد مصدق لاحق."
                        })
                else:
                    next_approver = initial_approver

                # Create the leave request
                leave_request = LeaveRequest(
                    officer=officer_profile,
                    leave_type=leave_type,
                    start_date=start_date,
                    end_date=end_date,
                    days_taken=days_taken,
                    remaining_days=remaining_days - days_taken if remaining_days is not None else None,
                    compensation_date = form.cleaned_data['compensation_date'],
                    status=LeaveRequest.PENDING,
                    approver=next_approver,
                    final_approver=get_final_approver()
                )
                leave_request.save()
            
            
                # Notify the next approver
                create_notification(
                    recipient_user=next_approver, 
                    message=f"طلب إجازة جديد من {officer_profile.rank} / {officer_profile.full_name} يحتاج موافقتك.",
                    is_current_approver=True
                )

                # Notify the final approver, but only if they are not the same as the next approver
                final_approver = get_final_approver()
                if officer_profile.is_leader or officer_profile.role :
                    create_notification(
                        recipient_user=final_approver, 
                        message=f"طلب إجازة جديد من {officer_profile.rank} / {officer_profile.full_name} يحتاج موافقتك النهائية.",
                        is_final_approver=True
                    )
            else:
                # Update
                form.instance.remaining_days = remaining_days - days_taken if remaining_days is not None else None
                form.save()


            return redirect('leave_requests')

    elif pk != None: # Update GET
        form = LeaveRequestForm(instance= get_object_or_404(LeaveRequest, pk= pk))
    else: # Create GET
        form = LeaveRequestForm()



    return render(request, 'officers_affairs/vacations/create_leave_request.html', {'form': form, 'remaining_days_per_type': remaining_days_per_type}) 



def get_head_of_branch():
    try:
        # Assuming 'role' is a field in the Officer model that indicates their role
        head_of_branch = Officer.objects.get(role='رئيس فرع شئون ضباط')
        return head_of_branch.user  # Return the associated user
    except Officer.DoesNotExist:
        return None  # Return None if no such officer exists




@login_required
def approve_leave_request(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)

    # Ensure the user has permission to approve
    if request.user not in [leave_request.approver, leave_request.final_approver]:
        return render(request, 'officers_affairs/error.html', {
            'error_message': "ليس لديك إذن للموافقة على هذا الطلب."
        })

    if request.method == 'POST':
        decision = request.POST.get('decision')
        
        # If the final_approver is making the decision, handle the special case
        if request.user == leave_request.final_approver:
            # Set current approver to final approver
            leave_request.approver = leave_request.final_approver

            # If accepted, finalize the approval
            if decision == 'accept':
                leave_request.status = LeaveRequest.APPROVED
                leave_request.approver = leave_request.final_approver
                leave_request.save()
                # Notify the officer and 'رئيس فرع شئون ضباط' about the final decision
                create_notification(
                    leave_request.officer.user, 
                    f"تم التصديق علي طلب إجازتك من السيد  /  {request.user.officer_profile.role}."
                )
                head_of_branch = get_head_of_branch()  # Fetch the user with the role 'رئيس فرع شئون ضباط'
                if head_of_branch:
                    create_notification(
                        head_of_branch, 
                        f" تمت الموافقة على طلب إجازة {leave_request.officer.rank} / {leave_request.officer.full_name}."
                    )
                    
                
            
                
                
                
            elif decision == 'reject':
                leave_request.status = LeaveRequest.REJECTED
                leave_request.approver = leave_request.final_approver
                leave_request.save()
                # Notify the officer and 'رئيس فرع شئون ضباط' about the rejection
                create_notification(
                    leave_request.officer.user, 
                    f"تم رفض طلب إجازتك من السيد / {request.user.officer_profile.role}."
                )
                head_of_branch = get_head_of_branch()
                if head_of_branch:
                    create_notification(
                        head_of_branch, 
                        f"تم رفض طلب إجازة  {leave_request.officer.rank} / {leave_request.officer.full_name}."
                    )
                
            return JsonResponse({'success': True})
        
         # Normal approval process for non-final approvers
        if decision == 'accept':
            
                # Get the next approver in the approval chain
            next_approver = get_next_approver(leave_request.approver, leave_request)
                
            if next_approver:
                leave_request.approver = next_approver
                leave_request.status = LeaveRequest.PENDING
                leave_request.save()
                # Notify the next approver
                create_notification(
                    next_approver, 
                    f"طلب إجازة من {leave_request.officer.rank} / {leave_request.officer.full_name} يحتاج موافقتك.",
                    is_current_approver=True
                )
                
            else:
              # If there's no next approver, mark it as approved by the current approver
                leave_request.status = LeaveRequest.APPROVED
                leave_request.save()
                
                # Notify the officer about the approval
                create_notification(
                    leave_request.officer.user, 
                    f"تم قبول طلب إجازتك من {request.user.officer_profile.rank} / {request.user.officer_profile.full_name}."
                )
                
                
        elif decision == 'reject':
            leave_request.status = LeaveRequest.REJECTED
            leave_request.save()
            
            # Notify the officer about the rejection
            create_notification(
                leave_request.officer.user, 
                f"تم رفض طلب إجازتك من {request.user.officer_profile.rank} / {request.user.officer_profile.full_name}."
            )
        # PRG pattern: Return a JSON response after processing the request
        return JsonResponse({'success': True})
          

    return render(request, 'officers_affairs/vacations/approve_leave_request.html', {'leave_request': leave_request})







def get_next_approver(current_approver, leave_request):
    # Check if the current approver is the final approver (المدير)
    final_approver = Officer.objects.filter(role='المدير').first()

    if final_approver and current_approver == final_approver.user:
        return None  # No next approver needed; request is finalized

    # Define the prioritized order of approvers (adjust as needed)
    approver_roles = [
        'رئيس فرع شئون ضباط',
        'رئيس فرع السكرتارية',
        'نائب المدير',
        'المدير'
    ]

    # Get all officers who match these roles
    approvers = Officer.objects.filter(role__in=approver_roles).order_by('role')

    # Create a list of approvers sorted by role priority
    role_priority = {role: index for index, role in enumerate(approver_roles)}
    sorted_approvers = sorted(approvers, key=lambda x: role_priority.get(x.role, float('inf')))

    # Ensure the current approver is in the list (in case it's the branch leader, for example)
    current_officer = Officer.objects.get(user=current_approver)
    if current_officer not in sorted_approvers:
        sorted_approvers.insert(0, current_officer)  # Add current approver to the beginning of the list

    # Find the current approver in this sorted list
    for index, approver in enumerate(sorted_approvers):
        if approver.user == current_approver:
            # Check if there's a next approver in the list
            if index + 1 < len(sorted_approvers):
                return sorted_approvers[index + 1].user  # Return next approver's user

    return None  # Return None if no more approvers







@login_required
def leave_requests_list(request):
    user_officer = request.user.officer_profile
    
    

    # Roles that can see the leave requests for their approval
    approver_roles = ['المدير', 'رئيس فرع شئون ضباط', 'نائب المدير', 'رئيس فرع السكرتارية']
    
    # Get filters from the request
    selected_status = request.GET.get('status')
    officer_name = request.GET.get('officer_name', '').strip()
    selected_branch_id = request.GET.get('branch')  # Get the selected branch ID from the request
    created_at = request.GET.get('created_at')    # Default to today's date
    
    # Prepare the leave requests based on user's role
    if user_officer.role == 'رئيس فرع شئون ضباط':
        # 'رئيس فرع شئون ضباط' can view all leave requests
        leave_requests = LeaveRequest.objects.all()
    elif user_officer.role == 'المدير':
        # 'المدير' sees only pending requests that need their approval

        # if current approvar == final aproval or
        leave_requests = LeaveRequest.objects.exclude(status='approved').exclude(status='rejected',approver=get_final_approver()).filter(Q(officer__is_leader=True) | Q(officer__role__isnull=False) | Q(approver=get_final_approver()))
    
    elif  user_officer.role in approver_roles:
        # Leaders or approvers see only pending requests from their branch that need their approval
        leave_requests = LeaveRequest.objects.filter(
            status='pending',
            approver=request.user  # Only requests where the user is the approver
        )    
        
    elif user_officer.is_leader :
        # Leaders or approvers see only pending requests from their branch that need their approval
        leave_requests = LeaveRequest.objects.filter(
            officer__branch=user_officer.branch,
            status='pending',
            approver=request.user  # Only requests where the user is the approver
        )
        
    else:
        # No requests for users without appropriate roles
        leave_requests = LeaveRequest.objects.none()
        
    # Apply date filter if a date is provided
    if created_at:
        leave_requests = leave_requests.filter(created_at__date=created_at)
        
     # Apply additional filters
    if selected_status:
        leave_requests = leave_requests.filter(status=selected_status)
        
    # Apply the officer name filter only if the user chooses a name
    if officer_name:
        leave_requests = leave_requests.filter(officer__full_name__icontains=officer_name)
        
   # Apply branch filter if a branch is selected
    if selected_branch_id:
        leave_requests = leave_requests.filter(officer__branch_id=selected_branch_id)

    
    # Sorting: Show requests needing the current user's approval first, then by date (newest to oldest), then by rank
    leave_requests = leave_requests.annotate(
        needs_approval=Case(
            When(approver=request.user,  status='pending', then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by(
        '-needs_approval',      # Priority to requests needing approval from the current user
        '-created_at',           # Sort by submission date (newest to oldest)
        '-officer__rank'          # Finally, sort by officer rank
    )
    
    
    
   
    paginator = Paginator(leave_requests, 10)  # Show 10 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

      
    # Prepare context
    context = {
        'leave_requests': page_obj,
        'selected_status': selected_status,
        'selected_date': created_at,
        'officer_name': officer_name,
        'selected_branch_id': selected_branch_id,
        'page_obj': page_obj,
        'today': timezone.now().date().isoformat(),
    }
    return render(request, 'officers_affairs/vacations/leave_requests_list.html', context)



def can_officer_edit_leave_request(officer, leaveRequest):
    if leaveRequest.status != leaveRequest.PENDING:
        return False

    leader = get_initial_approver(officer)

    if officer.is_leader:
        next_approver = get_next_approver(officer.user, None)
        if not next_approver:
            return False
    else:
        next_approver = leader
    
    return leaveRequest.approver == next_approver

@login_required
def leave_requests(request):
    officer = request.user.officer_profile
    leave_requests = LeaveRequest.objects.filter(officer=officer)  # Only show the current user's requests

    for leave_request in leave_requests:
        leave_request.can_edit = can_officer_edit_leave_request(officer, leave_request)

    return render(request, 'officers_affairs/vacations/leave_requests.html', {'requests': leave_requests})




def create_notification(recipient_user, message, is_current_approver=False, is_final_approver=False):
    """
    Creates a notification for the recipient_user based on their role in the leave request process.
    """
    if is_final_approver:  # The final approver gets the notification with the final approval link.
        link = reverse('leave_requests_list')
    elif is_current_approver:  # The current approver gets a notification with the same link.
        link = reverse('leave_requests_list')
    elif recipient_user == get_head_of_branch():
        link = reverse('leave_requests_list')
    else:
        link = reverse('leave_requests')  # Officers or others get a general notification link.

    notification = Notification.objects.create(
        user=recipient_user,
        message=message,
        link=link
    )



def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'officers_affairs/notifications.html', {'notifications': notifications})

def mark_notification_read(request, notification_id):
    if request.method == 'POST':
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'})
        
        
def notification_count(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count': Notification.objects.filter(user=request.user, is_read=False).count()
        }
    return {}

@login_required
def check_new_notifications(request):
    print("Checking notifications...")
    # Count unread notifications for the logged-in user
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

    # Return the count as a JSON response
    return JsonResponse({'unread_count': unread_count})

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    return render(request, 'officers_affairs/notification_list.html', {'notifications': notifications})



from django.utils.dateparse import parse_date
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from .models import Officer, UnitStatus, DailyAttendance

# View to record attendance
def record_attendance(request):
    date_str = request.GET.get('date', None)
    
    if date_str:
        try:
            # التحقق من أن التاريخ الذي تم تمريره هو سلسلة نصية صحيحة
            date_value = parse_date(date_str)
        except ValueError:
            # في حالة حدوث خطأ في التحويل
            date_value = None
    else:
        # استخدام التاريخ الحالي إذا لم يتم تمرير تاريخ في الطلب
        date_value = timezone.localtime().date()

    if request.method == 'POST':
        officers = Officer.objects.filter(status__name='قوة')  # Officers currently in the unit
        
        for officer in officers:
            status = request.POST.get(f'status_{officer.id}')
            notes = request.POST.get(f'notes_{officer.id}', '')

            if status:
                # Retrieve or create the UnitStatus instance
                unit_status_instance, created = UnitStatus.objects.get_or_create(name=status)

                # Check if there's an existing attendance record for today
                existing_attendance = DailyAttendance.objects.filter(officer=officer, date=date_value).first()

                if existing_attendance:
                    # If there is already an attendance record, update it if the status has changed
                    if existing_attendance.status != unit_status_instance or existing_attendance.notes != notes:
                        existing_attendance.status = unit_status_instance
                        existing_attendance.notes = notes
                        existing_attendance.save()
                else:
                    # If there's no attendance record for today, create a new one
                    DailyAttendance.objects.create(
                        officer=officer,
                        date=date_value,
                        status=unit_status_instance,
                        notes=notes,
                    )
        
        return HttpResponseRedirect(reverse('attendance_list'))
                    # headers={
                    #     'HX-Trigger': json.dumps({
                    #         "showMessage": "تم اضافة ضابط",
                    #     })
                    # })

    # GET request: Fetch officers with status "موجود"
    officers = Officer.objects.filter(status__name='قوة').order_by('seniority_number')
    officers = sorted(officers, key=lambda officer: extract_numeric(officer.seniority_number))

    unit_statuses = UnitStatus.objects.all()

    context = {
        'officers': officers,
        'unit_statuses': unit_statuses,
        'today': date_value,
    }
    return render(request, 'officers_affairs/attendance/record_attendance.html', context)


# View to display daily attendance
def attendance_list(request):
    date_str = request.GET.get('date', None)  # افترض أن التاريخ يأتي من طلب GET
    if date_str:
        try:
            date_value = parse_date(date_str)  # تأكد أن date_str هو نصي
        except ValueError:
            date_value = None  # في حالة حدوث خطأ في التحويل
    else:
        date_value = timezone.localtime().date()  # تاريخ اليوم الافتراضي
    attendance_records = DailyAttendance.objects.filter(date=date_value).select_related('officer')

    today = timezone.localtime().date()

    # Count officers with the status 'موجود', currently outside, and with a different status
    total_officers = DailyAttendance.objects.filter(date=date_value).count()
    inside_officers = DailyAttendance.objects.filter(status__name='موجود',date=date_value).count()
    outside_officers = DailyAttendance.objects.exclude(status__name='موجود').filter(date=date_value).count()
    outside_mission_officers = DailyAttendance.objects.filter(status__name='مأمورية',date=date_value).count()
    outside_hospital_officers = DailyAttendance.objects.filter(status__name='مست',date=date_value).count()
    outside_open_mission_officers = DailyAttendance.objects.filter(status__name='مأمورية مفتوحة',date=date_value).count()
    outside_annual_officers = DailyAttendance.objects.filter(status__name='سنوية',date=date_value).count()
    outside_casual_officers = DailyAttendance.objects.filter(status__name='عارضة',date=date_value).count()
    outside_instead_of_rest_officers = DailyAttendance.objects.filter(status__name='بدل راحة',date=date_value).count()
    outside_rest_officers = DailyAttendance.objects.filter(status__name='راحة',date=date_value).count()
    outside_leader_grant_officers = DailyAttendance.objects.filter(status__name='منحة قائد',date=date_value).count()
    outside_grant_officers = DailyAttendance.objects.filter(status__name='إذن',date=date_value).count()
    outside_travel_officers = DailyAttendance.objects.filter(status__name='سفر خارج البلاد',date=date_value).count()

    
    attendance_records = sorted(attendance_records, key=lambda record: extract_numeric(record.officer.seniority_number))

    context = {
        'attendance_records': attendance_records,
        'today': date_value,
        'total_officers': total_officers,
        'outside_officers': outside_officers,
        'inside_officers': inside_officers,
        'outside_mission_officers':outside_mission_officers,
        'outside_hospital_officers':outside_hospital_officers,
        'outside_open_mission_officers':outside_open_mission_officers,
        'outside_annual_officers':outside_annual_officers,
        'outside_casual_officers':outside_casual_officers,
        'outside_instead_of_rest_officers':outside_instead_of_rest_officers,
        'outside_rest_officers':outside_rest_officers,
        'outside_leader_grant_officers':outside_leader_grant_officers,
        'outside_grant_officers':outside_grant_officers,
        'outside_travel_officers':outside_travel_officers,
    }
    return render(request, 'officers_affairs/attendance/attendance_list.html', context)