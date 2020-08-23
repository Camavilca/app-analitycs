def get_match_average(
    match_cv=None, match_tests=None, interview_score=None, reference_score=None
):
    total_sum = 0
    total_len = 0

    if match_cv != None:
        total_len += 1
        total_sum += match_cv
    if match_tests != None:
        for key in match_tests:
            total_len += 1
            total_sum += match_tests[key]
    if interview_score != None:
        total_len += 1
        total_sum += interview_score
    if reference_score != None:
        total_len += 1
        total_sum += reference_score

    return total_sum / total_len  # ex-output: 0.88
