#!/usr/bin/env python3
"""Test file for comment analysis - meaningless and missing comments detection"""

import math
import random
from typing import List, Dict, Optional

# Good example with meaningful comments
def well_commented_function(data: List[Dict]) -> Dict:
    """Calculate advanced statistics with proper documentation"""
    
    # Initialize result containers for statistical analysis
    result = {
        'mean': 0,
        'median': 0,
        'std_dev': 0,
        'outliers': []
    }
    
    # Extract numeric values, filtering out invalid entries
    values = [item.get('value', 0) for item in data if isinstance(item.get('value'), (int, float))]
    
    if not values:
        return result
    
    # Calculate arithmetic mean using standard formula
    result['mean'] = sum(values) / len(values)
    
    # Calculate median using sorted array approach
    # For even-length arrays, take average of two middle elements
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 0:
        result['median'] = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
    else:
        result['median'] = sorted_values[n//2]
    
    # Calculate standard deviation using population formula
    # σ = √(Σ(x - μ)² / N)
    variance = sum((x - result['mean']) ** 2 for x in values) / len(values)
    result['std_dev'] = math.sqrt(variance)
    
    # Identify outliers using 2-sigma rule
    # Values beyond 2 standard deviations are considered outliers
    threshold = 2 * result['std_dev']
    result['outliers'] = [x for x in values if abs(x - result['mean']) > threshold]
    
    return result


# Bad example 1: Meaningless comments
def bad_meaningless_comments(arr):
    # increment i
    i = 0
    # loop through array
    for item in arr:
        # add 1 to i
        i += 1
        # check if item is greater than 5
        if item > 5:
            # print the item
            print(item)
    # return i
    return i

def another_bad_example(x, y):
    # TODO: fix this
    result = x + y  # add x and y
    return result  # return the result

# Bad example 2: Outdated comments
def outdated_comments_function(data):
    # This function calculates the sum of all positive numbers
    # Actually, it now calculates the product of all numbers
    result = 1
    for item in data:
        result *= item
    return result

# Bad example 3: Complex algorithm without comments
def complex_algorithm_no_comments(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return complex_algorithm_no_comments(left) + middle + complex_algorithm_no_comments(right)

def fibonacci_no_explanation(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b

# Bad example 4: Complex business logic without explanation
def calculate_insurance_premium(age, income, risk_factors, coverage_type, region):
    base_rate = 0.02
    if age < 25:
        age_multiplier = 1.5
    elif age < 35:
        age_multiplier = 1.2
    elif age < 50:
        age_multiplier = 1.0
    else:
        age_multiplier = 1.3
    
    if income < 30000:
        income_factor = 1.2
    elif income < 60000:
        income_factor = 1.0
    else:
        income_factor = 0.9
    
    risk_score = 1.0
    for factor in risk_factors:
        if factor == 'smoking':
            risk_score *= 1.5
        elif factor == 'high_bp':
            risk_score *= 1.3
        elif factor == 'diabetes':
            risk_score *= 1.4
    
    coverage_multiplier = {'basic': 1.0, 'standard': 1.5, 'premium': 2.0}.get(coverage_type, 1.0)
    
    regional_factor = {'urban': 1.1, 'suburban': 1.0, 'rural': 0.9}.get(region, 1.0)
    
    premium = income * base_rate * age_multiplier * income_factor * risk_score * coverage_multiplier * regional_factor
    
    if premium < income * 0.01:
        premium = income * 0.01
    elif premium > income * 0.15:
        premium = income * 0.15
    
    return round(premium, 2)

# Bad example 5: Mathematical calculations without context
def mysterious_calculation(x, y, z):
    a = x * 0.299 + y * 0.587 + z * 0.114
    b = (x - a) * 0.713 + a
    c = (z - a) * 0.527 + a
    return (a, b, c)

def another_mystery(data):
    n = len(data)
    sum_x = sum(data)
    sum_x2 = sum(x*x for x in data)
    mean = sum_x / n
    variance = (sum_x2 - sum_x * sum_x / n) / (n - 1)
    return math.sqrt(variance)

# Good example with proper comments for complex logic
def well_documented_pricing(age: int, income: float, risk_factors: List[str], 
                          coverage_type: str, region: str) -> float:
    """Calculate insurance premium based on multiple risk factors"""
    
    # Base premium rate as percentage of income (2%)
    base_rate = 0.02
    
    # Age-based risk adjustment
    # Younger drivers (under 25) and older drivers (50+) have higher risk
    if age < 25:
        age_multiplier = 1.5  # 50% increase for inexperienced drivers
    elif age < 35:
        age_multiplier = 1.2  # 20% increase for young adults
    elif age < 50:
        age_multiplier = 1.0  # Standard rate for prime age group
    else:
        age_multiplier = 1.3  # 30% increase for senior drivers
    
    # Income-based affordability adjustment
    # Lower income gets slight increase, higher income gets discount
    if income < 30000:
        income_factor = 1.2   # 20% increase for affordability concerns
    elif income < 60000:
        income_factor = 1.0   # Standard rate for middle income
    else:
        income_factor = 0.9   # 10% discount for high income
    
    # Calculate cumulative risk score from health/lifestyle factors
    risk_score = 1.0
    for factor in risk_factors:
        if factor == 'smoking':
            risk_score *= 1.5     # 50% increase for smoking
        elif factor == 'high_bp':
            risk_score *= 1.3     # 30% increase for high blood pressure
        elif factor == 'diabetes':
            risk_score *= 1.4     # 40% increase for diabetes
    
    # Coverage level multiplier
    coverage_multiplier = {
        'basic': 1.0,      # Standard rate
        'standard': 1.5,   # 50% more for additional coverage
        'premium': 2.0     # 100% more for comprehensive coverage
    }.get(coverage_type, 1.0)
    
    # Regional risk adjustment based on claim statistics
    regional_factor = {
        'urban': 1.1,      # 10% increase for higher urban accident rates
        'suburban': 1.0,   # Standard rate
        'rural': 0.9       # 10% decrease for lower rural accident rates
    }.get(region, 1.0)
    
    # Calculate final premium using all factors
    premium = (income * base_rate * age_multiplier * income_factor * 
              risk_score * coverage_multiplier * regional_factor)
    
    # Apply premium bounds to ensure affordability and minimum coverage
    min_premium = income * 0.01  # Minimum 1% of income
    max_premium = income * 0.15  # Maximum 15% of income
    
    if premium < min_premium:
        premium = min_premium
    elif premium > max_premium:
        premium = max_premium
    
    return round(premium, 2)


if __name__ == "__main__":
    # Test the functions
    print("Testing comment analysis...")
    
    # Test data
    test_data = [
        {'value': 10}, {'value': 20}, {'value': 30}, {'value': 40}, {'value': 50}
    ]
    
    # Test well-commented function
    stats = well_commented_function(test_data)
    print(f"Statistics: {stats}")
    
    # Test bad functions
    result1 = bad_meaningless_comments([1, 6, 3, 8, 2])
    print(f"Bad function result: {result1}")
    
    # Test complex algorithms
    sorted_arr = complex_algorithm_no_comments([64, 34, 25, 12, 22, 11, 90])
    print(f"Sorted array: {sorted_arr}")
    
    fib_result = fibonacci_no_explanation(10)
    print(f"Fibonacci result: {fib_result}")
    
    # Test pricing functions
    premium1 = calculate_insurance_premium(30, 50000, ['smoking'], 'standard', 'urban')
    premium2 = well_documented_pricing(30, 50000, ['smoking'], 'standard', 'urban')
    print(f"Premium comparison: {premium1} vs {premium2}")