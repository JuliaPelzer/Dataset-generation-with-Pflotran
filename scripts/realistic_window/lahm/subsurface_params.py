from dataclasses import dataclass
import numpy as np
import scripts.realistic_window.lahm.utils_and_visu as utils


@dataclass
class Domain:
    cell_numbers : list[int]
    cell_size : int
    # Umweltministerium BW: für t > 10.000 Tage = 27.4 Jahre kann ein Steady state angenommen werden und das Ergebnis stimmt mit einer stationären Lösung überein

    def __post_init__(self):
        self.x_lin = np.linspace(0, self.cell_numbers[0]*int(self.cell_size), self.cell_numbers[0])
        self.y_lin = np.linspace(0, self.cell_numbers[1]*int(self.cell_size), self.cell_numbers[1])
        self.x_grid, self.y_grid = np.meshgrid(self.x_lin, self.y_lin)

# helper functions
def _calc_R(ne, Cw, Cs):
    return ((1-ne)*Cs+ne*Cw)/(ne*Cw)

def _calc_alpha_T(alpha_L):
    return 0.1*alpha_L

def _approx_prop_of_porous_media(prop_water : float, prop_solid : float, n_e : float) -> float:
    return prop_water * n_e + prop_solid * (1-n_e) # new compared to LAHM, rule source: diss.tex

@dataclass
class Parameters:
    m_aquifer : float #[5,14]
    T_inj_diff : float
    q_inj : float # e.g. 0.00024 #[m^3/s]
    v_a : float # [m/s]

    n_e : float = 0.25
    C_w : float = 4.2e6 # [J/m^3K]
    C_s : float = 2.4e6
    C_m : float = _approx_prop_of_porous_media(C_w, C_s, n_e)
    R : float = _calc_R(n_e, C_w, C_s) #2.7142857142857144
    rho_w : float = 1000
    rho_s : float = 2800
    g : float = 9.81
    eta : float = 1e-3
    alpha_L : float = 10 #[1,30]

    time_sim : float = 27.5 #?[years]
    # Umweltministerium BW: für t > 10.000 Tage = 27.4 Jahre kann ein Steady state angenommen werden und das Ergebnis stimmt mit einer stationären Lösung überein
    time_sim_sec : np.array = utils._time_years_to_seconds(time_sim) # [s]

    lambda_w : float = 0.65 # [-], source: diss
    lambda_s : float = 1.0 # [-], source: diss
    lambda_m : float = _approx_prop_of_porous_media(lambda_w, lambda_s, n_e)


    def __post_init__(self):
        self.alpha_T : float = _calc_alpha_T(self.alpha_L)

        self.v_a_m_per_day = np.round(self.v_a*24*60*60, 12) # [m/day]
        # first lahm requirement:
        # assert self.v_a_m_per_day >= 1, "v_a must be at least 1 m per day to get a valid result"

        # check second lahm requirement: energy extraction / injection must be at most 45.000 kWh/year
        energy_extraction_boundary = 45000e3/365/24 #[W] = [J/s]
        energy_extraction_real = self.q_inj * self.C_w * self.T_inj_diff
        # assert energy_extraction_real <= energy_extraction_boundary, f"energy extraction must be at most 45.000 kWh/year but is at {energy_extraction_real} W" # TODO (einheiten korrekt??)