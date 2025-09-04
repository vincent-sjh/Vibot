#!/usr/bin/env python3
"""Test file for readability analysis - comments and line spacing detection"""

import math
import random
from typing import List, Dict, Optional

# Good example with proper comments and spacing
def well_documented_function(data: List[Dict]) -> Dict:
    """Calculate statistics with proper documentation and spacing"""
    
    # Initialize result containers
    result = {
        'mean': 0,
        'median': 0,
        'std_dev': 0,
        'outliers': []
    }
    
    # Extract numeric values from data
    values = [item.get('value', 0) for item in data if isinstance(item.get('value'), (int, float))]
    
    if not values:
        return result
    
    # Calculate mean (average)
    result['mean'] = sum(values) / len(values)
    
    # Calculate median (middle value)
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 0:
        result['median'] = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
    else:
        result['median'] = sorted_values[n//2]
    
    # Calculate standard deviation
    variance = sum((x - result['mean']) ** 2 for x in values) / len(values)
    result['std_dev'] = math.sqrt(variance)
    
    # Identify outliers (values beyond 2 standard deviations)
    threshold = 2 * result['std_dev']
    result['outliers'] = [x for x in values if abs(x - result['mean']) > threshold]
    
    return result


# Bad example 1: Missing comments for complex algorithm
def bad_complex_algorithm(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
def another_bad_function(data):
    result = []
    temp = {}
    for item in data:
        key = item['category']
        if key not in temp:
            temp[key] = []
        temp[key].append(item['value'])
    for category, values in temp.items():
        avg = sum(values) / len(values)
        result.append({'category': category, 'average': avg})
    return result
def third_function_no_spacing(x, y):
    return x * y + x / y - x ** y

# Bad example 2: Dense code without line separation
class BadDataProcessor:
    def __init__(self, config):
        self.config = config
        self.data = []
        self.results = {}
        self.errors = []
    def process_item(self, item):
        if not self.validate_item(item):
            self.errors.append(f"Invalid item: {item}")
            return None
        processed = self.transform_item(item)
        self.data.append(processed)
        return processed
    def validate_item(self, item):
        return isinstance(item, dict) and 'id' in item and 'value' in item
    def transform_item(self, item):
        multiplier = self.config.get('multiplier', 1)
        offset = self.config.get('offset', 0)
        return {
            'id': item['id'],
            'original_value': item['value'],
            'processed_value': item['value'] * multiplier + offset,
            'timestamp': item.get('timestamp', 'unknown')
        }

# Bad example 3: Complex business logic without comments
def calculate_pricing(base_price, customer_type, quantity, season, region):
    if customer_type == 'premium':
        discount = 0.15
    elif customer_type == 'standard':
        discount = 0.05
    else:
        discount = 0
    
    if quantity > 100:
        bulk_discount = 0.1
    elif quantity > 50:
        bulk_discount = 0.05
    else:
        bulk_discount = 0
    
    seasonal_multiplier = 1.0
    if season == 'winter':
        seasonal_multiplier = 1.2
    elif season == 'summer':
        seasonal_multiplier = 0.9
    
    regional_adjustment = 1.0
    if region == 'north':
        regional_adjustment = 1.1
    elif region == 'south':
        regional_adjustment = 0.95
    
    final_price = base_price * (1 - discount) * (1 - bulk_discount) * seasonal_multiplier * regional_adjustment
    
    if final_price < base_price * 0.3:
        final_price = base_price * 0.3
    
    return round(final_price, 2)

# Bad example 4: Mathematical algorithm without explanation
def mystery_algorithm(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b

def another_mystery(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return another_mystery(left) + middle + another_mystery(right)

# Good example with proper spacing and comments
class GoodDataProcessor:
    """A well-structured data processor with proper spacing and documentation"""
    
    def __init__(self, config: Dict):
        """Initialize the processor with configuration"""
        self.config = config
        self.data = []
        self.results = {}
        self.errors = []
    
    def process_item(self, item: Dict) -> Optional[Dict]:
        """Process a single data item with validation and transformation"""
        
        # Validate the input item
        if not self.validate_item(item):
            self.errors.append(f"Invalid item: {item}")
            return None
        
        # Transform the item according to configuration
        processed = self.transform_item(item)
        self.data.append(processed)
        
        return processed
    
    def validate_item(self, item: Dict) -> bool:
        """Validate that an item has required fields"""
        return isinstance(item, dict) and 'id' in item and 'value' in item
    
    def transform_item(self, item: Dict) -> Dict:
        """Transform an item using configured multiplier and offset"""
        
        # Get transformation parameters from config
        multiplier = self.config.get('multiplier', 1)
        offset = self.config.get('offset', 0)
        
        # Apply transformation
        return {
            'id': item['id'],
            'original_value': item['value'],
            'processed_value': item['value'] * multiplier + offset,
            'timestamp': item.get('timestamp', 'unknown')
        }


if __name__ == "__main__":
    # Test the functions
    print("Testing readability analysis...")
    
    # Test data
    test_data = [
        {'value': 10}, {'value': 20}, {'value': 30}, {'value': 40}, {'value': 50}
    ]
    
    # Test good function
    stats = well_documented_function(test_data)
    print(f"Statistics: {stats}")
    
    # Test bad functions
    sorted_arr = bad_complex_algorithm([64, 34, 25, 12, 22, 11, 90])
    print(f"Sorted array: {sorted_arr}")
    
    # Test pricing calculation
    price = calculate_pricing(100, 'premium', 75, 'winter', 'north')
    print(f"Final price: ${price}")