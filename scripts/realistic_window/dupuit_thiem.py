import numpy as np

def dupuit_thiem(hydr_cond:float, thickness:float, drawdown:float=None, r1:float=0.125/2, r2:float=10000, confined:bool=True, h1:float=None, h2:float=None):
    # q_inj = 2*pi*hydr_cond * thickness * drawdown / ln(r2/r1)
    # für gespanntes Grundwasser, nutzen trotzdem als Approximation
    if confined:
        q_inj = 2*np.pi*hydr_cond * thickness * drawdown / np.log(r2/r1)
    else:
        q_inj = np.pi*hydr_cond * (h2**2 - h1**2) / np.log(r2/r1)
    return q_inj


def drawdown_by_dupuit_thiem(hydr_cond:float, thickness:float, q_inj:float, r1:float=0.125/2, r2:float=10000):
    # q_inj = 2*pi*hydr_cond * thickness * drawdown / ln(r2/r1)
    # für gespanntes Grundwasser, nutzen wir trotzdem als Approximation der Absenkung

    drawdown = q_inj * np.log(r2/r1) / (2*np.pi*hydr_cond*thickness)
    return drawdown