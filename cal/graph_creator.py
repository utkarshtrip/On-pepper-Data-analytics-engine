import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import plotly.express as px
import plotly.io as pio
import base64
import plotly.graph_objs as go
import plotly.offline as opy
import operator 
import numpy as np
import pandas as pd


def apply_operations(new_df, expression_list):
    # Create a dictionary mapping the operator symbols to their corresponding functions
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    def solve_short_expression(new_df, sub_expression):

        while '*' in sub_expression or '/' in sub_expression:
            for cur_op in ['*', '/']:
                i = 0
                while cur_op in sub_expression:
                    index = sub_expression.index(cur_op)
                    left_operand = sub_expression[index - 1]
                    right_operand = sub_expression[index + 1]
                    new_df['result' + cur_op + str(i)] = operators[cur_op](new_df[left_operand], new_df[right_operand])
                    sub_expression = (
                            sub_expression[:index - 1] + ['result' + cur_op + str(i)] + sub_expression[index + 2:]
                    )

        # Perform evaluation of +, - operations last
        while '+' in sub_expression or '-' in sub_expression:
            for op in ['+', '-']:
                i = 0
                while op in sub_expression:
                    index = sub_expression.index(op)
                    left_operand = sub_expression[index - 1]
                    right_operand = sub_expression[index + 1]
                    new_df['result' + op + str(i)] = operators[op](new_df[left_operand], new_df[right_operand])
                    sub_expression = (
                            sub_expression[:index - 1] + ['result' + op + str(i)] + sub_expression[index + 2:]
                    )
                    i += 1

        return new_df[sub_expression[0]]

    def evaluate_bodmas(new_df, expression_list):
        # Perform evaluation of brackets first
        count = 0
        while ')' in expression_list:

            end = expression_list.index(')')
            start = end - 1
            while start >= 0:
                if expression_list[start] == '(':
                    break
                else:
                    start = start - 1

            # end = expression_list.index(')', start)
            sub_expr = expression_list[start + 1: end]
            new_df['result' + str(count)] = solve_short_expression(new_df, sub_expr)

            expression_list = expression_list[:start] + ['result' + str(count)] + expression_list[end + 1:]
            count += 1

        # Perform evaluation of *, / operations next
        while '*' in expression_list or '/' in expression_list:
            for op in ['*', '/']:
                i = 0
                while op in expression_list:
                    index = expression_list.index(op)
                    left_operand = expression_list[index - 1]
                    right_operand = expression_list[index + 1]
                    new_df['result' + op + str(i)] = operators[op](new_df[left_operand], new_df[right_operand])
                    expression_list = (
                            expression_list[:index - 1] + ['result' + op + str(i)] + expression_list[index + 2:]
                    )
                    i += 1

        # Perform evaluation of +, - operations last
        while '+' in expression_list or '-' in expression_list:
            for op in ['+', '-']:
                i = 0
                while op in expression_list:

                    index = expression_list.index(op)
                    left_operand = expression_list[index - 1]
                    right_operand = expression_list[index + 1]
                    new_df['result' + op + str(i)] = operators[op](new_df[left_operand], new_df[right_operand])
                    expression_list = (
                            expression_list[:index - 1] + ['result' + op + str(i)] + expression_list[index + 2:]
                    )

        return new_df[expression_list[0]]
    # Evaluate the expression list following the BODMAS rule
    result = evaluate_bodmas(new_df, expression_list)
    return result

def return_newColumn_df(df):
      global copy_col
      return pd.concat([df, copy_col], axis=1)

def modified_result(df, expression_list, expression_string):
    # Create a modified dataframe
    modified_df = df
    modified_df[expression_string]=apply_operations(modified_df,expression_list)
    global copy_col
    copy_col=pd.DataFrame()
    copy_col =  modified_df[[expression_string]]
    print("I am in modified_result function")
    modified_df['Period'] = modified_df['Period'].astype('datetime64[ns]')   
    print(modified_df.columns)
    fig = go.Figure()   
    column_list=['Revenue','Sales_quantity','Average_cost','The_average_annual_payroll_of_the_region']
    fig = px.line(modified_df, x = 'Period', y = ['expression_string']+column_list)
    # fig = px.line(modified_df, x = 'Period', y = modified_df.columns[1:])
    # fig.add_trace(go.Scatter(x=modified_df[modified_df.columns.tolist()[0]], y=modified_df['new_column'], mode='lines'))
    fig.update_layout(title=expression_string, title_y=0.9, title_x=0.5, title_yanchor='top')
    plot_div = opy.plot(fig, auto_open=False, output_type='div')
    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                    label="1m",
                    step="month",
                    stepmode="backward"),
                dict(count=6,
                    label="6m",
                    step="month",
                    stepmode="backward"),
                dict(count=1,
                    label="YTD",
                    step="year",
                    stepmode="todate"),
                dict(count=1,
                    label="1y",
                    step="year",
                    stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
        )
    )

    # fig.update_layout(title=expression_string, title_y=0.9, title_x=0.5, title_yanchor='top')
    # fig = px.line(modified_df, x = modified_df.columns[0], y = ['new_column'])
    plot_div = opy.plot(fig, auto_open=True,include_plotlyjs = True, output_type='div')

    # fig = go.Figure()
    
    # fig.add_trace(go.Scatter(x=modified_df[modified_df.columns.tolist()[0]], y=modified_df['new_column'], mode='lines'))
    # # fig.update_layout(title=expression_string, title_y=0.9, title_x=0.5, title_yanchor='top',xaxis=dict(tickangle=45))
    # fig.update_layout(title=expression_string, title_y=0.9, title_x=0.5, title_yanchor='top')
    # plot_div = opy.plot(fig, auto_open=False, output_type='div')
    return plot_div
