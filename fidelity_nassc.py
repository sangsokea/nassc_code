from my_circuit import create_circuit_without_qubit_1
from qiskit import transpile, execute, Aer
from my_fake_brisbane import FakeBrisbane
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from qiskit.transpiler import PassManager, CouplingMap
from qiskit.transpiler.preset_passmanagers import level_3_pass_manager
from qiskit.transpiler.passmanager_config import PassManagerConfig
from qiskit.providers.aer.noise import NoiseModel

# 1. Create the circuit and bind parameters
qc, params = create_circuit_without_qubit_1()
optimal_params = [ 1.82876858,  3.24641369,  1.62958088,  1.65092094,  1.53970519,  1.48885995,
  1.61360675,  1.60338138, -0.05674933,  3.22233972,  1.71074834,  2.3904894,
  2.39006873,  1.90057308,  1.12667496,  2.54757948,  2.69105695,  1.96807924,
 -0.16380074,  3.00825887,  1.21191047,  2.04409067, -0.08081124,  0.15129047,
  2.3650488,   1.00597256,  0.50819349,  2.14206603,  3.13022607,  1.08640352,
  1.38612094,  2.80729928,  3.10398523,  1.97687435,  1.47502558,  2.19573618,
  2.2425441,   1.24964191,  1.03914953,  1.90718493]
param_bindings = {param: float(value) for param, value in zip(params, optimal_params)}
qc = qc.assign_parameters(param_bindings)

# 2. Get the backend and simulator
backend = FakeBrisbane()
simulator = Aer.get_backend('qasm_simulator')
noise_model = NoiseModel.from_backend(backend)

# 3. Transpile the circuit with different methods
coupling_map = CouplingMap(backend.configuration().coupling_map)

# NASSCSwap
config_nassc = PassManagerConfig(
            initial_layout=None,
            basis_gates= backend.configuration().basis_gates,
            coupling_map= coupling_map,
            routing_method='NASSCSwap',
            seed_transpiler=11,
            enable_factor_block=True,
            enable_factor_commute_0=True,
            enable_factor_commute_1=True,
            factor_block=1,
            factor_commute_0=1,
            factor_commute_1=1,
            hardware=backend)
pm_nassc = level_3_pass_manager(config_nassc)
transpiled_qc_nassc = pm_nassc.run(qc)


# 4. Run all circuits
shots = 8192
result_original = execute(qc, simulator, shots=shots, noise_model=noise_model).result()
counts_original = result_original.get_counts()

result_nassc = execute(transpiled_qc_nassc, simulator, shots=shots, noise_model=noise_model).result()
counts_nassc = result_nassc.get_counts()


# 5. Get top 5 bitstrings and prepare data for plotting and CSV
top5_original = sorted(counts_original.items(), key=lambda item: item[1], reverse=True)[:5]
top5_nassc = sorted(counts_nassc.items(), key=lambda item: item[1], reverse=True)[:5]

csv_rows = []
def to_csv_rows(circuit_name, top5_counts):
    for rank, (bitstring, count) in enumerate(top5_counts, 1):
        csv_rows.append({
            'circuit': circuit_name,
            'rank': rank,
            'bitstring': bitstring,
            'count': count,
            'probability': count / shots
        })

to_csv_rows('original', top5_original)
to_csv_rows('transpiled_nassc', top5_nassc)

# Save to CSV
df = pd.DataFrame(csv_rows)
df.to_csv("brisbane_fidelity_comparison_all_noise.csv", index=False)

# 6. Plot results
fig, axs = plt.subplots(2, 1, figsize=(12, 24), sharex=False)

def plot_top5(ax, data, title):
    bitstrings = [bit for bit, _ in data]
    probs = [count / shots for _, count in data]
    x = np.arange(len(bitstrings))

    bars = ax.bar(x, probs, color='skyblue')
    ax.set_title(title, fontsize=11)
    ax.set_ylim(0, max(probs) + 0.05 if probs else 0.1)
    ax.set_ylabel("Probability")
    ax.set_xticks(x)
    ax.set_xticklabels(bitstrings, fontsize=9)
    ax.grid(axis='y', linestyle='--')

    for bar, prob in zip(bars, probs):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.005,
                f"{prob:.3f}", ha='center', va='bottom', fontsize=8)

plot_top5(axs[0], top5_original, "Original Circuit - Top-5 Bitstrings")
plot_top5(axs[1], top5_nassc, "Transpiled Circuit (NASSCSwap) - Top-5 Bitstrings")

plt.xlabel("Bitstring")
plt.tight_layout()
plt.savefig("fidelity_comparison_all_plot_noise.png")

print("Fidelity analysis complete. Results saved to brisbane_fidelity_comparison_all_noise.csv and fidelity_comparison_all_plot_noise.png")
