# -*- coding: utf-8 -*-
# 
# title: Odds of Event Conversion to Probability
# description: This function provides the implied probability for a given event
# parameters:
#   odds: odds of event
#   category: type of odds
#        'us', American Odds
#        'dec', Decimal Odds
#        'frac', Fractional Odds
# return implied probability of a given event
# 
# examples
# implied_prob([-500,450], category='us')
# implied_prob([1.2, 5.5], category='dec')
# implied_prob([1/5, 9/2], category='frac')
# 

import sys

def implied_prob(odds, category = "us"):
    
    if type(odds) is not list:
        odds = [odds]
    
    # Error Handling
    if not all(isinstance(x, (int, float)) for x in odds) :
        sys.exit("odds must be numeric")
        
    if category not in ['us', 'frac', 'dec']:
        sys.exit("type must be either: ('us', 'dec', 'frac')")
    
    
    if category == 'us':
        
       
        if not all(isinstance(x, int) for x in odds):
            sys.exit('us odds must be a whole number')
            
        if any(x in range(-99,100) for x in odds):
            sys.exit("us odds cannot be between -99 and 99")
        
        imp_prob = [1 / (1 - 100 / x) if x <= -100 else 1 / (1 + x / 100) for x in odds]

    
    elif category == 'dec':
        
        if any(x <= 1 for x in odds):        
            sys.exit("dec odds must be greater then 1")
        
        imp_prob = [1 / x for x in odds]

        
    elif category == 'frac':
        
        if any(x <= 0 for x in odds):
            sys.exit("frac odds must be greater then 0")

        imp_prob = [1 / (1 + x) for x in odds]
            
    
    return imp_prob