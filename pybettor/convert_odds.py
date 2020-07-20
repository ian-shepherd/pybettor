# -*- coding: utf-8 -*-
# 
# title: Odds Converter
# description: This function converts any odds or probability
# parameters:
#   odds: odds of event implied or probability
#   cat_in: type of odds or implied probability
#        'us', American Odds
#        'dec', Decimal Odds
#        'frac', Fractional Odds
#        'prob', Implied Probability
#   cat_out: type of odds or implied probability
#        'all', All Odds and implied probability
#        'us', American Odds
#        'dec', Decimal Odds
#        'frac', Fractional Odds
#        'prob', Implied Probability
# return the odds or implied probability of a given event
# 
# examples
# convert_odds(-175, cat_in = 'us', cat_out = 'all')
# convert_odds(2, cat_in = 'dec', cat_out = 'prob')
# convert_odds(4/7, cat_in = 'frac', cat_out = 'us')
# convert_odds(.75, cat_in = 'prob', cat_out = 'frac')
# 

import sys
from fractions import Fraction
import pandas as pd
from implied_odds import implied_odds
from implied_prob import implied_prob

def convert_odds(odds, cat_in = 'us', cat_out = 'all'):
    
    if type(odds) is not list:
        odds = [odds]
    
    # Error Handling
    if not all(isinstance(x, (int, float)) for x in odds) :
        sys.exit("odds must be numeric")
        
    if cat_in not in ['us', 'frac', 'dec', 'prob']:
        sys.exit("input category must be either: ('us', 'dec', 'frac', 'prob')")
        
    if cat_out not in ['all', 'us', 'frac', 'dec', 'prob']:
        sys.exit("output category must be either: ('all', 'us', 'dec', 'frac', 'prob')")
    
    if cat_in == cat_out:
        sys.exit("input and output categories must be different")

    
    if cat_in == 'us':
        
        if not all(isinstance(x, int) for x in odds):
            sys.exit('us odds must be a whole number')
            
        if any(x in range(-99,100) for x in odds):
            sys.exit("us odds cannot be between -99 and 99")
        
        
        if cat_out == 'all':
            us = odds
            dec = [-100 / x + 1 if x <= -100 else x / 100 + 1 for x in odds]
            dec = [round(x, 2) for x in dec]
            frac = [-100 / x if x <= -100 else x / 100 for x in odds]
            frac = [Fraction(x).limit_denominator(100)for x in frac]
            frac = [str(x.numerator) + '/' + str(x.denominator) for x in frac]  
            prob = implied_prob(odds, category = "us")
            new_odds = pd.DataFrame({'American' : us,
                                     'Decimal' : dec,
                                     'Fraction' : frac,
                                     'Implied Probability' : prob})
       
        elif cat_out == 'dec':
            new_odds = [-100 / x + 1 if x <= -100 else x / 100 + 1 for x in odds]
            new_odds = [round(x, 2) for x in new_odds]
        
        
        elif cat_out == 'frac':
            new_odds = [-100 / x if x <= -100 else x / 100 for x in odds]
            new_odds = [Fraction(x).limit_denominator(100)for x in new_odds]
            new_odds = [str(x.numerator) + '/' + str(x.denominator) for x in new_odds]            
        
        
        elif cat_out == 'prob':
            new_odds = implied_prob(odds, category = "us")
            
        
    elif cat_in == 'dec':
        
        if any(x <= 1 for x in odds):        
            sys.exit("dec odds must be greater then 1")
        
        
        if cat_out == 'all':
            us = [(x - 1) * 100 if x >= 2 else -100 / (x - 1) for x in odds]
            us = [round(x) for x in us]
            dec = odds
            frac = [Fraction(x - 1).limit_denominator(100) for x in odds]
            frac = [str(x.numerator) + '/' + str(x.denominator) for x in frac]  
            prob = implied_prob(odds, category = "dec")
            new_odds = pd.DataFrame({'American' : us,
                                     'Decimal' : dec,
                                     'Fraction' : frac,
                                     'Implied Probability' : prob})
        
        elif cat_out == 'us':
            new_odds = [(x - 1) * 100 if x >= 2 else -100 / (x - 1) for x in odds]
            new_odds = [round(x) for x in new_odds]
        
        elif cat_out == 'frac':
            new_odds = [Fraction(x - 1).limit_denominator(100) for x in odds]
            new_odds = [str(x.numerator) + '/' + str(x.denominator) for x in new_odds]
        
        elif cat_out == 'prob':
            new_odds = implied_prob(odds, category = "dec")
            
        
        
    elif cat_in == 'frac':
        
        if any(x <= 0 for x in odds):
            sys.exit("frac odds must be greater then 0")
        
        new_odds = 1
        if cat_out == 'all':
            us = [x * 100 if x >= 1 else -100 / x for x in odds]
            us = [round(x) for x in us]
            dec = [round(x + 1, 2) for x in odds]
            frac = [Fraction(x).limit_denominator(100) for x in odds]
            frac = [str(x.numerator) + '/' + str(x.denominator) for x in frac]  
            prob = implied_prob(odds, category = "frac")
            new_odds = pd.DataFrame({'American' : us,
                                     'Decimal' : dec,
                                     'Fraction' : frac,
                                     'Implied Probability' : prob})
        
        elif cat_out == 'us':
            new_odds = [x * 100 if x >= 1 else -100 / x for x in odds]
            new_odds = [round(x) for x in new_odds]
        
        elif cat_out == 'dec':
            new_odds = [round(x + 1, 2) for x in odds]
        
        elif cat_out == 'prob':
            new_odds = implied_prob(odds, category = "frac")
        
        
        
    elif cat_in == 'prob':
        
        if any(x < 0 or x>  1 for x in odds):
            sys.exit("probability must be between 0 and 1")
        
        if cat_out == 'all':
            us = implied_odds(odds, category = "us")
            dec = implied_odds(odds, category = "dec")
            frac = implied_odds(odds, category = "frac")
            prob = odds
            new_odds = pd.DataFrame({'American' : us,
                                     'Decimal' : dec,
                                     'Fraction' : frac,
                                     'Implied Probability' : prob})
        
        elif cat_out == 'us':
            new_odds = implied_odds(odds, category = "us")
        
        elif cat_out == 'dec':
            new_odds = implied_odds(odds, category = "dec")
        
        elif cat_out == 'frac':
            new_odds = implied_odds(odds, category = "frac")
    

    return new_odds