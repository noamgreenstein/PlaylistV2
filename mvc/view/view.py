from dash import Dash, html, dcc, Output, Input, State, dash_table, ctx
import pandas as pd
import constants as c

from mvc.model.music_model import MusicModel

model = MusicModel()
app = Dash(__name__)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Search',
                children=[
                    html.Div([
                        dcc.Input(id='search-input', type='text', placeholder='Enter search term...'
                                  , style={'width': '50%'}),
                        dcc.Dropdown(
                            id='option-selector',
                            options=[
                                {'label': 'Artist', 'value': 'artist'},
                                {'label': 'Album', 'value': 'album'},
                                {'label': 'Track', 'value': 'track'}
                            ],
                            placeholder='Type...',
                            style={'width': '40%'}),

                        dcc.Dropdown(
                            id='limit-selector',
                            options=[
                                {'label': f'{l}', 'value': f'{l}'} for l in range(5, 11)
                            ],
                            placeholder='Limit...',
                            style={'width': '40%'}),

                        html.Button('Search', id='search-button', n_clicks=0,
                                    style={'width': '25%'}),

                    ], style={'display': 'flex'}),
                    html.Div(id='output-container'),
                    html.Div([
                        dcc.Checklist(id='select-results', options=[], value=[]),
                        html.Button('Add to Library', id='add-button', n_clicks=0)
                    ])
                ]),

        dcc.Tab(label='Library',
                children=[
                    dcc.Dropdown(
                        id='library-selector',
                        options=[
                            {'label': 'Artists', 'value': 'artists'},
                            {'label': 'Albums', 'value': 'albums'},
                            {'label': 'Tracks', 'value': 'tracks'}
                        ],
                        value='artists',
                        style={'width': '40%'}),
                    dash_table.DataTable(
                        id='data-table',
                        style_table={'width': '50%'},
                        sort_action='native',
                        filter_action='native',
                        row_selectable='multi'
                    ),
                    html.Button('Delete Selected Rows', id='delete-btn', n_clicks=0),
                    html.Button('Submit New Ratings', id='ratings-submit', n_clicks=0, hidden=True),
                ]),

    ])
])


@app.callback(
    Output('output-container', 'children'),
    Output('select-results', 'options', allow_duplicate=True),
    Input('search-button', 'n_clicks'),
    State('search-input', 'value'),
    State('option-selector', 'value'),
    State('limit-selector', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, search_value, selected_option, limit):
    if n_clicks > 0:
        data = c.name_data
        item = 'artist' if selected_option is None else selected_option
        data['params']['name'] = search_value
        data['params']['item'] = item
        data['params']['limit'] = 5 if limit is None else limit
        data = model.use_spotify(data)
        if item == 'artist':
            options = [{'label': x['name'],
                        'value': f"artists;{x['name']};{x['id']};"
                                 f"{x['images'][0]['url'] if len(x['images']) > 0 else 'none'}"}
                       for x in data]
        elif item == 'track':
            options = [{'label': x['name'] + ' | ' + x['artists'][0]['name'] + ' | '
                                 + x['album']['name'] if x['album']['album_type'] == 'album' else
            x['name'] + ' | ' + x['artists'][0]['name'] + ' | Single',
                        'value': f"tracks;{x['name']};{x['id']};{x['artists'][0]['id']};"
                                 f"{x['album']['id']}"}
                       for x in data]
        else:
            options = [{'label': x['name'] + ' | ' + x['artists'][0]['name'],
                        'value': f"albums;{x['name']};{x['id']};{x['artists'][0]['id']};"
                                 f"{x['images'][0]['url'] if len(x['images']) > 0 else 'none'}"}
                       for x in data]

        return '', options
    return "Enter search terms and select an option.", []


@app.callback(
    Output('select-results', 'options', allow_duplicate=True),
    Input('add-button', 'n_clicks'),
    State('select-results', 'value'),
    prevent_initial_call=True
)
def add_to_library(n_clicks, selected_items):
    if n_clicks > 0 and len(selected_items) > 0:
        for item in selected_items:
            i = item.split(';')
            data = c.save_data
            data['table'] = i[0]
            data['columns'] = c.column_data.get(i[0])
            data['params'] = str(i[1:]).replace('[', '(').replace(']', ')')
            model.use_db(data)
            model.update()
    return []


@app.callback(
    Output('data-table', 'columns', allow_duplicate=True),
    Output('data-table', 'data', allow_duplicate=True),
    Input('library-selector', 'value'),
    prevent_initial_call='initial_duplicate'
)
def get_data(library_value):
    data = c.get_data
    data['table'] = library_value
    data['columns'] = c.selects[library_value]
    table_data = model.use_db(data)
    df = pd.DataFrame(table_data, columns=c.table_column[library_value])
    data_dict = df.to_dict('records')
    return [{"name": i, "id": i} if library_value != 'tracks' or i != 'Rating' else
            {"name": i, "id": i, 'editable': True} for i in df.columns], data_dict


@app.callback(
    Output('ratings-submit', 'hidden'),
    Input('library-selector', 'value')
)
def can_submit(library_value):
    return not library_value == 'tracks'


@app.callback(
    Output('ratings-submit', 'n_clicks'),
    Input('data-table', 'data'),
    Input('ratings-submit', 'n_clicks')
)
def update_ratings(data, n_clicks):
    if n_clicks > 0:
        for t in data:
            model.update_row('tracks',
                             [{'row': 'rating', 'value': t['Rating']}],
                             [{'row': 'track_id', 'value': t['ID']}])
    return 0


@app.callback(
    Output('data-table', 'columns', allow_duplicate=True),
    Output('data-table', 'data', allow_duplicate=True),
    State('library-selector', 'value'),
    Input('delete-btn', 'n_clicks'),
    State('data-table', 'selected_rows'),
    prevent_initial_call=True
)
def delete_data(library_value, n_clicks, rows):
    if n_clicks > 0:
        print(n_clicks)
        delete = c.delete_data
        delete['table'] = library_value
        param_str = f'{library_value[:-1]}_id = '
        print(rows)
        return get_data(library_value)
    return get_data(library_value)


if __name__ == '__main__':
    app.run(debug=True)
