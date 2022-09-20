import pandas as pd

# read file and save to another with sorted values
df = pd.read_excel('employees.xlsx')

# sort values
sorted_emp = df.sort_values(by='Years of Experience', ascending=False, axis=0, ignore_index=True)

# work with new sorted file
writer = pd.ExcelWriter('employees_sorted.xlsx', engine='xlsxwriter', datetime_format='YYYY-MM-DD')
sorted_emp.to_excel(writer, sheet_name='Employees Sorted', index=False)
workbook = writer.book
worksheet = writer.sheets['Employees Sorted']

# format rows
color_format_greater_than_20 = workbook.add_format({"bg_color": "FFA32D"})
color_format_equal_or_less_20 = workbook.add_format({"bg_color": "FFC984"})
color_format_equal_or_less_10 = workbook.add_format({"bg_color": "FFE8CB"})
border_top = workbook.add_format({"top": 2})
worksheet.conditional_format('A26:D26', {'type': 'no_errors',                                    
                                       'format': border_top})
worksheet.conditional_format('A2:D25', {'type': 'formula',
                                        'criteria': '=$B2<=10',
                                        'format': color_format_equal_or_less_10})                                       
worksheet.conditional_format('A2:D25', {'type': 'formula',
                                        'criteria': '=$B2<=20',
                                        'format': color_format_equal_or_less_20})                                        
worksheet.conditional_format('A2:D25', {'type': 'formula',
                                        'criteria': '=$B2>20',
                                        'format': color_format_greater_than_20})                                                                           
                                                                                                                                                  
# format columns
allign_format = workbook.add_format({"valign": "vcenter", "align": "center"})
worksheet.set_column('A:B', 22, allign_format)
worksheet.set_column('C:C', 25, allign_format)
worksheet.set_column('D:D', 12)    

# add chart
chart = workbook.add_chart({'type': 'bar'})
chart.set_legend({'none': True})
chart.add_series({
                'name': 'Years of expirience',
                'categories': "='Employees Sorted'!$A$2:$A$25",
                'values': "='Employees Sorted'!$B$2:$B$25",
                'data_labels': {'value': True}
                })
chart.set_x_axis({'major_gridlines': {'visible': False }})
chart.set_style(18)
worksheet.insert_chart('F2', chart, {'x_scale': 1.2, 'y_scale': 2})

# format headers
header_format = workbook.add_format({
        "valign": "vcenter",
        "align": "center",
        "bg_color": "#951F06",
        "bold": True,
        'font_color': '#FFFFFF',
        "top": 2 
    })

# write the column headers with the defined format
for col_num, value in enumerate(df.columns.values):
    worksheet.write(0, col_num, value, header_format)

# save to file
writer.save() 

   

