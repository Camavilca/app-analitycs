def get_match_average_cv_test(
    match_cv=None, match_tests=None
):
    total_sum = 0
    len_cv = 0
    
    total_sum2 = 0
    len_test = 0
    len_test2 = 0
    
    if match_cv != None:
        len_cv += 1
        total_sum += match_cv
        
    if match_tests != None:
        len_test += 1
        for key in match_tests:
            len_test2 += 1
            total_sum2 += match_tests[key]
       
        total_sum2 = total_sum2/len_test2
    
    tot = [total_sum,total_sum2]
    t_len = [len_cv,len_test]
    
    return sum(tot) / sum(t_len)