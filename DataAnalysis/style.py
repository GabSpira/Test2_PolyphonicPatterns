import pandas as pd


# Def tables style
styles = [
    dict(selector="tr:hover",
                props=[("background", "#D6EEEE")]),
    dict(selector="th.col_heading", props=[("color", "#fff"),
                            ("border", "3px solid #FFFFFF"),
                            ("padding", "12px 35px"),
                            #("border-collapse", "collapse"),
                            ("background", "#1D4477"),
                            ("font-size", "18px")
                            ]),
    dict(selector="th.row_heading", props=[("color", "#fff"),
                            ("border", "3px solid #FFFFFF"),
                            ("padding", "12px 35px"),
                            #("border-collapse", "collapse"),
                            ("background", "#1D4477"),
                            ("font-size", "15px")
                            ]),
    dict(selector="td", props=[("color", "#000000"),
                            ("border", "3px solid #FFFFFF"),
                            ("padding", "12px 35px"),
                            ('margin', '2px'),
                            # ("border-collapse", "collapse"),
                            ("font-size", "15px")   
                            ]),
    dict(selector="table", props=[                                   
                                    ("font-family" , 'Helvetica'),
                                    ("margin" , "25px auto"),
                                    ("border-collapse" , "collapse"),
                                    ("border" , "3px solid #FFFFFF"),
                                    ("border-bottom" , "2px solid #00cccc")                            
                                    ]),
    dict(selector="caption", props=[("caption-side", "left"), ("margin", "6px"), ("text-align", "right"), ("font-size", "120%"),
                                        ("font-weight", "bold")]),
    dict(selector="tr:nth-child(even)", props=[
        ("background-color", "#D9EFFA"),
    ]),
    dict(selector="tr:nth-child(odd)", props=[
        ("background-color", "#DEF4FF"),
    ]),
]

# Style function to highlight max value
def style_max(x, max_row, max_col):

    color = 'background-color: #BFE3F5'
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    
    df1.iloc[max_row, max_col] = color
    return df1