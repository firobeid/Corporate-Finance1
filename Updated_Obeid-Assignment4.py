# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 18:12:58 2018
@author: Firas Obeid
Email: feras.obeid@lau.edu
All rights reserved.
"""
# This assignement has taught me 10,000 ways how not to let my code work with pandas. Make it simple it comes out elegant.
import pandas as pd
import numpy as np

pd.set_option('max_colwidth', 800)
#Built a main function that calculates, NPV, IRR, Profitability index, payback period and displays pandas of dicounted cash flows(npv_data) and undiscounted cash flows(dfcash)
def discounting(r, n):# This function will be called from my mother function to discount the cash flows
    discount_factor = [] #The discounting factors will be stored in a list
    for h in range(0, n + 1): # loop to get discount factors and append to a list
        rate = 1 / ((1 + r) ** h)
        discount_factor.append(rate)
    return discount_factor
# Main Function for the whole code:
def calc_npv(n, intial_cost, cash_flows, r, k): # A full mother function the calculate NPV, IRR and display pandas. All of that is done by passing the cashflows, period and rate of return(when needed)
    npv_data = pd.DataFrame({'Cash_Flows': [i for i in range(0,n + 1)]}, index = [i for i in range(0, n + 1)]) #the iterations will take whatever cash flows assigned when my function is called in separate problems
    npv_data.index.name = 'Year' #The index is set to be named "Years'. The number of years is passed through function call
    npv_data.loc[0]['Cash_Flows'] = intial_cost #index zero in colmun with intial cost. The zero index was empty and reserved for the intial cost as stated
    npv_data.Cash_Flows.loc[[i for i in range(1, n + 1)]] = cash_flows #tried several formats until this worked to change all cash flows through passing a list to the function and updating the iterable cash flow series. Note that range starts at 1 not 0 to keep 0 for intial cost reserved
    npv_data['Discounting factors'] = pd.Series(discounting(r,n)) #panda columns are eventually series so I added a new series of the discounted cash flows through an outter function coded earlier
    npv_data['Discounted_Cash_Flows'] = npv_data.apply(np.prod, axis = 1) #apply method used to multiply cash flows column with discounting factors column to give new discounted cash flows column. Axis = 1 resembles columns and 0 for rows
    df_cash_flow_only = pd.DataFrame({'Cash_Flows': [i for i in range(0,n + 1)]}, index = [i for i in range(0, n + 1)]) #dataframe for non discounted cash flows for payvack period cacl. and displaying purposes
    df_cash_flow_only.index.name = 'Year'
    df_cash_flow_only.loc[0]['Cash_Flows'] = intial_cost
    df_cash_flow_only.Cash_Flows.loc[[i for i in range(1, n + 1)]] = cash_flows
    npv = np.npv(r, npv_data.loc[:]['Cash_Flows']) #Pass cash flow column from dataframe. I could have summed up the discounted cash flows + intial cost, but kept a general frmat for calculation purposes
    irr = round((np.irr(npv_data.loc[:]['Cash_Flows']) * 100), 4)
    prof_index = 0 # I was getting a runtime warning, thus I adjusted that be add if_st so that if one of the problems have intial_cost = 0 dont excute
    if intial_cost != 0:
        prof_index = round((np.npv(r, npv_data.loc[:]['Cash_Flows']) + (-intial_cost)) / (-intial_cost), 3) # to caclculate PI through removing the intial cost from discounted cash flows then dividind the PV of DCF / initial cost
    if r == 0: #if rate is zero the cash flows oayback will be calculated and passed by providing the "k" iterable in the call function, which is the last year that cumulative cash flows are <=0.
        residual_CF = intial_cost + sum(cash_flows[:k])
        left_over_CF = -residual_CF / cash_flows[k]
        period = round((k  + left_over_CF), 4)  
    else: #if r is not zero, we calculate the discounted cash flows payback. I appended to a series the discounting factors through calling th outside function and turning that series to a list. The index 0 is deleted since its is 1 and we want the first element in D_C_F to discount first element in cash_flows list
        D_C_F =  pd.Series(discounting(r,n)).tolist()
        del D_C_F[0]
        discounted_list =  [x * D_C_F[i] for i, x in enumerate(cash_flows)] #for every index in cash_flow list, the respective index in D_C_F will be multiplied to get back the discounted cash flows. I used this method instead of retriving from pandas since accessing pandas in such a way don't give back reuired elements.
        residual_CF = intial_cost + sum(discounted_list[:k])
        left_over_CF = -residual_CF /discounted_list[k] #fractional payback that goes on to the kth iteration 
        period = round((k  + left_over_CF), 4)
    return npv, npv_data, irr, df_cash_flow_only, period, prof_index # when calling the function I have to call all returned variables and fill all parameters. Some parameters are passed to allows the function to return a value without them yielding a significant implication on the functions calculations
#Question 1 : You will oberve that I only have to call my function for the rest of the problem to get back an answer. The rest is just diplaying the answer and slight modifications i.e: Qxns 12 & 13
npv, npv_data, irr, dfcash, period, PI = calc_npv(4, -3300, [2500, 1700, 2900, 2300], 0 / 100, 1) 
print("\n\n\t\t\t\t **************NPV Assignment**************\n\nQuestion1:\n{}\nThe payback period for the given cash flows is {} yrs.".format(dfcash, period))
#Question 2 
npv, npv_data, irr, dfcash, opt_1, PI = calc_npv(11, -2960, [740] * 11, 0 / 100, 4)
npv, npv_data, irr, dfcash, opt_2, PI = calc_npv(11, -4366, [740] * 11, 0 / 100, 5)
npv, npv_data, irr, dfcash, opt_3, PI = calc_npv(11, -8880, [740] * 11, 0 / 100, 10)
print("\nQuestion 2:\na) The payback period is {} when the initial cost is $2960.\
     \nb)The payback period is {} when the initial cost is $4366.\nc)The payback period \
is {} when the initial cost is $8880, which means that their is no payback since cash flows stop at year 11.".format(opt_1, opt_2, opt_3))
#Question3 
npv, npv_data, irr, dfcash, period, PI = calc_npv(4, -7000, [4200, 5300, 6100, 7400], 14 / 100, 1) 
print("\nQuestion 3:\n{}\nThe discounted payback period for the cash flows with initial\
 cost $7,000 is {} yrs.".format(npv_data, period))
#Question 4  
npv, npv_data, irr, dfcash, period_1, PI = calc_npv(6, -14400, [3300] * 6, 0 / 100, 4) 
npv, npv_data_2, irr, dfcash, period_2, PI = calc_npv(6, -14400, [3300] * 6, 4 / 100, 4) 
npv, npv_data_3, irr, dfcash, period_3, PI = calc_npv(6, -14400, [3300] * 6, 19 / 100, 5) 
print("\nQuestion 4:\n{}\na)The discounted payback period is {} years if the discount rate is zero percent.\
\nb){}\nThe discounted payback period is {} years if the discount rate is 4 percent.\nc) {}\nIf the discount rate for the period is 19 percent, we don't have a payback period since we get {} years\
 and the cash flows stop after 6 years".format(dfcash, period_1, npv_data_2, period_2, npv_data_2, period_3))
#Question 5
npv_a, npv_data_a, irr, dfcash, period, PI = calc_npv(3, -30000, [23000, 13300, 11000], 11 / 100, 0)  
npv_b, npv_data_b, irr, dfcash, period, PI = calc_npv(3, -30000, [23000, 13300, 11000], 40 / 100, 0)  
print("\nQuestion 5:\n{}\na) The NPV is ${:,.2f} when the discount rate is 11%.\nb) The NPV is ${:,.2f} when the discount rate is 40%".format(npv_data_a, npv_a, npv_b))
# Question 6
npv, npv_data_6, irr, dfcash, period, PI = calc_npv(9, -14000, [3000] * 9, 11 / 100, 1)
print("\nQuestion 6:\n{}\na) The NPV is ${:,.2f} on the 11% required return.\nb) The IRR of the project is {}%.".format(npv_data_6, npv, irr)) 
# Question7 
npv, npv_data, irr, dfcash, period, PI = calc_npv(3, -7951, [4300, 3300, 5400], 0 / 100, 1) 
print("\nQuestion7:\n{}\nThe IRR for the project with the given cash flows is {}%.".format(dfcash, irr))    
# Question 8
npv_a, npv_data, irr, dfcash, period, PI = calc_npv(3, -8600, [4800, 5600, 5900], 0 / 100, 1) 
npv_b, npv_data, irr, dfcash, period, PI = calc_npv(3, -8600, [4800, 5600, 5900], 10 / 100, 1) 
npv_c, npv_data, irr, dfcash, period, PI = calc_npv(3, -8600, [4800, 5600, 5900], 18 / 100, 1) 
npv_d, npv_data, irr, dfcash, period, PI = calc_npv(3, -8600, [4800, 5600, 5900], 23 / 100, 1) 
print("\nQuestion 8:\n{}\na) The NPV is ${:,.2f} on the 0% discount rate.\nb) The NPV is ${:,.2f} on the 10% discount rate.\nc) The NPV is ${:,.2f} on the 18%\
 discount rate.\nd) The NPV is ${:,.2f} on the 23% discount rate.".format(dfcash, npv_a, npv_b, npv_c, npv_d)) 
# Question 9
npv, npv_data, irr_a, dfcash, period, PI = calc_npv(4, -36700, [19040, 14540, 12040, 9040], 1 / 100, 1) 
npv, npv_data, irr_b, dfcash, period, PI = calc_npv(4, -36700, [6580, 13080, 19580, 23580], 1 / 100, 1) 
npv_a, npv_data, irr, dfcash, period, PI = calc_npv(4, -36700, [19040, 14540, 12040, 9040], 15 / 100, 1) 
npv_b, npv_data, irr, dfcash, period, PI = calc_npv(4, -36700, [6580, 13080, 19580, 23580], 15 / 100, 1)
npv, npv_data, irr_indifferent, dfcash, period, PI = calc_npv(4, 0, [12460, 1460, -7540, -14540], 15 / 100, 1) #to find inndifferent rate I substratcted cashflow A fron cashflow B in their respective periods
print("\nQuestion 9:\n{}\na) The IRR for project A is {}%.\nb) The IRR for project B is {}%.\nc) The NPV for project A is ${:,.2f} for the 15% required \
return.\nd) The NPV for project B is ${:,.2f} on the 15% reuired return.\nc) The discount rate that would make the company  indifferent between these two projects is {}%".format(dfcash, irr_a, irr_b, npv_a, npv_b, irr_indifferent)) 
# Question 10
npv, npv_data, irr_a, dfcash, period, PI_a = calc_npv(3, -7600, [5300, 2700, 3500], 11 / 100, 1)
npv, npv_data, irr_a, dfcash, period, PI_b = calc_npv(3, -7600, [5300, 2700, 3500], 18 / 100, 1) 
npv, npv_data, irr_a, dfcash, period, PI_c = calc_npv(3, -7600, [5300, 2700, 3500], 24 / 100, 1)
print("\nQuestion 10:\n{}\na) The PI for the project with the relevent discount rate of 11% is {}.\nb) The PI for the project with the relevent discount rate of 18% is {}.\nc)The \
PI for the project with the relevent discount rate of 24% is {}.".format(dfcash, PI_a, PI_b, PI_c))
# Question 11
npv, npv_data, irr, dfcash_A, period_A, PI = calc_npv(4, -218744, [29300, 51000, 51000, 424000], 0 / 100, 3) # keep r = 0 to run my above condition in the mother function for payback with discounting
npv, npv_data, irr_a, dfcash_B, period_B, PI = calc_npv(4, -14887, [4036, 8737, 13211, 8514], 0 / 100, 2)
npv_A, npv_data_A, irr_A, dfcash, period_Ad, PI_A = calc_npv(4, -218744, [29300, 51000, 51000, 424000], 6 / 100, 3)
npv_B, npv_data_B, irr_B, dfcash, period_Bd, PI_B = calc_npv(4, -14887, [4036, 8737, 13211, 8514], 6 / 100, 2)
cashflow = pd.concat([dfcash_A['Cash_Flows'],dfcash_B['Cash_Flows']], axis = 1) #found through trail and error best way to join the dataframes in one df through their indexes
cashflow.columns = ['Cash Flows A', 'Cash Flows B']
print("\nQuestion 11:\n{}\na)The payback period for Project A is {}yrs.\nb)The payback period for Project B is {}yrs.\n\n{}\n{}\nc) The \
discounted payback period for Project A is {}yrs.\nd) The discounted payback period for Project B is {}yrs.\ne) The NPV for project A is ${:,.2f}.\nf) The NPV for project B is ${:,.2f}.\ng) The IRR for project A is {}%.\nh) The IRR for project B is {}%.\
\ni) The PI for project A is {}.\nj) The PI for project B is {}.".format(cashflow, period_A, period_B, npv_data_A, npv_data_B, period_Ad, period_Bd, npv_A, npv_B, irr_A, irr_B, PI_A, PI_B))
# Question 12
npv, npv_data, irr_Discount, dfcash_A, period_A, PI = calc_npv(4, -36429.3, [12000, 14700, 16600, 13700], 9 / 100, 3)#discounting appraoch: returned last year cash outflow to PV and added it to intial cost to derrive MIRR (Discount) 
irr_reinvest = round(np.mirr([-29800, 12000, 14700, 16600, 13700, -10200], 9 / 100, 9 / 100) * 100, 4)
irr_combination = round(np.mirr([-36429.3, 12000, 14700, 16600, 13700], 9 / 100, 9 / 100) * 100, 4)
print("\nQuestion 12:\n{}\na) The MIRR using discounting approach is {}%.\nb) The MIRR using reinvestment approach is {}%.\nc) The MIRR using combination approach is {}%.".format(dfcash_A, irr_Discount, irr_reinvest, irr_combination))
# Question 13             
npv, npv_data, irr_Discount, dfcash_B, period_A, PI = calc_npv(4, -15870.531, [6100, 6700, 6200, 5100], 9 / 100, 3)#discounting appraoch: returned last year cash outflow to PV and added it to intial cost to derrive MIRR (Discount)
irr_reinvest = round((np.mirr([-13200, 6100, 6700, 6200, 5100, -4500], 11 / 100, 9 / 100)) * 100, 4)
irr_combination = round((np.mirr([-15870.531, 6100, 6700, 6200, 5100], 11 / 100, 9 / 100)) * 100, 4) 
print("\nQuestion 13:\n{}\na) The MIRR using discounting approach is {}%.\nb) The MIRR using reinvestment approach is {}%.\nc) The MIRR using combination approach is {}%.".format(dfcash_B, irr_Discount, irr_reinvest, irr_combination))
#Question 14
npv_b, npv_data, irr, dfcash_a, period, PI_a = calc_npv(2, -64300, [-30300, -48300], 10.5 / 100, 1)
npv_c, npv_data, irr_a, dfcash, period, PI_a = calc_npv(2, -64300, [-30300, -48300], 0, 1)
npv_d, npv_data, irr_a, dfcash, period, PI_a = calc_npv(2, -64300, [-30300, -48300], 21 / 100, 1)
print("\nQuestion 14:\n{}\na) The IRR is {}%, which an error since no internal rate of revenue can be established for negative cash flows.\nb) At 10.5% the NPV is ${:,.2f}.\nc) At 0% the NPV is ${:,.2f}.\nd) At 21% the NPV is \
${:,.2f}.\n\n\n\t\t\t\t\t\t----------END of NPV-----------".format(dfcash_a, irr, npv_b, npv_c, npv_d))
#Cost Benfit Analysis Assignment
#Question1 #Question2
print("\n\n\n\t\t\t**************Cost Benefit Analysis Assignment**************n\n\nQuestion 1:    Define cost benefit analysis:\n Cost benefit analysis is the study of the benefit vs the cost of the project taking opportunity \
 cost into consideration and all projected future costs that are implied of the undertaken project. The analysis is an approach to to study the feasibilty of a new project to strategically decide if a person should\
 implement the startup or launch the underlying idea. The criteria that are used to assess such projects are the forecasted cashflows, the intial startup implementation fees, and the reuired discount rate. These\
 criteria's are further used to calculate the net present value of the project (at the end forcasted cashflow or life), the breakeven point (which is where the NPV = 0 at a specific IRR) and the modified IRR if\
 the cash flows are to be reinvested or to get a better estimate of the IRR.\n\nQuestion 2:    How is risk-benefit ration different from cost benefit analysis?\n Risk benefit analysis is an extention of the cost benefit\
 analysis. It is a more structured approach  that is used as a rational decision making tool that adds risk factors to the benefit and cost associated with the project. This extension approach takes risks that are related to\
 unanticipated events and that are based on irrational decisions people take since people are generally risk averse.")
#Question3
npv, npv_data, irr, dfcash, period, PI_emb = calc_npv(20, -3375000 , [960000] * 20, 15 / 100, 5) 
print("\nQuestion 3:\n{}\na) The overall NPV of the project is ${:,.2f}.\nb) The project will break even at {}yrs, which is the discounted payback period.\nc) EMB  should implement this project with the 15% discount rate since the \
NPV>0 and the payback period is rewarding interms of recovering intial costs and covering maintenance costs".format(npv_data, npv, period))
#Question4
npv, npv_data, irr, dfcash, period, PI = calc_npv(20, -3375000 , [960000] * 20, 30 / 100, 1) 
print("\nQuestion 4:\n{}\na) The over all net present value for the project is ${:,.2f} after taking the net benefit(cost) as cashflows and discounting them at 30% with respect th their period.\nb) At a discount rate of 30% the company\
 will never break-even during and until the 20th year(end year) since NPV<0 and the intial implementation costs are not recovered.\nc) The company should not go forward with this project, simce as stated the NPV<0 and their\
is no payback period.".format(npv_data, npv))
# Question 5
npv, npv_data, irr, dfcash, period, PI = calc_npv(20, -3375000 , [385000] * 20, 15 / 100, 1) 
print("\nQuestion 5:\n{}\na) The over all net present value for the project is ${:,.2f} after taking the net benefit(cost) as cashflows and discounting them at 15% with respect their period.\nb) At a discount rate of 15% the company\
 will never break-even during and until the 20th year(end year) since NPV<0 and the intial implementation costs are not recovered.\nc) The company should not go forward with this project, simce as stated the NPV<0 and their\
 is no payback period.".format(npv_data, npv))
# Question 6
npv, npv_data, irr, dfcash, period, PI = calc_npv(20, -3375000 , [385000] * 20, 9.5754 / 100, 19) 
print("\nQuestion 6:\n{}\na) The project will be economically feasible at NPV = 0, which is the point at which the company is indifferent and just broke even. The discount rate or IRR will thus be {:,.4f}%.\nb) The breakeven will be\
 after {}, thus taking that into consideration and discounting at 9.5754%, the project will breakeven by a negligible margin in the last year (year 20). Thus the SAP project should not be implemented since it is not feasible.\n\n\n\t\t\t\t\t\t----------END of NPV----------- ".format(npv_data, irr, period))


