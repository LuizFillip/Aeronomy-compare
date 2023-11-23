import events as ev

args = dict(
    capsize = 3,
    marker = 's'
    )
 
def plot_hist(ax):
    
    return ax
    
def plot_distribution(
        ax, 
        df, 
        limits,
        col = 'gamma',
        label = '', 
        count = True,
        drop = 2
        ):

    ds = ev.probability_distribuition(
        df,
        limits,
        col = col
        )
    
    epbs = ds['epbs'].sum()
    
    ds = ds.loc[~(
        (ds['days'] == 1) & 
        (ds['epbs'] == 1))
        ]
        
    ax1 = ax.twinx()
    
    ds['mean'].plot(
        kind = 'hist', 
        bins = np.arange(0, 3.2, 0.2),
        ax  = ax1, 
        color = 'gray',
        alpha = 0.3
        )
    if drop is not None:
        ds.drop(
            ds.tail(drop).index, 
            inplace = True
            )
    
    if count:
        LABEL = f'{label} ({epbs} events)'
    else:
        LABEL = label
    
    ax.errorbar(
        ds['mean'], 
        ds['rate'], 
        xerr = ds['std'],
        yerr = ds['epb_error'],
        label = LABEL,
        **args
        )
    

    for bar in [0, 1]:
        ax.axhline(
            bar, 
            linestyle = ":", 
            lw = 2, 
            color = "k"
            )
        
    return epbs 



