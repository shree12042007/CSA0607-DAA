"""
Task 1: Fractional Knapsack Problem (Logistics Vehicle Loading)
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
Strategy: Greedy Algorithm (Sort by Value-to-Weight Ratio Descending)
"""

class Package:
    def __init__(self, pkg_id, weight, value):
        self.pkg_id = pkg_id
        self.weight = float(weight)
        self.value = float(value)
        self.ratio = self.value / self.weight if self.weight > 0 else 0.0

def load_vehicle(packages, capacity):
    if capacity <= 0 or not packages:
        return [], 0.0

    # Sort packages in descending order of value-to-weight ratio
    sorted_packages = sorted(packages, key=lambda p: p.ratio, reverse=True)

    remaining_capacity = float(capacity)
    total_value = 0.0
    loaded_manifest = []

    for pkg in sorted_packages:
        if remaining_capacity == 0:
            break

        if pkg.weight <= remaining_capacity:
            fraction = 1.0
            taken_weight = pkg.weight
            earned_value = pkg.value
        else:
            fraction = remaining_capacity / pkg.weight
            taken_weight = remaining_capacity
            earned_value = pkg.value * fraction

        loaded_manifest.append({
            "pkg_id": pkg.pkg_id,
            "fraction": round(fraction, 4),
            "weight_loaded": round(taken_weight, 2),
            "value_added": round(earned_value, 2)
        })
        total_value += earned_value
        remaining_capacity -= taken_weight

    return loaded_manifest, round(total_value, 2)

if __name__ == "__main__":
    print("=== TASK 1: LOGISTICS VEHICLE LOADING (FRACTIONAL KNAPSACK) ===")
    pkgs1 = [
        Package("PKG-1", 10, 60),
        Package("PKG-2", 20, 100),
        Package("PKG-3", 30, 120)
    ]
    cap1 = 50
    manifest1, val1 = load_vehicle(pkgs1, cap1)
    print(f"\n[Test Case 1] Capacity = {cap1} kg")
    for item in manifest1:
        print(f"  Loaded {item['pkg_id']}: Fraction={item['fraction']}, Weight={item['weight_loaded']}kg, Value={item['value_added']}")
    print(f"Total Maximum Value: {val1}")

    manifest2, val2 = load_vehicle(pkgs1, 0)
    print(f"\n[Test Case 2] Capacity = 0 kg -> Manifest: {manifest2}, Total Value: {val2}")

    manifest3, val3 = load_vehicle(pkgs1, 100)
    print(f"\n[Test Case 3] Capacity = 100 kg -> Total Value: {val3}")
