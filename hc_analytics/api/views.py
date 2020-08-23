from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from .utils.selection.cv.score import get_score
from .utils.selection.employment.best_dictionary import get_best_dictionary
from .utils.selection.employment.match_cvs import match_cvs
from .utils.selection.match.cvs_vs_diccs import get_match_all
from .utils.selection.match.average_score import get_match_average
import json


class CV(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            cv_id = data["cvId"]

            result = get_score(cv_id)
            return Response({"ok": True, "result": result}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"ok": False, "result": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Employment(viewsets.ViewSet):
    def post_best_dictionary(self, request):
        try:
            data = json.loads(request.body)
            description_employment = data["description"]
            result = get_best_dictionary(description_employment)
            return Response({"ok": True, "result": result}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"ok": False, "result": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post_match_cvs(self, request):
        try:
            data = json.loads(request.body)
            dictionary_id = data["dictionaryId"]
            result = match_cvs(dictionary_id)
            return Response({"ok": True, "result": result}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"ok": False, "result": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Match(viewsets.ViewSet):
    def post_match_all(self, request):
        try:
            result = get_match_all()
            return Response({"ok": True, "result": result}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"ok": False, "result": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post_match_average(self, request):
        try:
            data = json.loads(request.body)
            match_cv = data["matchCv"]

            # expected match_test to be:
            # {
            #   "PERSONALIDAD": 0.75,
            #   "COMUNICACION_EFECTIVA": 0.88,
            #    etc etc ...
            # }
            match_tests = data["matchTests"]  # data type of match_test => 'array'
            interview_score = data["interviewScore"]
            reference_score = data["referenceScore"]
            result = get_match_average(
                match_cv, match_tests, interview_score, reference_score
            )
            return Response({"ok": True, "result": result}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"ok": False, "result": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    def post_match_average_cv_test(self,request):
        try:
            data = json.loads(request.body)
            match_cv = data["matchCv"]
            match_tests = data["matchTests"]  # data type of match_test => 'array'

            result = get_match_average_cv_test(
                match_cv, match_tests
            )
            return Response({"ok": True, "result": result}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"ok": False, "result": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )        
