from typing import List

# Create a type alias
Vector = List[float]  # [2.0, 5.3, 1.8, 2.054]

def scale_vector(vector: Vector, scalar: float) -> Vector:
    return [x * scalar for x in vector]

v = [1.0, 2.0, 3.0]
result = scale_vector(v, 2.0)
print(result)  # Output: [2.0, 4.0, 6.0]




