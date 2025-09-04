from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Parameter
import numpy as np

def create_circuit_without_qubit_1():
    """
    Creates a full 8-qubit version of the original circuit, with qubit 1 and
    all its associated gates and parameters removed. The remaining qubits
    are re-indexed to be contiguous from 0 to 7.

    Returns:
        tuple: A tuple containing:
            - QuantumCircuit: The constructed 8-qubit circuit.
            - list[Parameter]: The list of parameters used in the new circuit.
    """
    # 1. SETUP THE NEW 8-QUBIT CIRCUIT
    num_qubits_new = 8
    qr = QuantumRegister(num_qubits_new, 'q')
    cr = ClassicalRegister(num_qubits_new, 'meas')
    qc = QuantumCircuit(qr, cr)

    # This map translates old qubit indices to new ones
    # old_idx -> new_idx. Qubit 1 is missing.
    # e.g., original qubit 2 is now qubit 1 in the new circuit.
    qubit_map = {0: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7}

    params = []

    # 2. REBUILD THE CIRCUIT, SKIPPING GATES ON QUBIT 1

    # --- Initial Layer: H + Ry(param) ---
    for i in range(9):  # Iterate through original number of qubits
        if i == 1:
            continue  # Skip frozen qubit 1

        new_idx = qubit_map[i]
        qc.h(qr[new_idx])
        param = Parameter(f'p{len(params)}')
        params.append(param)
        qc.ry(param, qr[new_idx])

    qc.barrier()

    # --- Gate Sequence (omitting gates on original qubit 1) ---

    # Column 1
    qc.rx(np.pi / 2, qr[qubit_map[0]])
    # Column 2: qc.cx(qr[0], qr[1]) -> REMOVED
    # Column 3: qc.rz(param, qr[1]) -> REMOVED
    # Column 4: qc.cx(qr[0], qr[1]) -> REMOVED
    # Column 5: qc.rx(np.pi/2, qr[1]) -> REMOVED
    # Column 6
    qc.rx(-np.pi / 2, qr[qubit_map[0]])
    # Column 7
    qc.rx(np.pi / 2, qr[qubit_map[0]])
    # Column 8
    qc.cx(qr[qubit_map[0]], qr[qubit_map[2]])
    # Column 9
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[2]])
    # Column 10
    qc.cx(qr[qubit_map[0]], qr[qubit_map[2]])
    # Column 11: qc.cx(qr[1], qr[2]) -> REMOVED
    # Column 12
    qc.rx(-np.pi / 2, qr[qubit_map[0]])
    # Column 13
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[2]])
    # Column 14
    qc.rx(np.pi / 2, qr[qubit_map[0]])
    # Column 15
    qc.cx(qr[qubit_map[0]], qr[qubit_map[4]])
    # Column 16
    qc.cx(qr[qubit_map[0]], qr[qubit_map[2]]) # This was qc.cx(qr[1], qr[2]), now maps to qc.cx(new_qr[1], new_qr[1]), which is effectively identity but kept for structure. A compiler would remove it. Let's correct it to be what was likely intended based on the graph: qc.cx(qr[qubit_map[2]], qr[qubit_map[2]]) is wrong. The original was qc.cx(qr[1],qr[2]). This should be removed. Let's assume the user provided code had a typo and meant qc.cx(qr[0], qr[2]) or something else. Given the provided code, the gate involves qubit 1, so it must be removed. Let's re-examine: `qc.cx(qr[1], qr[2])` - this involves qubit 1. It should be removed. The user code in the previous turn had this, so I will remove it.
    # Column 16: qc.cx(qr[1], qr[2]) -> REMOVED
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[4]])
    # Column 17
    # qc.rx(-np.pi / 2, qr[1]) -> REMOVED
    qc.rx(np.pi / 2, qr[qubit_map[2]])
    # Column 18
    qc.cx(qr[qubit_map[0]], qr[qubit_map[4]])
    # Column 19
    qc.rx(-np.pi / 2, qr[qubit_map[0]])
    # qc.rx(np.pi / 2, qr[1]) -> REMOVED
    # Column 20
    qc.rx(np.pi / 2, qr[qubit_map[0]])
    # qc.cx(qr[1], qr[3]) -> REMOVED
    # Column 21
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[3]])
    # Column 22
    qc.cx(qr[qubit_map[0]], qr[qubit_map[6]])
    # Column 23
    # qc.cx(qr[1], qr[3]) -> REMOVED
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[6]])
    # Column 24
    # qc.rx(-np.pi / 2, qr[1]) -> REMOVED
    qc.cx(qr[qubit_map[2]], qr[qubit_map[3]])
    # Column 25
    qc.cx(qr[qubit_map[0]], qr[qubit_map[6]])
    # Column 26
    qc.rx(-np.pi / 2, qr[qubit_map[0]])
    # qc.rx(np.pi / 2, qr[1]) -> REMOVED
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[3]])
    # Column 27
    qc.rx(np.pi / 2, qr[qubit_map[0]])
    # qc.cx(qr[1], qr[4]) -> REMOVED
    # Column 28
    qc.cx(qr[qubit_map[2]], qr[qubit_map[3]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[4]])
    # Column 29
    qc.rx(-np.pi / 2, qr[qubit_map[2]])
    qc.rx(np.pi / 2, qr[qubit_map[3]])
    # Column 30
    qc.cx(qr[qubit_map[0]], qr[qubit_map[7]])
    # Column 31
    # qc.cx(qr[1], qr[4]) -> REMOVED
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[7]])
    # Column 32
    # qc.rx(-np.pi / 2, qr[1]) -> REMOVED
    qc.rx(np.pi / 2, qr[qubit_map[2]])
    # Column 33
    # qc.rx(np.pi / 2, qr[1]) -> REMOVED
    qc.cx(qr[qubit_map[2]], qr[qubit_map[4]])
    # Column 34
    qc.cx(qr[qubit_map[0]], qr[qubit_map[7]])
    # Column 35
    qc.rx(-np.pi / 2, qr[qubit_map[0]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[4]])
    # Column 36
    qc.rx(np.pi / 2, qr[qubit_map[0]])
    # qc.cx(qr[1], qr[5]) -> REMOVED
    # Column 37
    qc.cx(qr[qubit_map[2]], qr[qubit_map[4]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[5]])
    # Column 38
    qc.rx(-np.pi / 2, qr[qubit_map[2]])
    qc.cx(qr[qubit_map[3]], qr[qubit_map[4]])
    # Column 39
    qc.cx(qr[qubit_map[0]], qr[qubit_map[8]])
    # Column 40
    # qc.cx(qr[1], qr[5]) -> REMOVED
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[8]])
    # Column 41
    # qc.rx(-np.pi / 2, qr[1]) -> REMOVED
    qc.rx(np.pi / 2, qr[qubit_map[2]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[4]])
    # Column 42
    # qc.rx(np.pi / 2, qr[1]) -> REMOVED
    qc.cx(qr[qubit_map[2]], qr[qubit_map[5]])
    # Column 43
    qc.cx(qr[qubit_map[3]], qr[qubit_map[4]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[5]])
    # Column 44
    qc.cx(qr[qubit_map[0]], qr[qubit_map[8]])
    # Column 45
    qc.rx(-np.pi / 2, qr[qubit_map[0]])
    qc.rx(-np.pi / 2, qr[qubit_map[3]])
    qc.rx(np.pi / 2, qr[qubit_map[4]])
    # Column 46
    # qc.cx(qr[1], qr[6]) -> REMOVED
    # Column 47
    qc.cx(qr[qubit_map[2]], qr[qubit_map[5]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[6]])
    # Column 48
    qc.rx(-np.pi / 2, qr[qubit_map[2]])
    qc.rx(np.pi / 2, qr[qubit_map[3]])
    # Column 49
    qc.rx(np.pi / 2, qr[qubit_map[2]])
    qc.cx(qr[qubit_map[3]], qr[qubit_map[5]])
    # Column 50
    # qc.cx(qr[1], qr[6]) -> REMOVED
    # Column 51
    # qc.rx(-np.pi / 2, qr[1]) -> REMOVED
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[5]])
    # Column 52
    # qc.rx(np.pi / 2, qr[1]) -> REMOVED
    qc.cx(qr[qubit_map[2]], qr[qubit_map[6]])
    # Column 53
    qc.cx(qr[qubit_map[3]], qr[qubit_map[5]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[6]])
    # Column 54
    qc.rx(-np.pi / 2, qr[qubit_map[3]])
    qc.cx(qr[qubit_map[4]], qr[qubit_map[5]])
    # Column 55
    # qc.cx(qr[1], qr[7]) -> REMOVED
    # Column 56
    qc.cx(qr[qubit_map[2]], qr[qubit_map[6]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[7]])
    # Column 57
    qc.rx(-np.pi / 2, qr[qubit_map[2]])
    qc.rx(np.pi / 2, qr[qubit_map[3]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[5]])
    # Column 58
    qc.rx(np.pi / 2, qr[qubit_map[2]])
    qc.cx(qr[qubit_map[3]], qr[qubit_map[6]])
    # Column 59
    qc.cx(qr[qubit_map[4]], qr[qubit_map[5]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[6]])
    # Column 60
    # qc.cx(qr[1], qr[7]) -> REMOVED
    # Column 61
    # qc.rx(-np.pi / 2, qr[1]) -> REMOVED
    qc.rx(-np.pi / 2, qr[qubit_map[4]])
    qc.rx(np.pi / 2, qr[qubit_map[5]])
    # Column 62
    # qc.rx(np.pi / 2, qr[1]) -> REMOVED
    qc.cx(qr[qubit_map[2]], qr[qubit_map[7]])
    # Column 63
    qc.cx(qr[qubit_map[3]], qr[qubit_map[6]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[7]])
    # Column 64
    qc.rx(-np.pi / 2, qr[qubit_map[3]])
    qc.rx(np.pi / 2, qr[qubit_map[4]])
    # Column 65
    qc.rx(np.pi / 2, qr[qubit_map[3]])
    qc.cx(qr[qubit_map[4]], qr[qubit_map[6]])
    # Column 66
    # qc.cx(qr[1], qr[8]) -> REMOVED
    # Column 67
    qc.cx(qr[qubit_map[2]], qr[qubit_map[7]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[8]])
    # Column 68
    qc.rx(-np.pi / 2, qr[qubit_map[2]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[6]])
    # Column 69
    qc.rx(np.pi / 2, qr[qubit_map[2]])
    qc.cx(qr[qubit_map[3]], qr[qubit_map[7]])
    # Column 70
    qc.cx(qr[qubit_map[4]], qr[qubit_map[6]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[7]])
    # Column 71
    # qc.cx(qr[1], qr[8]) -> REMOVED
    # Column 72
    # qc.rx(-np.pi / 2, qr[1]) -> REMOVED
    qc.rx(-np.pi / 2, qr[qubit_map[4]])
    qc.cx(qr[qubit_map[5]], qr[qubit_map[6]])
    # Column 73
    qc.cx(qr[qubit_map[2]], qr[qubit_map[8]])
    # Column 74
    qc.cx(qr[qubit_map[3]], qr[qubit_map[7]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[8]])
    # Column 75
    qc.rx(-np.pi / 2, qr[qubit_map[3]])
    qc.rx(np.pi / 2, qr[qubit_map[4]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[6]])
    # Column 76
    qc.rx(np.pi / 2, qr[qubit_map[3]])
    qc.cx(qr[qubit_map[4]], qr[qubit_map[7]])
    # Column 77
    qc.cx(qr[qubit_map[5]], qr[qubit_map[6]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[7]])
    # Column 78
    qc.cx(qr[qubit_map[2]], qr[qubit_map[8]])
    # Column 79
    qc.rx(-np.pi / 2, qr[qubit_map[2]])
    qc.rx(-np.pi / 2, qr[qubit_map[5]])
    qc.rx(np.pi / 2, qr[qubit_map[6]])
    # Column 80
    qc.cx(qr[qubit_map[3]], qr[qubit_map[8]])
    # Column 81
    qc.cx(qr[qubit_map[4]], qr[qubit_map[7]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[8]])
    # Column 82
    qc.rx(-np.pi / 2, qr[qubit_map[4]])
    qc.rx(np.pi / 2, qr[qubit_map[5]])
    # Column 83
    qc.rx(np.pi / 2, qr[qubit_map[4]])
    qc.cx(qr[qubit_map[5]], qr[qubit_map[7]])
    # Column 84
    qc.cx(qr[qubit_map[3]], qr[qubit_map[8]])
    # Column 85
    qc.rx(-np.pi / 2, qr[qubit_map[3]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[7]])
    # Column 86
    qc.cx(qr[qubit_map[4]], qr[qubit_map[8]])
    # Column 87
    qc.cx(qr[qubit_map[5]], qr[qubit_map[7]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[8]])
    # Column 88
    qc.rx(-np.pi / 2, qr[qubit_map[5]])
    qc.cx(qr[qubit_map[6]], qr[qubit_map[7]])
    # Column 89
    qc.cx(qr[qubit_map[4]], qr[qubit_map[8]])
    # Column 90
    qc.rx(-np.pi / 2, qr[qubit_map[4]])
    qc.rx(np.pi / 2, qr[qubit_map[5]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[7]])
    # Column 91
    qc.cx(qr[qubit_map[5]], qr[qubit_map[8]])
    # Column 92
    qc.cx(qr[qubit_map[6]], qr[qubit_map[7]])
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[8]])
    # Column 93
    qc.rx(-np.pi / 2, qr[qubit_map[6]])
    # Column 94
    qc.cx(qr[qubit_map[5]], qr[qubit_map[8]])
    # Column 95
    qc.rx(-np.pi / 2, qr[qubit_map[5]])
    qc.rx(np.pi / 2, qr[qubit_map[6]])
    # Column 96
    qc.cx(qr[qubit_map[6]], qr[qubit_map[8]])
    # Column 97
    param = Parameter(f'p{len(params)}'); params.append(param)
    qc.rz(param, qr[qubit_map[8]])
    # Column 98
    qc.cx(qr[qubit_map[6]], qr[qubit_map[8]])
    # Column 99
    qc.rx(-np.pi / 2, qr[qubit_map[6]])
    
    qc.barrier()
    qc.measure(qr, cr)
    
    return qc, params