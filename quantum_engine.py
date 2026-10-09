
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA


def optimize_routes():
    routes = {
        "Hyderabad → Delhi": 9480,
        "Hyderabad → Mumbai": 8532,
        "Delhi → Mumbai": 9006,
        "Chennai → Bengaluru": 4200,
        "Mumbai → Singapore": 7800,
        "Bengaluru → London": 11500,
        "Delhi → Dubai": 7200,
        "Kolkata → Bangkok": 6500,
        "Chennai → Singapore": 8100,
        "Hyderabad → Bengaluru": 3900,
    }

    # Create one decision qubit for each of the 10 routes.
    problem = QuadraticProgram("quantum_flight_optimizer")

    for i in range(len(routes)):
        problem.binary_var(name=f"route_{i}")

    problem.minimize(linear=list(routes.values()))

    # Exactly one route must be selected.
    problem.linear_constraint(
        linear=[1] * len(routes),
        sense="==",
        rhs=1,
        name="choose_one_route",
    )

    # Lightweight QAOA settings for a local simulation.
    sampler = StatevectorSampler()
    qaoa = QAOA(
        sampler=sampler,
        optimizer=COBYLA(maxiter=3),
        reps=1,
    )

    optimizer = MinimumEigenOptimizer(qaoa)
    result = optimizer.solve(problem)

    selected = [
        name
        for name, value in zip(routes.keys(), result.x)
        if value > 0.5
    ]

    # Create a clear schematic of a 10-qubit QAOA circuit.
    circuit = QuantumCircuit(10)

    for qubit in range(10):
        circuit.h(qubit)

    for qubit in range(9):
        circuit.cx(qubit, qubit + 1)
        circuit.rz(0.5, qubit + 1)
        circuit.cx(qubit, qubit + 1)

    for qubit in range(10):
        circuit.rx(0.5, qubit)

    return {
        "routes": routes,
        "selected_route": selected[0] if selected else None,
        "emissions": float(result.fval),
        "status": str(result.status),
        "circuit": circuit.draw(output="text").__str__(),
    }