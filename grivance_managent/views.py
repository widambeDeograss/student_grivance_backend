from datetime import timedelta, datetime

from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from celery import shared_task
from .models import SubmittedProblems
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Create your views here.
class DivisionView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        serialized = DivisionPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Division.objects.all()
            serialized = DivisionGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            divisionId = request.GET.get("divisiId")
            queryset = Division.objects.get(id=divisionId)
            subm_problems = SubmittedProblems.objects.filter(current_responsible_division=divisionId)
            sub_divs = SubDivision.objects.filter(division=divisionId)
            prob_types = ProblemType.objects.filter(responsible_division=divisionId)
            subm_problems_solved = SubmittedProblems.objects.filter(current_responsible_division=divisionId, problem_solved_state=True)
            subm_problems_unsolved = SubmittedProblems.objects.filter(current_responsible_division=divisionId, problem_solved_state=False)
            serialized = DivisionGetSerializer(instance=queryset, many=False)
            data = {
                "submitted_probs": subm_problems.count(),
                "submitted_probs_solved": subm_problems_solved.count(),
                "submitted_probs_unsolved": subm_problems_unsolved.count(),
                "sub_divisions": sub_divs.count(),
                "problem_types": prob_types.count(),
                "division": serialized.data
            }
            return Response(data)
        else:
            return Response({"message": "Specify the querying type"})


class SubDivisionView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        serialized = SubDivisionPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = SubDivision.objects.all()
            serialized = SubDivisionGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            divisionId = request.GET.get("divisiId")
            queryset = SubDivision.objects.filter(division=divisionId)
            serialized = SubDivisionGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "sub_single":
            divisionId = request.GET.get("sub_divisiId")
            queryset = SubDivision.objects.get(id=divisionId)
            serialized = SubDivisionGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class ProblemTypeView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        print(data['type_name'])
        an_data = {
            "type_name": data['type_name'],
            "time_required": timezone.timedelta(days=int(data['time_required'])),
            "responsible_division": data['responsible_division'],
            "responsible_sub_divifany": '',
        }
        serialized = ProblemTypePostSerializer(data=an_data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = ProblemType.objects.all()
            serialized = ProblemTypeGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            probId = request.GET.get("probId")
            queryset = ProblemType.objects.get(id=probId)
            subm_problems = SubmittedProblems.objects.filter(problem_type=probId)
            subm_problems_solved = SubmittedProblems.objects.filter(problem_type=probId, problem_solved_state=True)
            subm_problems_unsolved = SubmittedProblems.objects.filter(problem_type=probId, problem_solved_state=False)
            serialized = ProblemTypeGetSerializer(instance=queryset, many=False)
            data = {
                "submitted_probs": subm_problems.count(),
                "submitted_probs_solved": subm_problems_solved.count(),
                "submitted_probs_unsolved": subm_problems_unsolved.count(),
                "problem_type": serialized.data
            }
            return Response(data)
        elif querytype == "signle_div_problems":
            divId = request.GET.get("divisiId")
            queryset = ProblemType.objects.filter(responsible_division=divId)
            print(queryset)
            serialized = ProblemTypeGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)

        else:
            return Response({"message": "Specify the querying type"})


class SubmittedProblemsView(APIView):

    @staticmethod
    def post(request):
        data = request.data
        querytype = request.GET.get("querytype")

        if querytype == "anonymous":
            if data.get('current_responsible_sub_divifany') is not None:
                an_data = {
                    "problem_type": data['problem_type'],
                    "current_responsible_division": data['current_responsible_division'],
                    "current_responsible_sub_divifany": data['current_responsible_sub_divifany'],
                    "submitted_problem": data['submitted_problem'],
                }
                serializedNotification = NotificationPostSerializer(data={
                    "notification": f"Grievance with problem type no {data['problem_type']} has been submitted to your division solve it before deadline",
                    "sub_divifany":  data['current_responsible_sub_divifany'],
                })
                if serializedNotification.is_valid():
                    serializedNotification.save()
            else:
                an_data = {
                    "problem_type": data['problem_type'],
                    "current_responsible_division": data['current_responsible_division'],
                    "submitted_problem": data['submitted_problem'],
                }
                serializedNotification = NotificationPostSerializer(data={
                    "notification": f"Grievance with problem type {data['problem_type']} has been submitted to your division solve it before deadline",
                    "division": data['current_responsible_division'],
                })
                if serializedNotification.is_valid():
                    serializedNotification.save()

            serialized = SubmittedProblemsPostSerializer(data=an_data)
            if serialized.is_valid():
                instance = serialized.save()
                serialized_instance = SubmittedProblemsPostSerializer(instance)
                return Response({"save": True, "saved_problem": serialized_instance.data})
            else:
                return Response({"save": False, "error": serialized.errors})
        else:
            id = request.GET.get("id")
            serialized = SubmittedProblemsPostSerializer(data=data)
            if serialized.is_valid():
                instance = serialized.save()
                serialized_instance = SubmittedProblemsPostSerializer(instance)
                return Response({"save": True, "saved_problem": serialized_instance.data})
            else:
                return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = SubmittedProblems.objects.all()
            serialized = SubmittedProblemsGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single_div":
            divisionId = request.GET.get("divisiId")
            queryset = SubmittedProblems.objects.get(current_responsible_division=divisionId)
            serialized = SubmittedProblemsGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
        elif querytype == "single_prob":
            prob_id = request.GET.get("id")
            queryset = SubmittedProblems.objects.get(id=prob_id)
            serialized = SubmittedProblemsGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
        elif querytype == "user_prob":
            user_id = request.GET.get("user_id")
            queryset = SubmittedProblems.objects.filter(user_submitted=user_id)
            serialized = SubmittedProblemsGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class ProblemEvidenceView(APIView):

    @staticmethod
    def post(request):
        data = request.data
        print(data)
        if data.get('type_submission') == "problem_evd":
            try:
                sub_problem = get_object_or_404(SubmittedProblems,
                                                current_responsible_division=data['current_responsible_division'],
                                                problem_type=data['problem_type'],
                                                submitted_problem=data['submitted_problem'])
                data1 = {
                    "problem": sub_problem.id,
                    "file_type": int(data['file_type']),
                    "evdc": data['evdc'],
                }
                print(data1)
                serializedd = ProblemEvidencePostSerializer(data=data1)
                if serializedd.is_valid():
                    serializedd.save()
                    return Response({"save": True})
            except Exception as e:
                print(e)
                return Response({"save": False})
        else:
            try:
                id = request.GET.get("prob_id")
                serialized = ProblemEvidencePostSerializer(data=data)
                if serialized.is_valid():
                    sub_prob = SubmittedProblems.objects.get(id=id)
                    sub_prob.problem_solved_state = True
                    sub_prob.save()
                    serialized.save()
                    serializedNotification = NotificationPostSerializer(data={
                        "notification": f"Your Grievance with no {id} has been solved",
                        "user": data['user'],
                    })
                    if serializedNotification.is_valid():
                        serializedNotification.save()
                    return Response({"save": True})
                return Response({"save": False, "error": serialized.errors})
            except SubmittedProblems.DoesNotExist:
                return Response({"save": False, "error": "Problem doest exist"})



    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = ProblemEvidence.objects.all()
            serialized = ProblemEvidenceGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            id = request.GET.get("prob_id")
            queryset = ProblemEvidence.objects.filter(problem=id)
            serialized = ProblemEvidenceGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class NotificationView(APIView):

    @staticmethod
    def post(request):
        data = request.data
        serialized = NotificationPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Notification.objects.all()
            serialized = NotificationGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            id = request.GET.get("user_id")
            queryset = Notification.objects.get(user=id)
            serialized = NotificationGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class DashBoardStats(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        users = User.objects.all().count()
        divisions_count = Division.objects.all().count()
        subm_problems_solved = SubmittedProblems.objects.filter(problem_solved_state=True).count()
        subm_problems_unsolved = SubmittedProblems.objects.filter(problem_solved_state=False).count()

        start_date = timezone.now() - timedelta(days=365)

        # Initialize the chart data dictionary
        chart_data = {
            'series': [],
            'labels': []
        }

        chart_data2 = {
            'series': [],
            'labels': []
        }

        chart_data3 = {
            'series': [],
            'labels': []
        }

        # Get the start and end dates for the week
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Initialize data arrays
        solved_data = []
        unsolved_data = []

        # Iterate over each day of the week
        for day_offset in range(7):
            # Get the date for the current day
            current_date = start_of_week + timedelta(days=day_offset)
            # Get the count of solved and unsolved problems for the current day
            solved_count = SubmittedProblems.objects.filter(
                created_at__date=current_date,
                problem_solved_state=True
            ).count()
            unsolved_count = SubmittedProblems.objects.filter(
                created_at__date=current_date,
                problem_solved_state=False
            ).count()
            # Add the counts to data arrays
            solved_data.append(solved_count)
            unsolved_data.append(unsolved_count)
            # Add the label for the current day
            chart_data3['labels'].append(current_date.strftime('%a'))

        # Add the data arrays to the chart data
        chart_data3['series'].append({
            'name': 'SolvedProblems',
            'data': solved_data
        })
        chart_data3['series'].append({
            'name': 'UnsolvedProblems',
            'data': unsolved_data
        })

        # Get all divisions
        divisions = Division.objects.all()

        # Iterate over each division
        for division in divisions:
            print(division)
            # Get the count of solved and unsolved problems for the division
            solved_count = SubmittedProblems.objects.filter(
                current_responsible_division=division,
                problem_solved_state=True
            ).count()

            unsolved_count = SubmittedProblems.objects.filter(
                current_responsible_division=division,
                problem_solved_state=False
            ).count()
            print(solved_count)
            # Calculate the percentage of solved problems
            total_count = solved_count + unsolved_count
            percentage_solved = round((solved_count / total_count) * 100, 2) if total_count != 0 else 0

            # Add percentage and division name to chart data
            chart_data2['series'].append(percentage_solved)
            chart_data2['labels'].append(division.name)
        print(chart_data2)
        # Get distinct problem types
        problem_types = ProblemType.objects.all()

        # Iterate over each problem type
        for problem_type in problem_types:
            # Get the count of submitted problems for each month in the past year
            problem_counts = SubmittedProblems.objects.filter(
                problem_type=problem_type,
                created_at__gte=start_date
            ).extra({'month': "EXTRACT(month FROM created_at)", 'year': "EXTRACT(year FROM created_at)"}).values(
                'month', 'year').annotate(count=Count('id'))

            # Initialize data list for the problem type
            data = []

            # Iterate over each month in the past year
            for i in range(1, 13):
                # Find the count of submitted problems for the current month
                count = next((item['count'] for item in problem_counts if item['month'] == i), 0)
                data.append(count)

            # Add data for the problem type to the chart data
            chart_data['series'].append({
                'name': problem_type.type_name,
                'data': data
            })

        # Populate labels for the chart (last 12 months)
        current_month = start_date.month
        current_year = start_date.year
        for i in range(12):
            chart_data['labels'].append(datetime(current_year, current_month, 1).strftime('%b'))
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
        print(chart_data)

        data = {
            "users": users,
            "divisions": divisions_count,
            "solved_problems": subm_problems_solved,
            "unsolved_problems": subm_problems_unsolved,
            "chart_one": chart_data,
            "chart_two": chart_data2,
            "chart_3": chart_data3

        }
        return JsonResponse(data)


@shared_task
def check_time_limit_notifications():
    print("----------------------------------------------")
    threshold_time = timezone.now() + timezone.timedelta(minutes=30)  # Example: 30 minutes before time limit
    problems_near_time_limit = SubmittedProblems.objects.filter(created_at__lte=threshold_time)

    for problem in problems_near_time_limit:
        # Send notification to the required personnel
        send_notification(problem)


def send_notification(problem):
    subject = f"Problem nearing time limit: {problem.id}"
    message = f"The problem with ID {problem.id} is nearing the time limit."
    recipients = [
        problem.current_responsible_division.admin.email]  # Assuming the admin field contains the User with an email field
    send_mail(subject, message, 'from@example.com', recipients)
