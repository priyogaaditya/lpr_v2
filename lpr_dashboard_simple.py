import numpy as np 
import pandas as pd 
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import base64
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import re
import plotly.express as px
from plotly.offline import plot
from flask import Flask


class DBconfig:
    user = 'techbros'
    host = 'lprcowtowndb.czdbdrdlwnvw.us-east-1.rds.amazonaws.com'
    pwd = 'techbros123'
    db_name = 'lpr_database'
    port = int(3306)
    region='us-east-1'

def define_ganjil_genap(license_plate):
    number = re.findall('[0-9]', license_plate)
    if(license_plate!="UNKNOWN"):
        if int(number[-1]) % 2 == 0:
            return 'GENAP'
        if int(number[-1]) % 2 == 1:
            return 'GANJIL'
    return ''
    
# origin_map = {
#     'ABC': 'Jakarta Selatan',
#     'CDE': 'Jakarta Barat',
#     'EFG': 'Jakarta Timur',
#     'GHI': 'Jakarta Utara',
#     'IJK': 'Jakarta Pusat'
# }

# def get_origin_license(license):
#     license = license.replace(' ', '')
#     license = license.upper()
#     filter_license = re.findall(r'[0-9]+[\w]+', license)[0]
#     filter_license = re.findall(r'[a-zA-Z]+', filter_license)[0]
#     try:
#         origin_area = origin_map[filter_license]
#     except:
#         origin_area = 'UNKNOWN'
#     return origin_area

layout_jumlah_tipe_kendaraan = html.Div([
    html.Div([
        html.H2('Select Year:', style = {'font-size': '15px'}),
        dcc.Input(id="vehicle_type_year",
                placeholder='Enter selected year...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Starting Month:', style = {'font-size': '15px'}),
        dcc.Input(id="vehicle_type_month_start",
                placeholder='Enter starting month...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Stop Month:', style = {'font-size': '15px'}),
        dcc.Input(id="vehicle_type_month_stop",
                placeholder='Enter stop month...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Starting Date:', style = {'font-size': '15px'}),
        dcc.Input(id="vehicle_type_date_start",
                placeholder='Enter starting date...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Stop Date:', style = {'font-size': '15px'}),
        dcc.Input(id="vehicle_type_date_stop",
                placeholder='Enter stop date...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Starting Hour:', style = {'font-size': '15px'}),
        dcc.Input(id="vehicle_type_hour_start",
                placeholder='Enter starting date...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Stop Hour:', style = {'font-size': '15px'}),
        dcc.Input(id="vehicle_type_hour_stop",
                placeholder='Enter stop date...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    dcc.Store(id = 'vehicle_type_store_inputs'),
    html.Button('Submit', id='vehicle_type_submit_button', n_clicks=0, disabled=False, 
                style = {'font-size': '15px',
                'cursor': 'pointer',
                'text-align': 'center',
                'color': 'black',
                }),
    html.Div([
        dcc.Dropdown(
            id='vehicle-type-dropdown',
            options=[
                {'label': 'Data Hourly', 'value': 'vehicle_type_hourly'},
                {'label': 'Data Daily', 'value': 'vehicle_type_daily'},
                {'label': 'Data Monthly', 'value': 'vehicle_type_monthly'},
                {'label': 'Summary', 'value': 'vehicle_type_summary'},
            ],
            value='vehicle_type_hourly'
        ),
        html.Div(id='vehicle-type-output-container')
    ])
])

layout_jumlah_ganjil_genap = html.Div([
    html.Div([
        html.H2('Select Year:', style = {'font-size': '15px'}),
        dcc.Input(id="ganjil_genap_year",
                placeholder='Enter selected year...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Starting Month:', style = {'font-size': '15px'}),
        dcc.Input(id="ganjil_genap_month_start",
                placeholder='Enter starting month...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Stop Month:', style = {'font-size': '15px'}),
        dcc.Input(id="ganjil_genap_month_stop",
                placeholder='Enter stop month...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Starting Date:', style = {'font-size': '15px'}),
        dcc.Input(id="ganjil_genap_date_start",
                placeholder='Enter starting date...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Stop Date:', style = {'font-size': '15px'}),
        dcc.Input(id="ganjil_genap_date_stop",
                placeholder='Enter stop date...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Starting Hour:', style = {'font-size': '15px'}),
        dcc.Input(id="ganjil_genap_hour_start",
                placeholder='Enter starting date...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    html.Div([
        html.H2('Select Stop Hour:', style = {'font-size': '15px'}),
        dcc.Input(id="ganjil_genap_hour_stop",
                placeholder='Enter stop date...',
                type='text',
                persistence = False,
                style={'width': '400px'}
        )
    ]), 
    dcc.Store(id = 'ganjil_genap_store_inputs'),
    html.Button('Submit', id='ganjil_genap_submit_button', n_clicks=0, disabled=False, 
                style = {'font-size': '15px',
                'cursor': 'pointer',
                'text-align': 'center',
                'color': 'black',
                }),
    html.Div([
        dcc.Dropdown(
            id='ganjil_genap-dropdown',
            options=[
                {'label': 'Data Hourly', 'value': 'ganjil_genap_hourly'},
                {'label': 'Data Daily', 'value': 'ganjil_genap_daily'},
                {'label': 'Data Monthly', 'value': 'ganjil_genap_monthly'},
                {'label': 'Summary', 'value': 'ganjil_genap_summary'},
            ],
            value='ganjil_genap_hourly'
        ),
        html.Div(id='ganjil_genap-output-container')
    ])
])

# layout_jumlah_origin_area = html.Div([
#     html.Div([
#         html.H2('Select Year:', style = {'font-size': '15px'}),
#         dcc.Input(id="origin_area_year",
#                 placeholder='Enter selected year...',
#                 type='text',
#                 persistence = False,
#                 style={'width': '400px'}
#         )
#     ]), 
#     html.Div([
#         html.H2('Select Starting Month:', style = {'font-size': '15px'}),
#         dcc.Input(id="origin_area_month_start",
#                 placeholder='Enter starting month...',
#                 type='text',
#                 persistence = False,
#                 style={'width': '400px'}
#         )
#     ]), 
#     html.Div([
#         html.H2('Select Stop Month:', style = {'font-size': '15px'}),
#         dcc.Input(id="origin_area_month_stop",
#                 placeholder='Enter stop month...',
#                 type='text',
#                 persistence = False,
#                 style={'width': '400px'}
#         )
#     ]), 
#     html.Div([
#         html.H2('Select Starting Date:', style = {'font-size': '15px'}),
#         dcc.Input(id="origin_area_date_start",
#                 placeholder='Enter starting date...',
#                 type='text',
#                 persistence = False,
#                 style={'width': '400px'}
#         )
#     ]), 
#     html.Div([
#         html.H2('Select Stop Date:', style = {'font-size': '15px'}),
#         dcc.Input(id="origin_area_date_stop",
#                 placeholder='Enter stop date...',
#                 type='text',
#                 persistence = False,
#                 style={'width': '400px'}
#         )
#     ]), 
#     html.Div([
#         html.H2('Select Starting Hour:', style = {'font-size': '15px'}),
#         dcc.Input(id="origin_area_hour_start",
#                 placeholder='Enter starting date...',
#                 type='text',
#                 persistence = False,
#                 style={'width': '400px'}
#         )
#     ]), 
#     html.Div([
#         html.H2('Select Stop Hour:', style = {'font-size': '15px'}),
#         dcc.Input(id="origin_area_hour_stop",
#                 placeholder='Enter stop date...',
#                 type='text',
#                 persistence = False,
#                 style={'width': '400px'}
#         )
#     ]), 
#     dcc.Store(id = 'origin_area_store_inputs'),
#     html.Button('Submit', id='origin_area_submit_button', n_clicks=0, disabled=False, 
#                 style = {'font-size': '15px',
#                 'cursor': 'pointer',
#                 'text-align': 'center',
#                 'color': 'black',
#                 }),
#     html.Div([
#         dcc.Dropdown(
#             id='origin_area-dropdown',
#             options=[
#                 {'label': 'Data Hourly', 'value': 'origin_area_hourly'},
#                 {'label': 'Data Daily', 'value': 'origin_area_daily'},
#                 {'label': 'Data Monthly', 'value': 'origin_area_monthly'},
#                 {'label': 'Summary', 'value': 'origin_area_summary'},
#             ],
#             value='origin_area_hourly'
#         ),
#         html.Div(id='origin_area-output-container')
#     ])
# ])


server = Flask(__name__)
app = dash.Dash(__name__, server=server)

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Jumlah Jenis Kendaraan', children=[
            layout_jumlah_tipe_kendaraan,
        ]),
        dcc.Tab(label='Jumlah Ganjil Genap ', children=[
            layout_jumlah_ganjil_genap,
        ])
        # dcc.Tab(label='Jumlah Origin Area', children=[
        #     layout_jumlah_origin_area,
        # ])
    ])
])

# # ========================================= callbacks for tab 1 (jumlah type kendaraan )=============================================
@app.callback(Output("vehicle_type_store_inputs", "data"),
    [Input('vehicle_type_year', 'value'),
    Input("vehicle_type_month_start", "value"),
    Input("vehicle_type_month_stop", "value"),
    Input("vehicle_type_date_start", "value"),
    Input("vehicle_type_date_stop", "value"),
    Input("vehicle_type_hour_start", "value"),
    Input("vehicle_type_hour_stop", "value")])

def store_inputs(year, month_start, month_stop, date_start, date_stop, hour_start, hour_stop):
    features_str = [year, month_start, month_stop, date_start, date_stop, hour_start, hour_stop]
    if len(features_str) == 7 and None not in features_str and '' not in features_str:
        return {'year':year, 
            'month_start':month_start, 
            'month_stop': month_stop, 
            'date_start':date_start, 
            'date_stop':date_stop, 
            'hour_start':hour_start, 
            'hour_stop':hour_stop}
    
@app.callback(Output('vehicle-type-output-container', 'children'), 
                [Input('vehicle_type_submit_button', 'n_clicks'),
                Input('vehicle-type-dropdown', 'value')],
                State('vehicle_type_store_inputs', 'data'))

def update_vehicle_type(n_click, dropdown_value_option, stored_inputs):
    trigger = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if stored_inputs is not None:
        year = int(stored_inputs['year'])
        month_start =int(stored_inputs['month_start'])
        month_stop =int(stored_inputs['month_stop'])
        date_start =int(stored_inputs['date_start'])
        date_stop =int(stored_inputs['date_stop'])
        hour_start =int(stored_inputs['hour_start'])
        hour_stop =int(stored_inputs['hour_stop'])

        datetime_start = f'{date_start}/{month_start}/{year} {hour_start}'
        datetime_start = datetime.strptime(datetime_start, '%d/%m/%Y %H')
        print(datetime_start)

        datetime_stop = f'{date_stop}/{month_stop}/{year} {hour_stop}'
        datetime_stop = datetime.strptime(datetime_stop, '%d/%m/%Y %H')
        print(datetime_stop)

        engine = create_engine('mysql+pymysql://' + DBconfig.user + ':' + DBconfig.pwd + '@' + DBconfig.host + ':' + str(DBconfig.port) + '/' + DBconfig.db_name , echo=False)
        query = f"SELECT * FROM lpr_table_use where timestamp >= '{datetime_start}' AND timestamp <= '{datetime_stop}'"
        lpr_data = pd.read_sql(query, con=engine)

        print('[INFO] data size:', lpr_data.shape)
    
        if n_click > 0:
            print('[INFO] n_click:', n_click)
            if dropdown_value_option == 'vehicle_type_hourly':
                if lpr_data.shape[0] > 0:
                    lpr_data_hourly = lpr_data.copy()
                    lpr_data_hourly = lpr_data_hourly.groupby(by=['vehicle_type', 'timestamp']).agg("count")
                    lpr_data_hourly.reset_index(inplace=True)
                    lpr_data_hourly = lpr_data_hourly.sort_values(by='timestamp', ascending=True)
                    lpr_data_hourly = lpr_data_hourly.rename(columns={'license_plate': 'Count Vehicle'})
                    fig = px.bar(lpr_data_hourly, x="timestamp", y="Count Vehicle", color="vehicle_type", title="Hourly Vehicle Counting")
                    return dcc.Graph(figure=fig)
                else:
                    return html.P([f'Data did not found in selected range'],
                                            style = {"padding-top": "20px", 
                                                        'display': 'list',
                                                         'font-size': '25px',})
            
            if dropdown_value_option == 'vehicle_type_daily':
                if lpr_data.shape[0] > 0:
                    lpr_data_daily = lpr_data.copy()
                    lpr_data_daily['day_hour'] = pd.to_datetime(lpr_data_daily['timestamp'], format='%Y-%m-%d %H').dt.floor('H')
                    lpr_data_daily = lpr_data_daily.groupby(by=['vehicle_type', 'day_hour']).agg("count")
                    lpr_data_daily.reset_index(inplace=True)
                    lpr_data_daily = lpr_data_daily.sort_values(by='day_hour', ascending=True)
                    lpr_data_daily = lpr_data_daily.drop(columns=['timestamp'])
                    lpr_data_daily = lpr_data_daily.rename(columns={'license_plate': 'Count Vehicle'})
                    fig = px.bar(lpr_data_daily, x='day_hour', y="Count Vehicle", color="vehicle_type", title="Daily Vehicle Counting")
                    return dcc.Graph(figure=fig)
                else:
                    return html.P([f'Data did not found in selected range'],
                                            style = {"padding-top": "20px", 
                                                        'display': 'list',
                                                         'font-size': '25px',})
            
            if dropdown_value_option == 'vehicle_type_monthly':
                if lpr_data.shape[0] > 0:
                    lpr_data_monthly = lpr_data.copy()
                    lpr_data_monthly['month'] = lpr_data_monthly['timestamp'].apply(lambda x: x.strftime('%m-%Y')) 
                    lpr_data_monthly = lpr_data_monthly.groupby(by=['vehicle_type', 'month']).agg("count")
                    lpr_data_monthly.reset_index(inplace=True)
                    lpr_data_monthly = lpr_data_monthly.sort_values(by='month', ascending=True)
                    lpr_data_monthly = lpr_data_monthly.drop(columns=['timestamp'])
                    lpr_data_monthly = lpr_data_monthly.rename(columns={'license_plate': 'Count Vehicle'})
                    fig = px.bar(lpr_data_monthly, x='month', y="Count Vehicle", color="vehicle_type", title="Monthly Vehicle Counting")
                    return dcc.Graph(figure=fig)
                else:
                    return html.P([f'Data did not found in selected range'],
                                            style = {"padding-top": "20px", 
                                                        'display': 'list',
                                                         'font-size': '25px',})
            
            if dropdown_value_option == 'vehicle_type_summary':
                if lpr_data.shape[0] > 0:
                    ## Summarize hourly in a day (24 hour)
                    lpr_data_summary_hourly = lpr_data.copy()
                    lpr_data_summary_hourly['hour'] = lpr_data_summary_hourly['timestamp'].dt.hour
                    lpr_data_summary_hourly = lpr_data_summary_hourly.groupby(by=['vehicle_type', 'hour']).agg("count")
                    lpr_data_summary_hourly.reset_index(inplace=True)
                    lpr_data_summary_hourly = lpr_data_summary_hourly.drop(columns=['timestamp'])
                    lpr_data_summary_hourly = lpr_data_summary_hourly.rename(columns={'license_plate': 'Count Vehicle'})
                    lpr_data_summary_hourly_fig = px.bar(lpr_data_summary_hourly, x="hour", y="Count Vehicle", color="vehicle_type", title="Summary Hourly Vehicle Counting")

                    ## Summarize weekday in a week (7 days)
                    lpr_data_summary_weekly = lpr_data.copy()
                    lpr_data_summary_weekly['weekday'] = lpr_data_summary_weekly['timestamp'].dt.day_name()
                    lpr_data_summary_weekly = lpr_data_summary_weekly.groupby(by=['vehicle_type', 'weekday']).agg("count")
                    lpr_data_summary_weekly.reset_index(inplace=True)
                    lpr_data_summary_weekly = lpr_data_summary_weekly.drop(columns=['timestamp'])
                    lpr_data_summary_weekly = lpr_data_summary_weekly.rename(columns={'license_plate': 'Count Vehicle'})
                    lpr_data_summary_weekly_fig = px.bar(lpr_data_summary_weekly, x="weekday", y="Count Vehicle", color="vehicle_type", title="Summary Weekly Vehicle Counting")

                    ## Summarize daily in a month (30 days)
                    lpr_data_summary_daily = lpr_data.copy()
                    lpr_data_summary_daily['day'] = lpr_data_summary_daily['timestamp'].dt.day
                    lpr_data_summary_daily = lpr_data_summary_daily.groupby(by=['vehicle_type', 'day']).agg("count")
                    lpr_data_summary_daily.reset_index(inplace=True)
                    lpr_data_summary_daily = lpr_data_summary_daily.drop(columns=['timestamp'])
                    lpr_data_summary_daily = lpr_data_summary_daily.rename(columns={'license_plate': 'Count Vehicle'})
                    lpr_data_summary_daily_fig = px.bar(lpr_data_summary_daily, x="day", y="Count Vehicle", color="vehicle_type", title="Summary Monthly Vehicle Counting")

                    ## Summarize Total
                    lpr_data_summary_total = lpr_data.copy()
                    lpr_data_summary_total = lpr_data_summary_total.groupby(by=['vehicle_type']).agg("count")
                    lpr_data_summary_total.reset_index(inplace=True)
                    lpr_data_summary_total = lpr_data_summary_total.drop(columns=['timestamp'])
                    lpr_data_summary_total = lpr_data_summary_total.rename(columns={'license_plate': 'Count Vehicle'})
                    lpr_data_summary_total_fig = px.pie(lpr_data_summary_total, values='Count Vehicle', names='vehicle_type', title='Total counted vehicle type')

                    vehicle_type_summary_layout = html.Div([
                        dcc.Graph(figure=lpr_data_summary_hourly_fig),
                        dcc.Graph(figure=lpr_data_summary_weekly_fig),
                        dcc.Graph(figure=lpr_data_summary_daily_fig),
                        dcc.Graph(figure=lpr_data_summary_total_fig),
                    ])

                    return vehicle_type_summary_layout
                else:
                    return html.P([f'Data did not found in selected range'],
                                            style = {"padding-top": "20px", 
                                                        'display': 'list',
                                                         'font-size': '25px',})
        else:
            return dash.no_update
    else:
            return dash.no_update


# ========================================= callbacks for tab 2 (jumlah ganjil genap )=============================================
@app.callback(Output("ganjil_genap_store_inputs", "data"),
    [Input('ganjil_genap_year', 'value'),
    Input("ganjil_genap_month_start", "value"),
    Input("ganjil_genap_month_stop", "value"),
    Input("ganjil_genap_date_start", "value"),
    Input("ganjil_genap_date_stop", "value"),
    Input("ganjil_genap_hour_start", "value"),
    Input("ganjil_genap_hour_stop", "value")])

def store_inputs(year, month_start, month_stop, date_start, date_stop, hour_start, hour_stop):
    features_str = [year, month_start, month_stop, date_start, date_stop, hour_start, hour_stop]
    if len(features_str) == 7 and None not in features_str and '' not in features_str:
        return {'year':year, 
            'month_start':month_start, 
            'month_stop': month_stop, 
            'date_start':date_start, 
            'date_stop':date_stop, 
            'hour_start':hour_start, 
            'hour_stop':hour_stop}
    
@app.callback(Output('ganjil_genap-output-container', 'children'), 
                [Input('ganjil_genap_submit_button', 'n_clicks'),
                Input('ganjil_genap-dropdown', 'value')],
                State('ganjil_genap_store_inputs', 'data'))

def update_ganjil_genap(n_click, dropdown_value_option, stored_inputs):
    trigger = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if stored_inputs is not None:
        year = int(stored_inputs['year'])
        month_start =int(stored_inputs['month_start'])
        month_stop =int(stored_inputs['month_stop'])
        date_start =int(stored_inputs['date_start'])
        date_stop =int(stored_inputs['date_stop'])
        hour_start =int(stored_inputs['hour_start'])
        hour_stop =int(stored_inputs['hour_stop'])

        datetime_start = f'{date_start}/{month_start}/{year} {hour_start}'
        datetime_start = datetime.strptime(datetime_start, '%d/%m/%Y %H')
        print(datetime_start)

        datetime_stop = f'{date_stop}/{month_stop}/{year} {hour_stop}'
        datetime_stop = datetime.strptime(datetime_stop, '%d/%m/%Y %H')
        print(datetime_stop)

        engine = create_engine('mysql+pymysql://' + DBconfig.user + ':' + DBconfig.pwd + '@' + DBconfig.host + ':' + str(DBconfig.port) + '/' + DBconfig.db_name , echo=False)
        query = f"SELECT * FROM lpr_table_use where timestamp >= '{datetime_start}' AND timestamp <= '{datetime_stop}'"
        lpr_data = pd.read_sql(query, con=engine)

        print('[INFO] data size:', lpr_data.shape)
    
        if n_click > 0:
            print('[INFO] n_click:', n_click)
            if dropdown_value_option == 'ganjil_genap_hourly':
                if lpr_data.shape[0] > 0:
                    ganjil_genap_hourly = lpr_data.copy()
                    ganjil_genap_hourly['ganjil_genap'] = ganjil_genap_hourly['license_plate'].apply(define_ganjil_genap)
                    ganjil_genap_hourly = ganjil_genap_hourly.groupby(by=['ganjil_genap', 'timestamp']).agg("count")
                    ganjil_genap_hourly.reset_index(inplace=True)
                    ganjil_genap_hourly = ganjil_genap_hourly.sort_values(by='timestamp', ascending=True)
                    ganjil_genap_hourly = ganjil_genap_hourly.rename(columns={'license_plate': 'Count Ganjil Genap'})
                    fig = px.bar(ganjil_genap_hourly, x="timestamp", y="Count Ganjil Genap", color="ganjil_genap", title="Hourly Counted Ganjil Genap")
                    return dcc.Graph(figure=fig)
                else:
                    return html.P([f'Data did not found in selected range'],
                                            style = {"padding-top": "20px", 
                                                        'display': 'list',
                                                         'font-size': '25px',})
            
            if dropdown_value_option == 'ganjil_genap_daily':
                if lpr_data.shape[0] > 0:
                    ganjil_genap_daily = lpr_data.copy()
                    ganjil_genap_daily['ganjil_genap'] = ganjil_genap_daily['license_plate'].apply(define_ganjil_genap)
                    ganjil_genap_daily['day_hour'] = pd.to_datetime(ganjil_genap_daily['timestamp'], format='%Y-%m-%d %H').dt.floor('H')
                    ganjil_genap_daily = ganjil_genap_daily.groupby(by=['ganjil_genap', 'day_hour']).agg("count")
                    ganjil_genap_daily.reset_index(inplace=True)
                    ganjil_genap_daily = ganjil_genap_daily.sort_values(by='day_hour', ascending=True)
                    ganjil_genap_daily = ganjil_genap_daily.drop(columns=['timestamp'])
                    ganjil_genap_daily = ganjil_genap_daily.rename(columns={'license_plate': 'Count Ganjil Genap'})
                    fig = px.bar(ganjil_genap_daily, x='day_hour', y="Count Ganjil Genap", color="ganjil_genap", title="Daily Counted Ganjil Genap")
                    return dcc.Graph(figure=fig)
                else:
                    return html.P([f'Data did not found in selected range'],
                                            style = {"padding-top": "20px", 
                                                        'display': 'list',
                                                         'font-size': '25px',})
            
            if dropdown_value_option == 'ganjil_genap_monthly':
                if lpr_data.shape[0] > 0:
                    ganjil_genap_monthly = lpr_data.copy()
                    ganjil_genap_monthly['ganjil_genap'] = ganjil_genap_monthly['license_plate'].apply(define_ganjil_genap)
                    ganjil_genap_monthly['month'] = ganjil_genap_monthly['timestamp'].apply(lambda x: x.strftime('%m-%Y')) 
                    ganjil_genap_monthly = ganjil_genap_monthly.groupby(by=['ganjil_genap', 'month']).agg("count")
                    ganjil_genap_monthly.reset_index(inplace=True)
                    ganjil_genap_monthly = ganjil_genap_monthly.sort_values(by='month', ascending=True)
                    ganjil_genap_monthly = ganjil_genap_monthly.drop(columns=['timestamp'])
                    ganjil_genap_monthly = ganjil_genap_monthly.rename(columns={'license_plate': 'Count Ganjil Genap'})
                    fig = px.bar(ganjil_genap_monthly, x='month', y="Count Ganjil Genap", color="ganjil_genap", title="Monthly Counted Ganjil Genap")
                    return dcc.Graph(figure=fig)
                else:
                    return html.P([f'Data did not found in selected range'],
                                            style = {"padding-top": "20px", 
                                                        'display': 'list',
                                                         'font-size': '25px',})
            
            if dropdown_value_option == 'ganjil_genap_summary':
                if lpr_data.shape[0] > 0:
                    ## Summarize hourly in a day (24 hour)
                    ganjil_genap_summary_hourly = lpr_data.copy()
                    ganjil_genap_summary_hourly['ganjil_genap'] = ganjil_genap_summary_hourly['license_plate'].apply(define_ganjil_genap)
                    ganjil_genap_summary_hourly['hour'] = ganjil_genap_summary_hourly['timestamp'].dt.hour
                    ganjil_genap_summary_hourly = ganjil_genap_summary_hourly.groupby(by=['ganjil_genap', 'hour']).agg("count")
                    ganjil_genap_summary_hourly.reset_index(inplace=True)
                    ganjil_genap_summary_hourly = ganjil_genap_summary_hourly.drop(columns=['timestamp'])
                    ganjil_genap_summary_hourly = ganjil_genap_summary_hourly.rename(columns={'license_plate': 'Count Ganjil Genap'})
                    ganjil_genap_summary_hourly_fig = px.bar(ganjil_genap_summary_hourly, x="hour", y="Count Ganjil Genap", color="ganjil_genap", title="Summary Hourly Counted Ganjil Genap")

                    ## Summarize weekday in a week (7 days)
                    ganjil_genap_summary_weekly = lpr_data.copy()
                    ganjil_genap_summary_weekly['ganjil_genap'] = ganjil_genap_summary_weekly['license_plate'].apply(define_ganjil_genap)
                    ganjil_genap_summary_weekly['weekday'] = ganjil_genap_summary_weekly['timestamp'].dt.day_name()
                    ganjil_genap_summary_weekly = ganjil_genap_summary_weekly.groupby(by=['ganjil_genap', 'weekday']).agg("count")
                    ganjil_genap_summary_weekly.reset_index(inplace=True)
                    ganjil_genap_summary_weekly = ganjil_genap_summary_weekly.drop(columns=['timestamp'])
                    ganjil_genap_summary_weekly = ganjil_genap_summary_weekly.rename(columns={'license_plate': 'Count Ganjil Genap'})
                    ganjil_genap_summary_weekly_fig = px.bar(ganjil_genap_summary_weekly, x="weekday", y="Count Ganjil Genap", color="ganjil_genap", title="Summary Weekly Counted Ganjil Genap")

                    ## Summarize daily in a month (30 days)
                    ganjil_genap_summary_daily = lpr_data.copy()
                    ganjil_genap_summary_daily['ganjil_genap'] = ganjil_genap_summary_daily['license_plate'].apply(define_ganjil_genap)
                    ganjil_genap_summary_daily['day'] = ganjil_genap_summary_daily['timestamp'].dt.day
                    ganjil_genap_summary_daily = ganjil_genap_summary_daily.groupby(by=['ganjil_genap', 'day']).agg("count")
                    ganjil_genap_summary_daily.reset_index(inplace=True)
                    ganjil_genap_summary_daily = ganjil_genap_summary_daily.drop(columns=['timestamp'])
                    ganjil_genap_summary_daily = ganjil_genap_summary_daily.rename(columns={'license_plate': 'Count Ganjil Genap'})
                    ganjil_genap_summary_daily_fig = px.bar(ganjil_genap_summary_daily, x="day", y="Count Ganjil Genap", color="ganjil_genap", title="Summary Daily Counted Ganjil Genap")

                    ## Summarize Total
                    ganjil_genap_summary_total = lpr_data.copy()
                    ganjil_genap_summary_total['ganjil_genap'] = ganjil_genap_summary_total['license_plate'].apply(define_ganjil_genap)
                    ganjil_genap_summary_total = ganjil_genap_summary_total.groupby(by=['ganjil_genap']).agg("count")
                    ganjil_genap_summary_total.reset_index(inplace=True)
                    ganjil_genap_summary_total = ganjil_genap_summary_total.drop(columns=['timestamp'])
                    ganjil_genap_summary_total = ganjil_genap_summary_total.rename(columns={'license_plate': 'Total Counted Ganjil Genap'})
                    ganjil_genap_summary_total_fig = px.pie(ganjil_genap_summary_total, values='Total Counted Ganjil Genap', names='ganjil_genap', title='Total Counted Ganjil Genap')

                    ganjil_genap_summary_layout = html.Div([
                        dcc.Graph(figure=ganjil_genap_summary_hourly_fig),
                        dcc.Graph(figure=ganjil_genap_summary_weekly_fig),
                        dcc.Graph(figure=ganjil_genap_summary_daily_fig),
                        dcc.Graph(figure=ganjil_genap_summary_total_fig),
                    ])

                    return ganjil_genap_summary_layout
                else:
                    return html.P([f'Data did not found in selected range'],
                                            style = {"padding-top": "20px", 
                                                        'display': 'list',
                                                         'font-size': '25px',})
        else:
            return dash.no_update
    else:
            return dash.no_update

# ========================================= callbacks for tab 3 (jumlah origin area)=============================================
# @app.callback(Output("origin_area_store_inputs", "data"),
#     [Input('origin_area_year', 'value'),
#     Input("origin_area_month_start", "value"),
#     Input("origin_area_month_stop", "value"),
#     Input("origin_area_date_start", "value"),
#     Input("origin_area_date_stop", "value"),
#     Input("origin_area_hour_start", "value"),
#     Input("origin_area_hour_stop", "value")])

# def store_inputs(year, month_start, month_stop, date_start, date_stop, hour_start, hour_stop):
#     features_str = [year, month_start, month_stop, date_start, date_stop, hour_start, hour_stop]
#     if len(features_str) == 7 and None not in features_str and '' not in features_str:
#         return {'year':year, 
#             'month_start':month_start, 
#             'month_stop': month_stop, 
#             'date_start':date_start, 
#             'date_stop':date_stop, 
#             'hour_start':hour_start, 
#             'hour_stop':hour_stop}
    
# @app.callback(Output('origin_area-output-container', 'children'), 
#                 [Input('origin_area_submit_button', 'n_clicks'),
#                 Input('origin_area-dropdown', 'value')],
#                 State('origin_area_store_inputs', 'data'))

# def update_ganjil_genap(n_click, dropdown_value_option, stored_inputs):
#     trigger = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if stored_inputs is not None:
#         year = int(stored_inputs['year'])
#         month_start =int(stored_inputs['month_start'])
#         month_stop =int(stored_inputs['month_stop'])
#         date_start =int(stored_inputs['date_start'])
#         date_stop =int(stored_inputs['date_stop'])
#         hour_start =int(stored_inputs['hour_start'])
#         hour_stop =int(stored_inputs['hour_stop'])

#         datetime_start = f'{date_start}/{month_start}/{year} {hour_start}'
#         datetime_start = datetime.strptime(datetime_start, '%d/%m/%Y %H')
#         print(datetime_start)

#         datetime_stop = f'{date_stop}/{month_stop}/{year} {hour_stop}'
#         datetime_stop = datetime.strptime(datetime_stop, '%d/%m/%Y %H')
#         print(datetime_stop)

#         engine = create_engine('mysql+pymysql://' + DBconfig.user + ':' + DBconfig.pwd + '@' + DBconfig.host + ':' + str(DBconfig.port) + '/' + DBconfig.db_name , echo=False)
#         query = f"SELECT * FROM lpr_table_use where timestamp >= '{datetime_start}' AND timestamp <= '{datetime_stop}'"
#         lpr_data = pd.read_sql(query, con=engine)

#         print('[INFO] data size:', lpr_data.shape)
    
#         if n_click > 0:
#             print('[INFO] origin_area n_click:', n_click)
#             if dropdown_value_option == 'origin_area_hourly':
#                 if lpr_data.shape[0] > 0:
#                     origin_hourly = lpr_data.copy()
#                     origin_hourly['origin'] = origin_hourly['license_plate'].apply(get_origin_license)
#                     origin_hourly = origin_hourly.groupby(by=['origin', 'timestamp']).agg("count")
#                     origin_hourly.reset_index(inplace=True)
#                     origin_hourly = origin_hourly.sort_values(by='timestamp', ascending=True)
#                     origin_hourly = origin_hourly.rename(columns={'license_plate': 'Count Origin'})
#                     fig = px.bar(origin_hourly, x="timestamp", y="Count Origin", color="origin", title="Hourly Origin Area")
#                     return dcc.Graph(figure=fig)
#                 else:
#                     return html.P([f'Data did not found in selected range'],
#                                             style = {"padding-top": "20px", 
#                                                         'display': 'list',
#                                                          'font-size': '25px',})
            
#             if dropdown_value_option == 'origin_area_daily':
#                 if lpr_data.shape[0] > 0:
#                     origin_daily = lpr_data.copy()
#                     origin_daily['origin'] = origin_daily['license_plate'].apply(get_origin_license)
#                     origin_daily['day_hour'] = pd.to_datetime(origin_daily['timestamp'], format='%Y-%m-%d %H').dt.floor('H')
#                     origin_daily = origin_daily.groupby(by=['origin', 'day_hour']).agg("count")
#                     origin_daily.reset_index(inplace=True)
#                     origin_daily = origin_daily.sort_values(by='day_hour', ascending=True)
#                     origin_daily = origin_daily.drop(columns=['timestamp'])
#                     origin_daily = origin_daily.rename(columns={'license_plate': 'Count Origin'})
#                     fig = px.bar(origin_daily, x='day_hour', y="Count Origin", color="origin", title="Daily Origin Area")
#                     return dcc.Graph(figure=fig)
#                 else:
#                     return html.P([f'Data did not found in selected range'],
#                                             style = {"padding-top": "20px", 
#                                                         'display': 'list',
#                                                          'font-size': '25px',})
            
#             if dropdown_value_option == 'origin_area_monthly':
#                 if lpr_data.shape[0] > 0:
#                     origin_monthly = lpr_data.copy()
#                     origin_monthly['origin'] = origin_monthly['license_plate'].apply(get_origin_license)
#                     origin_monthly['month'] = origin_monthly['timestamp'].apply(lambda x: x.strftime('%m-%Y')) 
#                     origin_monthly = origin_monthly.groupby(by=['origin', 'month']).agg("count")
#                     origin_monthly.reset_index(inplace=True)
#                     origin_monthly = origin_monthly.sort_values(by='month', ascending=True)
#                     origin_monthly = origin_monthly.drop(columns=['timestamp'])
#                     origin_monthly = origin_monthly.rename(columns={'license_plate': 'Count Origin'})
#                     fig = px.bar(origin_monthly, x='month', y="Count Origin", color="origin", title="Monthly Origin Area")
#                     return dcc.Graph(figure=fig)
#                 else:
#                     return html.P([f'Data did not found in selected range'],
#                                             style = {"padding-top": "20px", 
#                                                         'display': 'list',
#                                                          'font-size': '25px',})
            
#             if dropdown_value_option == 'origin_area_summary':
#                 if lpr_data.shape[0] > 0:
#                     ## Summarize hourly in a day (24 hour)
#                     origin_summary_hourly = lpr_data.copy()
#                     origin_summary_hourly['origin'] = origin_summary_hourly['license_plate'].apply(get_origin_license)
#                     origin_summary_hourly['hour'] = origin_summary_hourly['timestamp'].dt.hour
#                     origin_summary_hourly = origin_summary_hourly.groupby(by=['origin', 'hour']).agg("count")
#                     origin_summary_hourly.reset_index(inplace=True)
#                     origin_summary_hourly = origin_summary_hourly.drop(columns=['timestamp'])
#                     origin_summary_hourly = origin_summary_hourly.rename(columns={'license_plate': 'Count Origin'})
#                     origin_summary_hourly_fig = px.bar(origin_summary_hourly, x="hour", y="Count Origin", color="origin", title="Summary Hourly Counted Origin")

#                     ## Summarize weekday in a week (7 days)
#                     origin_summary_weekly = lpr_data.copy()
#                     origin_summary_weekly['origin'] = origin_summary_weekly['license_plate'].apply(get_origin_license)
#                     origin_summary_weekly['weekday'] = origin_summary_weekly['timestamp'].dt.day_name()
#                     origin_summary_weekly = origin_summary_weekly.groupby(by=['origin', 'weekday']).agg("count")
#                     origin_summary_weekly.reset_index(inplace=True)
#                     origin_summary_weekly = origin_summary_weekly.drop(columns=['timestamp'])
#                     origin_summary_weekly = origin_summary_weekly.rename(columns={'license_plate': 'Count Origin'})
#                     origin_summary_weekly_fig = px.bar(origin_summary_weekly, x="weekday", y="Count Origin", color="origin", title="Summary Weekly Counted Origin")

#                     ## Summarize daily in a month (30 days)
#                     origin_summary_daily = lpr_data.copy()
#                     origin_summary_daily['origin'] = origin_summary_daily['license_plate'].apply(get_origin_license)
#                     origin_summary_daily['day'] = origin_summary_daily['timestamp'].dt.day
#                     origin_summary_daily = origin_summary_daily.groupby(by=['origin', 'day']).agg("count")
#                     origin_summary_daily.reset_index(inplace=True)
#                     origin_summary_daily = origin_summary_daily.drop(columns=['timestamp'])
#                     origin_summary_daily = origin_summary_daily.rename(columns={'license_plate': 'Count Origin'})
#                     origin_summary_daily_fig = px.bar(origin_summary_daily, x="day", y="Count Origin", color="origin", title="Summary daily Counted Origin")

#                     ## Summarize Total
#                     origin_summary_total = lpr_data.copy()
#                     origin_summary_total['origin'] = origin_summary_total['license_plate'].apply(get_origin_license)
#                     origin_summary_total = origin_summary_total.groupby(by=['origin']).agg("count")
#                     origin_summary_total.reset_index(inplace=True)
#                     origin_summary_total = origin_summary_total.drop(columns=['timestamp'])
#                     origin_summary_total = origin_summary_total.rename(columns={'license_plate': 'Total Counted Origin'})
#                     origin_summary_total_fig = px.pie(origin_summary_total, values='Total Counted Origin', names='origin', title='Summary Total Counted Ganjil Genap')

#                     origin_area_summary_layout = html.Div([
#                         dcc.Graph(figure=origin_summary_hourly_fig),
#                         dcc.Graph(figure=origin_summary_weekly_fig),
#                         dcc.Graph(figure=origin_summary_daily_fig),
#                         dcc.Graph(figure=origin_summary_total_fig),
#                     ])

#                     return origin_area_summary_layout
#                 else:
#                     return html.P([f'Data did not found in selected range'],
#                                             style = {"padding-top": "20px", 
#                                                         'display': 'list',
#                                                          'font-size': '25px',})
#         else:
#             return dash.no_update
#     else:
#             return dash.no_update

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)