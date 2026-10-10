#!/usr/bin/env python3
"""
Test Case Generator - XMind Export Module
Exports generated test cases to XMind mind map format for visual test case organization
"""

import xmind
from xmind.core.markerref import MarkerId
from typing import List, Dict

def export_to_xmind(test_cases: List[Dict], output_file: str = "test_cases.xmind"):
    """
    Export test cases to XMind mind map format
    
    Args:
        test_cases: List of test case dictionaries
        output_file: Output XMind file path
    
    Returns:
        str: Success message
    """
    
    try:
        workbook = xmind.load(output_file)
        sheet = workbook.getPrimarySheet()
        sheet.setTitle("Test Suite")
        
        root = sheet.getRootTopic()
        root.setTitle("Test Cases")
        root.addMarker(MarkerId.starBlue)
        
        modules = {}
        for tc in test_cases:
            module = tc.get('module', 'General')
            if module not in modules:
                modules[module] = []
            modules[module].append(tc)
        
        for module_name, module_tests in modules.items():
            module_topic = root.addSubTopic()
            module_topic.setTitle(module_name)
            module_topic.addMarker(MarkerId.starGreen)
            
            features = {}
            for tc in module_tests:
                feature = tc.get('feature', module_name)
                key = f"{module_name}_{feature}"
                if key not in features:
                    features[key] = []
                features[key].append(tc)
            
            for feature_key, feature_tests in features.items():
                feature_name = feature_key.split('_', 1)[1]
                feature_topic = module_topic.addSubTopic()
                feature_topic.setTitle(feature_name)
                
                for tc in feature_tests:
                    test_topic = feature_topic.addSubTopic()
                    test_topic.setTitle(f"{tc.get('id', 'TC')}: {tc.get('name', 'Unnamed')}")
                    
                    notes = f"""
ID: {tc.get('id', 'N/A')}
Priority: {tc.get('priority', 'Medium')}
Status: {tc.get('status', 'Not Run')}

Description:
{tc.get('description', 'No description')}

Steps:
{tc.get('steps', 'No steps defined')}

Expected Result:
{tc.get('expected', 'No expected result defined')}
"""
                    test_topic.setPlainNotes(notes)
                    
                    priority = tc.get('priority', 'Medium')
                    if priority == 'Critical':
                        test_topic.addMarker("priority-1")
                    elif priority == 'High':
                        test_topic.addMarker("priority-2")
                    elif priority == 'Medium':
                        test_topic.addMarker("priority-3")
                    else:
                        test_topic.addMarker("priority-4")
                    
                    status = tc.get('status', 'Not Run')
                    if status == 'Pass':
                        test_topic.addMarker(MarkerId.flagGreen)
                    elif status == 'Fail':
                        test_topic.addMarker(MarkerId.flagRed)
                    elif status == 'In Progress':
                        test_topic.addMarker(MarkerId.flagYellow)
        
        xmind.save(workbook)
        
        return f"✅ Successfully exported {len(test_cases)} test cases to {output_file}"
    
    except Exception as e:
        return f"❌ Error exporting to XMind: {str(e)}"

if __name__ == "__main__":
    # Example usage
    test_cases = [
        {
            'id': 'TC001',
            'module': 'Authentication',
            'feature': 'Login',
            'name': 'Valid Login',
            'description': 'Test user login with valid credentials',
            'steps': '1. Navigate to login\n2. Enter username\n3. Enter password\n4. Click login',
            'expected': 'User logged in successfully',
            'priority': 'Critical',
            'status': 'Not Run'
        },
        {
            'id': 'TC002',
            'module': 'Authentication',
            'feature': 'Login',
            'name': 'Invalid Password',
            'description': 'Test login with invalid password',
            'steps': '1. Navigate to login\n2. Enter username\n3. Enter wrong password\n4. Click login',
            'expected': 'Error message displayed',
            'priority': 'High',
            'status': 'Pass'
        }
    ]
    
    result = export_to_xmind(test_cases, "example_test_cases.xmind")
    print(result)
