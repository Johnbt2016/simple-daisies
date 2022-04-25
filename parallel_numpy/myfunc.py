import numpy as np

bottom_density_curves = np.load('BottomDensity.npy')
c = np.load('Oxfordian.npy')
t_c = c[:,1] + c[:,2]
m_c = np.max(t_c)
normalized_uep = t_c / m_c
oil_surface_density = 800
gas_surface_density = 0.8


def discount_losses(exp_oil, exp_gas, vol_to_discount):
    
    gas_scf = exp_gas * 5800 * 1e6
    oil_bbl = exp_oil * 1e6
    vol_gas_surface = exp_gas * 5800 * 1e6 * 0.0283168 # (in m3)
    vol_oil_surface = exp_oil * 1e6 * 0.16 # (in m3)

    m_gas = vol_gas_surface * gas_surface_density
    m_oil = vol_oil_surface * oil_surface_density

    total_mass = m_gas + m_oil

    cumm_gor = gas_scf / oil_bbl

    # Getting bottom density from GOR and corresponding STS
    bottom_density = np.interp(cumm_gor, bottom_density_curves[:,1], bottom_density_curves[:,2])
    eq_sts = np.interp(cumm_gor, bottom_density_curves[:,1], bottom_density_curves[:,0])

    normalized_uep_at_eq_sts = np.interp(eq_sts, bottom_density_curves[:,0], normalized_uep)

    # Bottom volume from mass and bottom density
    vol_bottom = total_mass / bottom_density
    
    # Discounted volume
    final_volume = vol_bottom - vol_to_discount
    # print(vol_bottom, vol_to_discount, final_volume)

    # UEP curve with bottom volumes to recompute composition
    n_uep_scaleup = vol_bottom / normalized_uep_at_eq_sts
    bottom_uep = n_uep_scaleup * normalized_uep

    # STS corresponding to the final volume
    sts_vol_to_match = np.interp(final_volume, bottom_uep, bottom_density_curves[:,0])

    # Use this STS value to retrieve GOR
    gor_at_final_volume = np.interp(sts_vol_to_match, bottom_density_curves[:,0], bottom_density_curves[:,1])

    # Rebuild UEP curve at surface conditions
    n_uep_scaleup = (exp_oil + exp_gas) / normalized_uep_at_eq_sts
    surface_uep = n_uep_scaleup * normalized_uep

    # Read the final volume at surfce conditions
    final_surface_volume = np.interp(sts_vol_to_match, bottom_density_curves[:,0], surface_uep)

    # Recompute volume of oil and gas using GOT and final volume
    final_gas = final_surface_volume / (1 + 5800 / gor_at_final_volume)
    final_oil = final_surface_volume - final_gas

    return final_oil, final_gas, gor_at_final_volume