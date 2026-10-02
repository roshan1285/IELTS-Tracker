from .models import CustomUser, ListeningTest, ReadingTest, WritingTest

from django.http import JsonResponse
import json

import math

def calculate_listening_band_score(score):

    if score is None:
        return None

    if score >= 39: return 9.0
    if score >= 37: return 8.5
    if score >= 35: return 8.0
    if score >= 33: return 7.5
    if score >= 30: return 7.0
    if score >= 27: return 6.5
    if score >= 23: return 6.0
    if score >= 20: return 5.5
    if score >= 16: return 5.0
    if score >= 13: return 4.5
    if score >= 11: return 4.0
    if score >= 8: return 3.5
    if score >= 6: return 3.0
    if score >= 4: return 2.5
    if score == 3: return 2.0
    if score == 2: return 1.5
    if score == 1: return 1.0
    return 0.0

def calculate_reading_band_score(score):

        if score is None:
            return None

        if score >= 39: return 9.0
        if score >= 37: return 8.5
        if score >= 35: return 8.0
        if score >= 33: return 7.5
        if score >= 30: return 7.0
        if score >= 27: return 6.5
        if score >= 23: return 6.0
        if score >= 19: return 5.5
        if score >= 15: return 5.0
        if score >= 13: return 4.5
        if score >= 10: return 4.0
        if score >= 8: return 3.5
        if score >= 6: return 3.0
        if score >= 4: return 2.5
        if score == 3: return 2.0
        if score == 2: return 1.5
        if score == 1: return 1.0
        return 0.0

def round_to_half(x):
    return math.floor(x * 2 + 0.5) / 2


def calculate_overall_band_score(request):

    if request.method == "POST":
        data= json.loads(request.body)

        L=float(data.get('L', 0))
        R=float(data.get('R', 0))
        W=float(data.get('W', 0))
        S=float(data.get('S', 0))
        
        overall_band = round_to_half(
            (L + R + W + S) / 4
        )

        return JsonResponse({"overall_band":overall_band})