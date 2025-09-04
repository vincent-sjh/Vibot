#!/usr/bin/env python3
"""Test file for function quality analysis"""

def good_function(x, y):
    """A well-designed function"""
    return x + y

def long_function_with_many_lines():
    """This function is intentionally long to test the analyzer"""
    result = 0
    for i in range(100):
        if i % 2 == 0:
            result += i
        else:
            result -= i
        
        if i % 10 == 0:
            print(f"Processing {i}")
            
        if i % 20 == 0:
            result *= 2
            
        if i % 30 == 0:
            result //= 3
            
        if i % 40 == 0:
            result += 100
            
        if i % 50 == 0:
            result -= 50
            
        # More unnecessary lines to make it long
        temp_var = i * 2
        temp_var += 10
        temp_var -= 5
        temp_var *= 3
        temp_var //= 2
        
        another_var = temp_var + result
        another_var *= 2
        another_var -= 100
        
        if another_var > 1000:
            another_var = 1000
        elif another_var < -1000:
            another_var = -1000
            
        result += another_var
        
        # Even more lines
        for j in range(5):
            if j % 2 == 0:
                result += j
            else:
                result -= j
                
        # And more...
        try:
            division_result = result / (i + 1)
            result = int(division_result)
        except ZeroDivisionError:
            result = 0
            
        # Keep adding lines...
        if result > 10000:
            result = 10000
        elif result < -10000:
            result = -10000
            
    return result

def function_with_many_parameters(param1, param2, param3, param4, param5, param6, param7, param8, *args, **kwargs):
    """Function with too many parameters"""
    return param1 + param2 + param3 + param4 + param5 + param6 + param7 + param8

def complex_function(data):
    """Function with high cyclomatic complexity"""
    result = 0
    
    if data is None:
        return None
        
    if isinstance(data, list):
        for item in data:
            if isinstance(item, int):
                if item > 0:
                    if item % 2 == 0:
                        result += item * 2
                    else:
                        result += item
                elif item < 0:
                    if item % 2 == 0:
                        result -= item
                    else:
                        result -= item * 2
                else:
                    result += 1
            elif isinstance(item, str):
                if len(item) > 5:
                    result += len(item)
                else:
                    result -= len(item)
            elif isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, int):
                        result += value
                    elif isinstance(value, str):
                        result += len(value)
    elif isinstance(data, dict):
        for key, value in data.items():
            if key.startswith('test'):
                if isinstance(value, int):
                    result += value * 3
                elif isinstance(value, str):
                    result += len(value) * 2
            else:
                if isinstance(value, int):
                    result += value
                elif isinstance(value, str):
                    result += len(value)
                    
    return result

async def async_function_with_issues(a, b, c, d, e, f, g):
    """Async function with multiple issues"""
    result = 0
    
    # Long and complex logic
    for i in range(100):
        if i % 2 == 0:
            if a > b:
                if c > d:
                    result += i * a
                else:
                    result += i * b
            else:
                if e > f:
                    result += i * c
                else:
                    result += i * d
        else:
            if g > 0:
                if a + b > c + d:
                    result -= i
                else:
                    result += i
            else:
                result *= 2
                
        # More complexity
        try:
            if result > 1000:
                result //= 2
            elif result < -1000:
                result *= -1
        except Exception:
            result = 0
            
        # Even more lines and complexity
        temp = result
        for j in range(10):
            if j % 3 == 0:
                temp += j
            elif j % 3 == 1:
                temp -= j
            else:
                temp *= j if j > 0 else 1
                
        result = temp
        
    return result

class TestClass:
    def method_with_issues(self, p1, p2, p3, p4, p5, p6):
        """Method with too many parameters"""
        # Long method
        result = p1 + p2 + p3 + p4 + p5 + p6
        
        for i in range(50):
            if i % 2 == 0:
                result += i
            else:
                result -= i
                
            if i % 3 == 0:
                result *= 2
            elif i % 3 == 1:
                result //= 2
            else:
                result += 10
                
            # More lines to make it long
            temp = result * i
            temp += 100
            temp -= 50
            temp *= 3
            temp //= 4
            
            result += temp
            
            if result > 10000:
                result = 10000
            elif result < -10000:
                result = -10000
                
        return result