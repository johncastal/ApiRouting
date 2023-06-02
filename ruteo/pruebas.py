from amplpy import AMPL
import numpy as np

# Define the distance matrix and cities
distance_matrix = np.array([[0, 10, 15], [10, 0, 20], [15, 20, 0]])
num_cities = distance_matrix.shape[0]

# Create an instance of the AMPL object
ampl = AMPL()

# Define the AMPL model
model = """
set Cities;
param Distance{Cities, Cities};

var Visit{Cities} binary;
var TotalDistance;

minimize TotalDistanceValue: sum{i in Cities, j in Cities} Distance[i,j] * Visit[i];

subject to VisitOnce {c in Cities}:
    sum {i in Cities} Visit[i] = 1;

subject to NoSubtour {c in Cities, d in Cities diff {c} }:
    sum {i in Cities: i <> c and i <> d} Visit[i] >= Visit[c] + Visit[d] - 1;
"""

# Load the model into AMPL
ampl.eval(model)

# Set the data in AMPL
cities_set = ampl.getSet('Cities')
cities_set.setValues(list(range(1, num_cities + 1)))


distance_param = ampl.getParameter('Distance')
distance_param.setDimensions(num_cities, num_cities)
for i in range(num_cities):
    for j in range(num_cities):
        distance_param.set(i+1, j+1, distance_matrix[i, j])


# Solve the model
ampl.solve()

# Retrieve and print the solution
visit_var = ampl.getVariable("Visit")
optimal_tour = [city for city in range(1, num_cities + 1) if visit_var.get(city)]

print("Optimal Tour:", optimal_tour)
