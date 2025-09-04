import sys
sys.path.append('/root/nassc_code')
from my_circuit import create_circuit_without_qubit_1

optimal_params = [ 1.82876858,  3.24641369,  1.62958088,  1.65092094,  1.53970519,  1.48885995,
  1.61360675,  1.60338138, -0.05674933,  3.22233972,  1.71074834,  2.3904894,
  2.39006873,  1.90057308,  1.12667496,  2.54757948,  2.69105695,  1.96807924,
 -0.16380074,  3.00825887,  1.21191047,  2.04409067, -0.08081124,  0.15129047,
  2.3650488,   1.00597256,  0.50819349,  2.14206603,  3.13022607,  1.08640352,
  1.38612094,  2.80729928,  3.10398523,  1.97687435,  1.47502558,  2.19573618,
  2.2425441,   1.24964191,  1.03914953,  1.90718493]

def circuits():
    qc, params = create_circuit_without_qubit_1()
    param_bindings = {param: float(value) for param, value in zip(params, optimal_params)}
    qc = qc.assign_parameters(param_bindings)
    return qc
