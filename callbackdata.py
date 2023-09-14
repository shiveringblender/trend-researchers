


tab_callbacks = {
    'home': {
        'callback': home_callbacks.update_chart,
        'outputs': [
            Output('selected-chart', 'figure'),
            OutputChecker('bar-chart-text', 'children'),
            Output('volatility-chart-text', 'children'),
            Output('line-chart-text', 'children'),
            Output('returns-chart-text', 'children'),
        ],
    },
    'correlation': {
        'callback': correlation_callbacks.update_chart,
        'outputs': [
            Output('selected-chart', 'figure'),
            Output('bar-chart-text', 'children'),
            Output('volatility-chart-text', 'children'),
            Output('line-chart-text', 'children'),
            Output('returns-chart-text', 'children'),
        ],
    },