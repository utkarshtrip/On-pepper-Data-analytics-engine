import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .xbrl_parser import parse_xbrl
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .graph_creator import modified_result

expression_list = []

def xbrl_table(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            # Read the uploaded file and pass it to the parse_xbrl function
            global df 
            # df = parse_xbrl(file)
            df= pd.read_csv(file)
            # Handle expression evaluation
            expression = request.POST.get('expression', '')
            if expression:
                try:
                    df['Result'] = eval(expression, {'df': df})
                    expression_list.append(expression)
                except Exception as e:
                    error_message = str(e)
                    context = {'error_message': error_message}
                    return render(request, 'error.html', context)

            context = {'data': df.to_dict('records'), 'expressions': expression_list}
            return render(request, 'xbrl_table.html', context)
        else:
            error_message = 'No file was selected.'
            context = {'error_message': error_message}
            return render(request, 'error.html', context)
    else:
        return render(request, 'xbrl_table.html')


def submit_expression(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        expression_list = data.get('expressionList')
        expression_list = expression_list.replace("\n", "")
        expression_list = expression_list.split()
        expression_string =data.get('expressionName')

        global df

        plot_html = modified_result(df, expression_list, expression_string)
        # Render the HTML page with the graph
        return JsonResponse({'plot_html': plot_html,})

    return JsonResponse({'status': 'error'})

def save_expression_column(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        save_expression = data.get('saveExpression')

        if save_expression:
            # Perform action when saveExpression is True
            # For example, update the global df and add an expression column
            global df
            df['expression_name'] = modified_result(df, expression_list, expression_string)
            return JsonResponse({'message': 'Expression column saved.'})

        # Perform action when saveExpression is False or not provided
        # For example, do something else or provide a different response
        return JsonResponse({'message': 'No action taken.'})

    # Handle other request methods if needed
    return JsonResponse({'message': 'Invalid request method.'})