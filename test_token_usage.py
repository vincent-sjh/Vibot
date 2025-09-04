#!/usr/bin/env python3
"""Test token usage tracking functionality"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vibot.commands.ustalony import TokenUsageTracker

# Test the token usage tracker
def test_token_tracker():
    tracker = TokenUsageTracker()
    tracker.start_tracking("deepseek-v3")
    
    # Simulate some usage data
    class MockUsage:
        def __init__(self, prompt_tokens, completion_tokens, total_tokens):
            self.prompt_tokens = prompt_tokens
            self.completion_tokens = completion_tokens
            self.total_tokens = total_tokens
    
    # Add some mock usage
    tracker.add_usage(MockUsage(1500, 300, 1800))
    tracker.add_usage(MockUsage(2000, 400, 2400))
    tracker.add_usage(MockUsage(1116, 355, 1471))
    
    # Print summary
    tracker.print_summary()

if __name__ == "__main__":
    test_token_tracker()