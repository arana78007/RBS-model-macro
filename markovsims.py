import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import statsmodels.api as sm

gamma_1 = 0.69
gamma_2 = -5.15

gamma_3 = 0.81
gamma_4 = 2.18

gamma_5 = 0.31
gamma_6 = -0.83

alpha = 0.3
beta = 0.99
rho = 0.9
delta = 0.1
eta = 0.5

C_s = 0.434
L_s = 0.388
Y = 0.596
Y_K = (1/alpha)*((1/beta)-(1-delta))
#above sets the parameters, below main func just forward iterates#
#prob some allignment issues by one or two periods, doesn't really matter tho#
investment = []
gdp = []
consumption = []
labour = []
capital = [0]
shock = [0] 
wage = []

def investment_t(t):
    inves_temp = ((1/Y_K)*gamma_3-(1-delta)*(1/Y_K))*capital[t] + ((1/Y_K)*gamma_4)*shock[t]
    investment.append(inves_temp)
    return investment

def gdp_t(t):
    gdp_temp = (1/2)*(((C_s/Y)*gamma_1-(1-delta)*(1/Y_K)+(1/Y_K)*gamma_3)*capital[t]+ (((C_s/Y)*gamma_2)+(1/Y_K)*gamma_4)*shock[t])
    gdp.append(gdp_temp)
    return gdp 

def labour_t(t):
    labour_temp = (alpha-eta*gamma_1)/((L_s/(1-L_s))+alpha)*capital[t] + (-1*eta*gamma_2)/((L_s/(1-L_s))+alpha)*shock[t]
    labour.append(labour_temp)
    return labour

def shock_t(t):
    shock_temp = rho*(shock[t]+np.random.normal(0,1))
    shock.append(shock_temp)
    return shock
    

def consumption_t(capital,shock,t):
    c_temp = gamma_1*capital[t] + gamma_2*shock[t]
    consumption.append(c_temp)
    return consumption

def capital_t_1(capital, shock,t):
    cap_temp = gamma_3*capital[t] + gamma_4*shock[t]
    capital.append(cap_temp)
    return capital

def wage_t(capital,shock,t):
    wage_temp = gamma_5*capital[t]+gamma_6*shock[t]
    wage.append(wage_temp)
    return wage

def main(n):
    for t in range(0,n):
        if t <= 10:
            consumption_t(capital,shock,t)
            wage_t(capital,shock,t)
            labour_t(t)
            gdp_t(t)
            investment_t(t)
            capital_t_1(capital,shock,t)
            shock_t(t)
        elif t == 11:
            #introduces a shock to the model of 1#
            shock[-1] = 1
            consumption_t(capital,shock,t)
            wage_t(capital,shock,t)
            labour_t(t)
            gdp_t(t)
            investment_t(t)
            capital_t_1(capital,shock,t)
            shock_t(t)
        elif t == 99:
            consumption_t(capital,shock,t)
            wage_t(capital,shock,t)
            labour_t(t)
            gdp_t(t)
            investment_t(t)
        else:
            consumption_t(capital,shock,t)
            wage_t(capital,shock,t)
            labour_t(t)
            gdp_t(t)
            investment_t(t)
            capital_t_1(capital,shock,t)
            shock_t(t)
    return consumption, wage,labour, gdp, investment, capital, shock

main(n=100)


plt.plot(consumption, label='consumption',color="blue")
plt.plot(investment, label='investment', color='red')
plt.plot(gdp, label='Y', color='green')
plt.plot(shock,label='shock', color='orange')
plt.plot(capital, label='capital', color='brown')
plt.plot(wage, label='wage', color='purple')
plt.plot(labour, label='labour',color='pink')

plt.legend()
#plt.savefig('testmarkovfinalfinal')

plt.plot()

cycle_consumption, trend_consumption = sm.tsa.filters.hpfilter(consumption, lamb=1600)
cycle_inves, trend_inves = sm.tsa.filters.hpfilter(investment, lamb=1600)
cycle_gdp, trend_gdp = sm.tsa.filters.hpfilter(gdp, lamb=1600)
cycle_cap, trend_cap = sm.tsa.filters.hpfilter(capital, lamb=1600)
cycle_wage, trend_wage = sm.tsa.filters.hpfilter(wage, lamb=1600)
cycle_lab, trend_lab = sm.tsa.filters.hpfilter(labour, lamb=1600)
#above gives the cycle and trend seperations for each series#

#add the plots for the labour market side stuff#

#below we compute the stats for each#
print('covariance of output and investment:' ,np.corrcoef(cycle_gdp,cycle_inves)[0,1])
print('covariance of output and consumption:' ,np.corrcoef(cycle_gdp,cycle_consumption)[0,1])
print('covariance of output and capital:' ,np.corrcoef(cycle_gdp,cycle_cap)[0,1])
print('covariance of output and wage:' ,np.corrcoef(cycle_gdp,cycle_wage)[0,1])
print('covariance of output and labour:' ,np.corrcoef(cycle_gdp,cycle_lab)[0,1])

output_volatility = np.std(cycle_gdp)

print('volatility of investment relative to output:' ,np.std(cycle_inves)/(output_volatility))
print('volatility of consumption relative to output:' ,np.std(cycle_consumption)/(output_volatility))
print('volatility of capital relative to output:' ,np.std(cycle_cap)/(output_volatility))
print('volatility of wage relative to output:' ,np.std(cycle_wage)/(output_volatility))
print('volatility of labour relative to ouput:' ,np.std(cycle_lab)/(output_volatility))
