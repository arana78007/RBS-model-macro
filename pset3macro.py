import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np

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
#above sets the parameters, below we implent main which recursivley returns to us list of each variable#
consumption = []
capital = [0]
shock = [0] 
wage = []

def shock_t(t):
    shock_temp = rho*shock[t]
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
            capital_t_1(capital,shock,t)
            shock_t(t)
        elif t == 11:
            shock[-1] = 1
            consumption_t(capital,shock,t)
            wage_t(capital,shock,t)
            capital_t_1(capital,shock,t)
            shock_t(t)
        else:
            consumption_t(capital,shock,t)
            wage_t(capital,shock,t)
            capital_t_1(capital,shock,t)
            shock_t(t)
    return consumption, capital, wage, shock

main(n=100)


plt.plot(np.array(consumption, dtype=float), color="blue")

plt.savefig('test')
