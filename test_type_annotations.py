#!/usr/bin/env python3
"""Test file for type annotation detection in function quality analysis"""

# Good examples with proper type annotations
def good_function_with_types(name: str, age: int, active: bool = True) -> str:
    """A well-typed function with proper annotations"""
    return f"{name} is {age} years old and {'active' if active else 'inactive'}"

def calculate_total(items: list[dict], tax_rate: float = 0.1) -> float:
    """Calculate total with tax"""
    subtotal = sum(item.get('price', 0) for item in items)
    return subtotal * (1 + tax_rate)

# Bad examples missing type annotations
def bad_function_no_types(name, age, active=True):
    """Function without any type annotations"""
    return f"{name} is {age} years old and {'active' if active else 'inactive'}"

def process_data(data, config, options=None):
    """Function with multiple parameters but no type hints"""
    if options is None:
        options = {}
    
    result = []
    for item in data:
        if item.get('status') == config.get('required_status'):
            processed = {
                'id': item['id'],
                'value': item['value'] * config.get('multiplier', 1),
                'processed': True
            }
            result.append(processed)
    
    return result

# Mixed examples - some annotations missing
def partially_typed_function(name: str, age, active: bool = True):
    """Function with some type annotations missing"""
    return f"{name} is {age} years old"

def missing_return_type(x: int, y: int):
    """Function with parameter types but missing return type"""
    return x + y

# Long function without type annotations (multiple issues)
def long_function_no_types(data, config, options, filters, transformers, validators, processors):
    """Very long function with many parameters and no type annotations"""
    # This function is intentionally long to trigger multiple issues
    
    # Validation phase
    if not data:
        return None
    
    if not config:
        config = {}
    
    if not options:
        options = {}
    
    if not filters:
        filters = []
    
    if not transformers:
        transformers = []
    
    if not validators:
        validators = []
    
    if not processors:
        processors = []
    
    # Processing phase
    results = []
    errors = []
    
    for item in data:
        try:
            # Apply filters
            skip_item = False
            for filter_func in filters:
                if not filter_func(item):
                    skip_item = True
                    break
            
            if skip_item:
                continue
            
            # Apply transformers
            transformed_item = item.copy()
            for transformer in transformers:
                transformed_item = transformer(transformed_item)
            
            # Apply validators
            validation_errors = []
            for validator in validators:
                validation_result = validator(transformed_item)
                if not validation_result.get('valid', True):
                    validation_errors.append(validation_result.get('error', 'Unknown validation error'))
            
            if validation_errors:
                errors.extend(validation_errors)
                continue
            
            # Apply processors
            processed_item = transformed_item.copy()
            for processor in processors:
                processed_item = processor(processed_item, config, options)
            
            results.append(processed_item)
            
        except Exception as e:
            errors.append(f"Error processing item {item.get('id', 'unknown')}: {str(e)}")
    
    # Final result compilation
    final_result = {
        'results': results,
        'errors': errors,
        'total_processed': len(results),
        'total_errors': len(errors),
        'success_rate': len(results) / (len(results) + len(errors)) if (len(results) + len(errors)) > 0 else 0
    }
    
    return final_result

# TypeScript-style function (for testing multi-language support)
"""
function processUserData(userData, config, options) {
    // Missing type annotations in TypeScript
    const result = {
        id: userData.id,
        name: userData.name,
        processed: true
    };
    return result;
}

function wellTypedFunction(userData: UserData, config: Config, options?: Options): ProcessedData {
    // Good TypeScript function with proper types
    const result: ProcessedData = {
        id: userData.id,
        name: userData.name,
        processed: true
    };
    return result;
}
"""

# Java-style function (for testing multi-language support)
"""
public class DataProcessor {
    // Missing return type and parameter types
    public processData(data, config) {
        return data.stream()
            .filter(item -> item.isValid())
            .collect(Collectors.toList());
    }
    
    // Good Java method with proper types
    public List<ProcessedData> processDataWithTypes(List<RawData> data, ProcessingConfig config) {
        return data.stream()
            .filter(item -> item.isValid())
            .map(item -> processItem(item, config))
            .collect(Collectors.toList());
    }
}
"""

if __name__ == "__main__":
    # Test the functions
    print("Testing type annotation detection...")
    
    # Test good function
    result1 = good_function_with_types("Alice", 30, True)
    print(f"Good function result: {result1}")
    
    # Test bad function
    result2 = bad_function_no_types("Bob", 25, False)
    print(f"Bad function result: {result2}")
    
    # Test mixed function
    result3 = partially_typed_function("Charlie", 35, True)
    print(f"Mixed function result: {result3}")