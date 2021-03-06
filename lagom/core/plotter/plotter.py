import numpy as np

import seaborn as sns

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator  # Useful for integer axis


class Plotter(object):
    def __init__(self):
        self.data = []
        
        # Call heatmap from Seaborn
        self.heatmap = sns.heatmap
        
    def add_curve(self, 
                  data, 
                  color, 
                  label, 
                  uncertainty=False, 
                  scales=None, 
                  alphas=None):
        D = {}
        D['data'] = np.array(data)  # DType: numpy array
        D['color'] = color
        D['label'] = label
        D['uncertainty'] = uncertainty
        D['scales'] = scales
        D['alphas'] = alphas
        
        self.data.append(D)
    
    def plot(self, 
             title, 
             xlabel, 
             ylabel, 
             xlim=None, 
             ylim=None, 
             log_x=False, 
             log_y=False, 
             integer_x=False, 
             integer_y=False):
        # Create a figure
        fig, ax = plt.subplots(1, 1, figsize=[6, 4])
        
        for D in self.data:
            # Unpack data
            data = D['data']
            
            mu = np.mean(data, axis=0)
            sigma = np.std(data, axis=0)
            
            # Plot the curve
            ax.plot(range(1, mu.shape[0]+1), mu, color=D['color'], label=D['label'])
            # Plot uncertainty with shaded area
            if D['uncertainty']:
                self._plot_uncertainty(ax, mu, sigma, D['scales'], D['alphas'], D['color'])
        
        ax.legend()
        
        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)
        
        if log_x:
            ax.set_xscale('log')
        if log_y:
            ax.set_yscale('log')
            
        if integer_x:
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        if integer_y:
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        # Adjust subplots to avoid label overlapping
        fig.tight_layout()
        return fig
    
    def _plot_uncertainty(self, ax, mu, sigma, scales, alphas, facecolor):
        num_points = mu.shape[0]
        for scale, alpha in zip(scales, alphas):
            ax.fill_between(range(1, num_points+1), 
                            mu - scale*sigma, 
                            mu + scale*sigma,
                            facecolor=facecolor, 
                            alpha=alpha)
