#!/usr/bin/env python3
"""
Test Case Generator - Excel Export Module
Exports generated test cases to professional Excel format with formatting and charts
"""

import xlsxwriter
from datetime import datetime
from typing import List, Dict

def export_to_excel(test_cases: List[Dict], output_file: str = "test_cases.xlsx"):
    """
    Export test cases to Excel with professional formatting
    
    Args:
        test_cases: List of test case dictionaries
        output_file: Output Excel file path
    
    Returns:
        str: Success message
    """
    
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet('Test Cases')
    
    # Define formats
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'center',
        'fg_color': '#366092',
        'border': 1,
        'font_color': 'white',
        'bg_color': '#4472C4'
    })
    
    # Priority formats
    critical_format = workbook.add_format({
        'bold': True,
        'bg_color': '#FFC7CE',
        'font_color': '#9C0006',
        'border': 1
    })
    
    high_format = workbook.add_format({
        'bold': True,
        'bg_color': '#FFEB9C',
        'font_color': '#9C6500',
        'border': 1
    })
    
    medium_format = workbook.add_format({
        'bold': True,
        'bg_color': '#FFFF00',
        'font_color': '#000000',
        'border': 1
    })
    
    low_format = workbook.add_format({
        'bold': True,
        'bg_color': '#C6EFCE',
        'font_color': '#006100',
        'border': 1
    })
    
    # Status formats
    pass_format = workbook.add_format({
        'bold': True,
        'bg_color': '#92D050',
        'font_color': '#006100',
        'border': 1
    })
    
    fail_format = workbook.add_format({
        'bold': True,
        'bg_color': '#FF0000',
        'font_color': '#FFFFFF',
        'border': 1
    })
    
    cell_format = workbook.add_format({
        'text_wrap': True,
        'valign': 'top',
        'border': 1
    })
    
    # Headers
    headers = [
        'ID', 'Module', 'Feature', 'Test Case Name', 'Description',
        'Preconditions', 'Steps', 'Expected Result', 'Priority', 'Status',
        'Assignee', 'Updated', 'Method'
    ]
    
    # Write headers
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, header_format)
        worksheet.set_column(col_num, col_num, 15)
    
    # Set specific column widths
    worksheet.set_column('A:A', 12)   # ID
    worksheet.set_column('D:D', 30)   # Name
    worksheet.set_column('E:E', 40)   # Description
    worksheet.set_column('F:F', 25)   # Preconditions
    worksheet.set_column('G:G', 50)   # Steps
    worksheet.set_column('H:H', 40)   # Expected
    
    # Write test cases
    for row_num, tc in enumerate(test_cases, start=1):
        worksheet.write(row_num, 0, tc.get('id', ''), cell_format)
        worksheet.write(row_num, 1, tc.get('module', ''), cell_format)
        worksheet.write(row_num, 2, tc.get('feature', ''), cell_format)
        worksheet.write(row_num, 3, tc.get('name', ''), cell_format)
        worksheet.write(row_num, 4, tc.get('description', ''), cell_format)
        worksheet.write(row_num, 5, tc.get('preconditions', ''), cell_format)
        worksheet.write(row_num, 6, tc.get('steps', ''), cell_format)
        worksheet.write(row_num, 7, tc.get('expected', ''), cell_format)
        worksheet.write(row_num, 8, tc.get('priority', 'Medium'), cell_format)
        worksheet.write(row_num, 9, tc.get('status', 'Not Run'), cell_format)
        worksheet.write(row_num, 10, tc.get('assignee', ''), cell_format)
        worksheet.write(row_num, 11, tc.get('updated', datetime.now().strftime('%Y-%m-%d')), cell_format)
        worksheet.write(row_num, 12, tc.get('method', ''), cell_format)
    
    # Apply conditional formatting
    worksheet.conditional_format('I2:I1000', {
        'type': 'text',
        'criteria': 'containing',
        'value': 'Critical',
        'format': critical_format
    })
    
    worksheet.conditional_format('I2:I1000', {
        'type': 'text',
        'criteria': 'containing',
        'value': 'High',
        'format': high_format
    })
    
    worksheet.conditional_format('I2:I1000', {
        'type': 'text',
        'criteria': 'containing',
        'value': 'Medium',
        'format': medium_format
    })
    
    worksheet.conditional_format('I2:I1000', {
        'type': 'text',
        'criteria': 'containing',
        'value': 'Low',
        'format': low_format
    })
    
    # Status conditional formatting
    worksheet.conditional_format('J2:J1000', {
        'type': 'text',
        'criteria': 'containing',
        'value': 'Pass',
        'format': pass_format
    })
    
    worksheet.conditional_format('J2:J1000', {
        'type': 'text',
        'criteria': 'containing',
        'value': 'Fail',
        'format': fail_format
    })
    
    # Add summary sheet
    summary_sheet = workbook.add_worksheet('Summary')
    summary_sheet.write('A1', 'Test Case Summary Report', header_format)
    summary_sheet.write('A2', f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', cell_format)
    
    summary_sheet.write('A4', 'Total Test Cases:', cell_format)
    summary_sheet.write_formula('B4', '=COUNTA(\'Test Cases\'!A:A)-1')
    
    summary_sheet.write('A5', 'Passed:', cell_format)
    summary_sheet.write_formula('B5', '=COUNTIF(\'Test Cases\'!J:J,"Pass")')
    
    summary_sheet.write('A6', 'Failed:', cell_format)
    summary_sheet.write_formula('B6', '=COUNTIF(\'Test Cases\'!J:J,"Fail")')
    
    summary_sheet.write('A7', 'Pass Rate:', cell_format)
    summary_sheet.write_formula('B7', '=IF(B4>0,B5/B4*100,0)')
    
    # Add chart
    chart = workbook.add_chart({'type': 'pie'})
    chart.add_series({
        'name': 'Test Results',
        'categories': ['Summary', 'A5', 'A6'],
        'values': ['Summary', 'B5', 'B6'],
    })
    chart.set_title({'name': 'Test Results Distribution'})
    summary_sheet.insert_chart('D4', chart)
    
    workbook.close()
    
    return f"✅ Successfully exported {len(test_cases)} test cases to {output_file}"

if __name__ == "__main__":
    # Example usage
    example_test_cases = [
        {
            'id': 'TC001',
            'module': 'Authentication',
            'feature': 'Login',
            'name': 'Valid User Login',
            'description': 'Verify user can login with valid credentials',
            'preconditions': 'User account exists',
            'steps': '1. Navigate to login\n2. Enter valid username\n3. Enter valid password\n4. Click login',
            'expected': 'User redirected to dashboard',
            'priority': 'Critical',
            'status': 'Pass',
            'assignee': 'QA Team',
            'method': 'Equivalence Partitioning'
        }
    ]
    
    print(export_to_excel(example_test_cases, 'example_test_cases.xlsx'))
