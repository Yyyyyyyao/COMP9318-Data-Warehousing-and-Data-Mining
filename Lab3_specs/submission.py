## import modules here 
import pandas as pd 
import numpy as np 

################# Question 1 #################

def multinomial_nb(training_data, sms):# do not change the heading of the function

    # ratio = the probability of sms is spam / the probability of sms is ham.
    # ratio = pro_spam_sms / pro_ham_sms

    # pro_spam = # of spam / total # of training data
    # pro_spam = # of spam / total # of training data
    count_spam = 0
    count_ham = 0
    training_token_spam = {} # {word, freq}
    training_token_ham = {} # {word, freq}
    vacabulary = {}
        
    for data in training_data:
        if data[1] == "spam":
            count_spam += 1
            for key, val in data[0].items():
                if key not in vacabulary:
                    vacabulary[key] = 1

                if key not in training_token_spam:
                    training_token_spam[key] = val
                else:
                    training_token_spam[key] += val
                    
        elif data[1] == "ham":
            count_ham += 1
            for key, val in data[0].items():
                if key not in vacabulary:
                    vacabulary[key] = 1
                    
                if key not in training_token_ham:
                    training_token_ham[key] = val
                else:
                    training_token_ham[key] += val

    total_distinct_words_in_spam = sum(training_token_spam.values())
    total_distinct_words_in_ham = sum(training_token_ham.values())
    
    pro_word_spam_dic = {}
    pro_word_ham_dic = {}
    for key, val in vacabulary.items():
        if key not in training_token_spam:
            pro_word_spam_dic[key] = (0+1) / (total_distinct_words_in_spam + len(vacabulary))
        else:
            pro_word_spam_dic[key] = (training_token_spam[key]+1) / (total_distinct_words_in_spam + len(vacabulary))

        if key not in training_token_ham:
            pro_word_ham_dic[key] = (0+1) / (total_distinct_words_in_ham + len(vacabulary))
        else:
            pro_word_ham_dic[key] = (training_token_ham[key]+1) / (total_distinct_words_in_ham + len(vacabulary))

    pro_spam = count_spam / len(training_data)
    pro_ham = count_ham / len(training_data)


    # pro_spam_sms = pro_sms_spam*pro_spam
    pro_spam_sms = pro_spam
    for word in sms:
        if word not in pro_word_spam_dic:
            continue
        else:
            pro_spam_sms = pro_spam_sms*pro_word_spam_dic[word]

    # pro_ham_sms = pro_sms_ham*pro_ham
    pro_ham_sms = pro_ham
    for word in sms:
        if word not in pro_word_ham_dic:
            continue
        else:
            pro_ham_sms = pro_ham_sms*pro_word_ham_dic[word]

    ratio = pro_spam_sms / pro_ham_sms
    
    return ratio 


