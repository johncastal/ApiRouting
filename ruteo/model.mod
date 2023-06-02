set Cities;
param Distance{Cities, Cities};

# Objective function: minimize total distance
var TotalDistance;

# Variables: indicate if a city is visited
var Visit{Cities} binary;

# Constraints: ensure each city is visited exactly once
subject to VisitOnce {c in Cities}:
    sum {i in Cities} Visit[i] = 1;

# Constraints: prevent subtours
subject to NoSubtour {c in Cities, d in Cities diff {c}}:
    sum {i in Cities: i <> c and i <> d} Visit[i] >= Visit[c] + Visit[d] - 1;

# Variables: path between cities
var p{Cities, Cities} binary;

# Parameter: binary variable indicating if a city is visited
param b{Cities} binary;

# Objective function: minimize total distance
minimize TotalDistanceValue: sum {i in Cities, j in Cities} Distance[i,j] * p[i,j];

subject to flow_out {i in Cities}:
    sum {j in Cities} p[i,j] - sum {j in Cities} p[j,i] = b[i] - Visit[i];

subject to flow_in {i in Cities}:
    sum {j in Cities} p[j,i] - sum {j in Cities} p[i,j] = Visit[i] - b[i];

solve;
