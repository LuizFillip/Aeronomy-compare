import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import datetime as dt 
from matplotlib.gridspec import GridSpec
from plotting import plot_terminator_and_equator, plot_corners
import base as b
import PlasmaBubbles as pb 
import os 
import numpy as np 

def multi_layout(nrows = 4, year = 2014):
    
    fig = plt.figure(dpi = 300, figsize=(18, 7))
    
    gs = GridSpec(nrows, 8)
    
    plt.subplots_adjust(wspace= 0.2, hspace = 0)
    
    ax_map = fig.add_subplot(
        gs[:, :nrows], 
        projection=ccrs.PlateCarree()
        )
    
    gg.map_attrs(ax_map, year, grid = False)
    
    # Regular plots on the right
    ax1 = fig.add_subplot(gs[0, nrows:])
    args = dict(sharey = ax1)
    
    ax2 = fig.add_subplot(gs[1, nrows:], **args)
    ax3 = fig.add_subplot(gs[2, nrows:], **args)
    ax4 = fig.add_subplot(gs[3, nrows:], **args)
    axes = [ax1, ax2, ax3, ax4]
    
    fig.text()
    
    return fig, ax_map, axes


def plot_ipp_on_map(
        ax_map, 
        df, dn, 
        corners
        ):
    
    ds = b.sel_df(df, dn)
        
    for i, key in enumerate(corners.keys()):
        
        xlim, ylim = corners[key]
        
        sel = ds.loc[
            (ds.lon > xlim[0]) & 
            (ds.lon < xlim[1]) & 
            (ds.lat > ylim[0]) & 
            (ds.lat < ylim[1])
            ]
        
        ax_map.scatter(
            sel.lon,
            sel.lat, 
            c = sel.roti, 
            s =  50, 
            vmin = 0, 
            vmax = 2,
            cmap = 'jet'
            )
                
def plot_roti_timeseries(
        axes, 
        df, dn, 
        corners, 
        local_term
        ):
    
    key = list(corners.keys())
    
    for i, ax in enumerate(axes):
        
        k = key[i]
        xlim, ylim = corners[k]
        llon, llat = local_term[k]
        
        dusk = gg.dusk_time(
                dn,  
                lat = llat, 
                lon = llon, 
                twilight = 18
                )
        
        ax.axvline(dusk, lw = 2)
        
        midnight = gg.local_midnight(llon, llat, dn)
        
        ax.axvline(midnight, lw = 2, color = 'b')
        
        sel = df.loc[
            (df.index < dn) & 
            (df.lon > xlim[0]) & 
            (df.lon < xlim[1]) & 
            (df.lat > ylim[0]) & 
            (df.lat < ylim[1])
            ]
        
        ax.text(
            0.03, 0.75,
            f'Box {i + 1}', 
            transform = ax.transAxes
            )
    
        ax.scatter(sel.index, sel.roti, 
                   s = 3, color = 'k')
        ax.set(
            ylim = [0, 2], 
            yticks = np.arange(0, 2, 0.5),
            xlim = [df.index[0], df.index[-1]]
            )
        ax.tick_params(
            axis='y', 
            labelright = True, 
            labelleft = False, 
            right = True, 
            left = False)
        
        if i == 0:
            ax.set(xticklabels = [])
            
        
    b.format_time_axes(axes[-1])

def first_entrance_of_terminator(
        ax_map, 
        corners, 
        eq_lon, 
        eq_lat
        ):
    out = {}
    for key in corners.keys():
        xlim, ylim = corners[key]
        ilon, ilat = gg.intersection(
            eq_lon, eq_lat, [xlim[1], xlim[1]], ylim)
        out[key] = (ilon, ilat) 
        ax_map.scatter(ilon, ilat)
        
    return out

def plot_ipp_variation(df, dn):
    
    fig, ax_map, axes = multi_layout(
        nrows = 4, year = dn.year)
    
   
    eq_lon, eq_lat = plot_terminator_and_equator(
            ax_map, dn, twilight = 18)
    
    corners = plot_corners(
            ax_map,
            start.year,
            radius = 10,
            label = True
            )
    
    local_term = first_entrance_of_terminator(
            ax_map, 
            corners, 
            eq_lon, 
            eq_lat
            )
    
    plot_roti_timeseries(axes, df, dn, corners, local_term)
    
    plot_ipp_on_map(ax_map, df, dn, corners)
        
    fig.suptitle(dn.strftime('%H:%M (UT)'))
    
    return fig
    
def range_time(start, mi):
    
    delta = dt.timedelta(minutes = mi)
    
    return start + delta

def save_intervals(df, start):
    
    for minute in range(0, 721):
        
        plt.ioff()
        fig = plot_ipp_variation(
            df, range_time(start, minute)
            )
        name = dn.strftime('%Y%m%d%H%M')
        print(name)
        fig.savefig(f'temp1/{name}')
            
        plt.clf()   
        plt.close()
        
        
start = dt.datetime(2014, 1, 1, 21)

df =  pb.concat_files(
    start, 
    pb.load_filter, 
    root = os.getcwd()
    )

df = b.sel_times(df, start)
        
dn = range_time(start, 10)

fig = plot_ipp_variation(df, dn)