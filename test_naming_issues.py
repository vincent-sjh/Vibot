#!/usr/bin/env python3
"""Test file for naming convention analysis functionality"""

# Oversimplified names
def process_data(a, b, c):
    """Function with oversimplified parameter names"""
    x = a + b
    y = c * 2
    z = x / y
    return z

# Obscure abbreviations
def calcTotPrc(qty, prc, disc):
    """Calculate total price with obscure abbreviations"""
    totPrc = qty * prc
    discAmt = totPrc * disc
    finPrc = totPrc - discAmt
    return finPrc

# Inconsistent naming style (mixing snake_case and camelCase)
def calculate_user_score(user_data):
    totalScore = 0  # camelCase
    bonus_points = 10  # snake_case
    userLevel = user_data.get('level')  # camelCase
    experience_points = user_data.get('exp')  # snake_case
    
    if userLevel > 5:
        totalScore += bonus_points
    
    return totalScore + experience_points

# Meaningless names
def process_stuff(data, temp, foo):
    """Function with meaningless parameter names"""
    result = []
    thing = data.copy()
    
    for item in thing:
        bar = temp * 2
        if foo:
            stuff = item + bar
            result.append(stuff)
    
    return result

# Poor constant naming (should be UPPER_CASE)
max_retries = 5
default_timeout = 30
api_base_url = "https://api.example.com"

# Poor class naming
class myclass:
    """Class with poor naming"""
    def __init__(self):
        self.data = {}
        self.temp = None
        self.foo = False

class handler:
    """Generic handler class name"""
    def process(self, stuff):
        return stuff

class manager:
    """Generic manager class name"""
    def __init__(self):
        self.items = []

# More oversimplified names in loops
def complex_calculation():
    """Function with oversimplified loop variables in complex context"""
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    result = []
    
    # Using i, j in complex nested loops where more descriptive names would help
    for i in range(len(matrix)):
        row_result = []
        for j in range(len(matrix[i])):
            # Complex calculation where i, j meaning is not obvious
            value = matrix[i][j] * i + j
            if i % 2 == 0:
                value += matrix[j][i] if j < len(matrix) else 0
            row_result.append(value)
        result.append(row_result)
    
    return result

# Poor function naming (non-verb for action)
def user_data(user_id):
    """Function name should be a verb since it performs an action"""
    # This function actually fetches user data, so should be named fetch_user_data or get_user_data
    return {"id": user_id, "name": "John", "email": "john@example.com"}

def calculation(x, y):
    """Generic function name that doesn't describe what it calculates"""
    return x * y + (x / y)

# Variable scope issues
def long_running_process():
    """Function with inappropriate variable names for their scope"""
    # Short name for long-lived variable
    d = {}  # This dictionary is used throughout the function
    
    # Long name for short-lived variable
    temporary_counter_for_simple_loop = 0
    
    for item in range(100):
        very_long_descriptive_name_for_simple_index = item
        d[very_long_descriptive_name_for_simple_index] = temporary_counter_for_simple_loop
        temporary_counter_for_simple_loop += 1
    
    return d

# Mixed abbreviation patterns
def getUserInfo(userId):
    """Inconsistent abbreviation - userId vs userInfo"""
    userDetails = fetch_user_details(userId)
    userStats = get_user_statistics(userId)
    return {"info": userDetails, "stats": userStats}

def fetch_user_details(user_id):
    """Different abbreviation pattern for same concept"""
    return {"name": "John", "age": 30}

def get_user_statistics(uid):
    """Yet another abbreviation pattern"""
    return {"login_count": 10, "last_login": "2024-01-01"}

# Magic numbers without named constants
def configure_system():
    """Function with magic numbers that should be named constants"""
    timeout = 300  # Should be TIMEOUT_SECONDS or similar
    max_connections = 100  # Should be MAX_CONNECTIONS
    retry_count = 3  # Should be MAX_RETRY_COUNT
    
    return {
        "timeout": timeout,
        "max_conn": max_connections,
        "retries": retry_count
    }

# Non-descriptive class names
class Data:
    """Overly generic class name"""
    def __init__(self):
        self.info = {}

class Utils:
    """Generic utility class name without specific purpose"""
    @staticmethod
    def helper(x):
        return x * 2

# Poor method naming in class
class UserProcessor:
    def __init__(self):
        self.users = []
    
    def user(self, user_id):  # Should be get_user or find_user
        """Method name should indicate action"""
        for u in self.users:
            if u.id == user_id:
                return u
        return None
    
    def data(self):  # Should be get_data or fetch_data
        """Method name doesn't indicate what it does"""
        return len(self.users)

# Misleading names
def is_valid_email(email_string):
    """Function that doesn't actually validate email properly"""
    # This function name suggests thorough email validation
    # but it only checks for @ symbol - misleading!
    return "@" in email_string

def save_to_database(data):
    """Function name suggests database operation but actually saves to file"""
    # Misleading - actually saves to file, not database
    with open("data.txt", "w") as f:
        f.write(str(data))