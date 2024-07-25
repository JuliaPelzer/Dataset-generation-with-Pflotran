# Implementation of LAHM model and application to my dataset
import numpy as np
from scipy import special
from scripts.realistic_window.lahm.subsurface_params import Parameters, Domain

###### Requirements etc
# only applicable to:
# - velocities over 1m/day
# - energy extraction under 45.000 kWh/year

# LAHM model (Kinzelbach, 1987):
# - calculates temperature field
# - with continous point source
# - convective and dispersive heat transport
# - in a homogeneous confined aquifer ("homogener gespannter Porengrundwasserleiter")
# - under instationary conditions

# - equations:
# $$ \Delta T (x,y,t) = \frac{Q \cdot \Delta T_{inj}}{4 \cdot n_e \cdot M \cdot v_a \cdot \sqrt{\pi \cdot \alpha_T}}
# \cdot \exp{(\frac{x - r}{2 \cdot \alpha_L})} \cdot \frac{1}{\sqrt{r}}
# \cdot erfc(\frac{r - v_a \cdot t/R}{2 \cdot \sqrt{v_a \cdot \alpha_L \cdot t/R}}) 
# $$
# with:
# $$ r = \sqrt{x^2 + y^2 \cdot \frac{\alpha_L}{\alpha_T}} $$

# - $\Delta T$ : Gesuchte Isotherme als Differenz zur unbeeinflussten Grundwassertemperatur [K]
# - $Q$ : Injektionsrate [m 3 /s]
# - $T_{inj}$ : Differenz zwischen der Injektionstemperatur und der unbeeinflussten Grundwassertemperatur [K]
# - $n_e$ : effektive Porosität [–]
# - $M$ : genutzte, grundwassererfüllte Mächtigkeit [m]
# - $v_a$ : Abstandsgeschwindigkeit [m/s]
# - $α_{L,T}$ : Längs- und Querdispersivität [m]
# - $x$, $y$: Längs- und Querkoordinaten [m]
# - $t$: Zeit [s]
# - $R$: Retardation [–]
# - $r$: radialer Abstand vom Injektionsbrunnen [m]

######## Next steps
# TODO temperature added too high

# read input from file
# test on dataset
# adaptation to 3D
# read streamlines
# coordination transformation

def lahm_calc_T(x, y, time, parameters):
    """
    Calculate the temperature difference between the injection well and the point (x, y) at time t.
    """
    
    n_e = parameters.n_e
    M = parameters.m_aquifer
    alpha_L = parameters.alpha_L
    alpha_T = parameters.alpha_T
    R = parameters.R
    T_inj_diff = parameters.T_inj_diff
    q_inj = parameters.q_inj
    v_a = parameters.v_a

    radial_distance = _radial_distance(x, y, alpha_L, alpha_T)
    term_numerator = q_inj * T_inj_diff
    term_denominator = 4 * n_e * M * v_a * np.sqrt(np.pi * alpha_T)
    term_exponential = np.exp((x - radial_distance) / (2 * alpha_L))
    term_sqrt = 1 / np.sqrt(radial_distance)
    term_erfc = special.erfc((radial_distance - v_a * time / R) / (2 * np.sqrt(v_a * alpha_L * time / R)))
    return term_numerator / term_denominator * term_exponential * term_sqrt * term_erfc

def _radial_distance(x, y, alpha_L, alpha_T):
    return np.sqrt(x**2 + y**2*alpha_L/alpha_T)

def estimate_plume_shapeparams_lahm(T_inj_diff: float, q_inj: float, v_a: float, m_aquifer: int) -> tuple:
    params = Parameters(m_aquifer=m_aquifer, T_inj_diff=T_inj_diff, q_inj=q_inj, v_a=v_a)
    cell_size = 1 # [m]
    
    delta_T = params.T_inj_diff
    x_pos = 0
    y_pos = 0
    while delta_T > 1:
        x_pos += cell_size
        delta_T = lahm_calc_T(x_pos, y_pos, params.time_sim_sec, params)
        # print("At x=", x_pos, "m:", round(delta_T, 2), "°C Temperaturdifferenz")

    delta_T = params.T_inj_diff
    x_half = x_pos / 2
    while delta_T > 1:
        y_pos += cell_size
        delta_T = lahm_calc_T(x_half, y_pos, params.time_sim_sec, params)
        # print("At y=", y_pos, "m:", round(delta_T, 2), "°C Temperaturdifferenz")
    y_pos *= 2

    return x_pos, y_pos

if __name__ == "__main__":
    m_aquifer=30 # m
    T_inj_diff=5 # °C
    q_inj=52 / 86400 # q_inj in m^3/s
    v_a=0.0015*0.058 # darcy in m/s
    
    length_1K, width_1K = estimate_plume_shapeparams_lahm(T_inj_diff, q_inj, v_a, m_aquifer)
    print(f"Downstream-length of plume: {length_1K} m")
    print(f"Width of plume at half length: {width_1K} m")

    # plot TODO tut grad nicht so wie erwartet bei cell_size != 1
    # domain = Domain(cell_numbers=[int(x_pos)+2, int(y_pos)+2], cell_size=cell_size)
    # delta_T_grid = lahm.delta_T(domain.x_grid, domain.y_grid, params.time_sim_sec, params)
    # print(delta_T_grid)
    # plt.imshow(delta_T_grid, cmap='hot', interpolation='nearest')
    # plt.colorbar()
    # plt.contour(delta_T_grid, colors='black', levels = [1,5])
    # plt.show()    

