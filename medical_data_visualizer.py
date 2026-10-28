import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")

# 2
df['overweight'] = (df['weight'] / ((df['height'] / 100)**2 ) > 25).astype(int)
 #astype(int) converts the boolean condition True/False into 1/0
# 3
df['cholesterol'] = (df['cholesterol']>1).astype(int)

# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt( #pd.melt reshapes the DF from wide to long format
        df,
        id_vars=['cardio'], #this is the anchor and all other variables are gathered into a single variable column 
        #with their 0 or 1 in a value column
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )


    # 6
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    

    # 7 
    catplot=sns.catplot( #sns.catplot builds the bar chart
        data=df_cat,
        x='variable',
        y='total',
        hue='value', #splits bars into 2 colors 0 or 1
        col='cardio', #splits iinto 2 charts, one for patients with no cardiovascular disease and one for those with it
        kind='bar'
    )


    # 8
    fig = catplot.fig


    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) 
        & (df['height'] >= df['height'].quantile(0.025)) 
        & (df['height'] <= df['height'].quantile(0.975)) 
        & (df['weight'] >= df['weight'].quantile(0.025))
        & (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12
    corr = df_heat.corr() #calculates Pearson correlation coefficient between
    #every numerical column

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))
    #hides redundancy, as the correlation matrix is 2 identical triangles


    # 14
    fig, ax = plt.subplots(figsize=(12,12))

    # 15
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", center=0, vmin=-0.1, vmax=0.25
    cbar_kws={'shrink': .5}, square=True)
    #annot=true and ftm='.1f' print the correlation numbers inside the squares, rounded 
    # to 1 decimal place. vmin and vmac lock the color scale limits
    # so the color gradient remains consistent, mask=mask applies the triangle filter we created in 13

    # 16
    fig.savefig('heatmap.png')
    return fig
