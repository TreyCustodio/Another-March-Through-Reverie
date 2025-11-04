#   Lecture Notes on Network Layer Control Plane (10/24/2025)

##  Link State

### Dijkstra's link-state algorithm
- every node knows all link costs
- all nodes have same info
- centralized network topology
- Computes least cost paths from one node to all other nodes using a **forwarding table**

### Algorithm Steps
#### (1) Initialization
- See slide 5-13
- D(v) = min(D(v), D(x) + C_x,v)
    - c_x,v = direct path from x to v
    - c_x,w = direct path from x to w
- you trace the route to each router, identifying minimum cost path
- if no direct path, you say it is inifinty

### Quiz
- NAT, IPv6, Sunday night