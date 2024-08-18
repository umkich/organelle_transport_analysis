import matplotlib.pyplot as plt
import numpy as np
from sklearn.mixture import GaussianMixture

def draw_tracks(kymo, name, worms_count, kymographs_count, tracks_count, save_name=""):
    figure, ax = plt.subplots(figsize=(7, 4))
    for track in kymo.keys():
        plt.plot(np.array(kymo[track]['y'])-np.array(kymo[track]['y'])[0],np.array(kymo[track]['x'])-np.array(kymo[track]['x'])[0])
    plt.xlim([0, 79])
    plt.ylim([-55, 33])
    plt.xlabel('Track duration (s)')
    plt.ylabel('Distance (\u03bcm)')
    plt.title(name)
    textstr = '\n'.join((
    '{}{}'.format(worms_count, ' worms'),
    '{}{}'.format(kymographs_count, ' kymographs'),
    '{}{}'.format(tracks_count, ' tracks')))
    props = dict(boxstyle='round', facecolor='purple', alpha=0.3)
    # place a text box in upper left in axes coords
    ax.text(0.75, 0.03, textstr, transform=ax.transAxes, fontsize=10,verticalalignment='bottom', bbox=props)

    if save_name != "":
        plt.savefig(save_name,dpi=300)

    plt.show()

def draw_tracks_segment(kymo, name, segment):
    for track in kymo.keys():
        segment.plot(np.array(kymo[track]['y'])-np.array(kymo[track]['y'])[0],np.array(kymo[track]['x'])-np.array(kymo[track]['x'])[0])
    segment.set_title(name)

def draw_all_segments_with_rest(index, directions, kymo, save_name=""):
    name_color_dict = {'right': 'r', 'left': 'g', 'stat': 'b'}
    
    plt.plot(kymo[index]['x'], kymo[index]['y'],'y')
    
    for key in name_color_dict.keys():
        for track in directions[key][index]:
            plt.plot(track['x'], track['y'],name_color_dict[key])
            
    track_y_0 = kymo[index]['y'][0]
    track_y_last = kymo[index]['y'][len(kymo[index]['y']) - 1]
    
    for segment in directions['stat'][index]:
        if len(directions['left'][index]) != 0 or len(directions['right'][index]) != 0:
            segment_y_0 = segment['y'][0]
            segment_y_last = segment['y'][len(segment['y']) - 1]
            
            if segment_y_0 != track_y_0 and segment_y_last != track_y_last:
                plt.plot(segment['x'], segment['y'], 'm') 

    if save_name != "":
        plt.savefig(save_name,dpi=300)
    plt.show()

def GMM_best_fit(velocity):
    X = np.concatenate([velocity]).reshape(-1, 1)

    # fit models with 1-10 components
    N = np.arange(1, 6)
    models = [None for i in range(len(N))]

    for i in range(len(N)):
        models[i] = GaussianMixture(N[i]).fit(X)

    # compute the AIC and the BIC
    AIC = [m.aic(X) for m in models]
    BIC = [m.bic(X) for m in models]

    fig = plt.figure(figsize=(16, 10))
    fig.subplots_adjust(left=0.12, right=0.97,
                        bottom=0.21, top=0.9, wspace=0.5)


    # plot 1: data + best-fit mixture
    ax = fig.add_subplot(121)
    M_best = models[np.argmin(BIC)]

    x = np.linspace(-6, 6, 1000)
    logprob = M_best.score_samples(x.reshape(-1, 1))
    responsibilities = M_best.predict_proba(x.reshape(-1, 1))
    pdf = np.exp(logprob)
    pdf_individual = responsibilities * pdf[:, np.newaxis]

    ax.hist(X, 30, density=True, histtype='stepfilled', alpha=0.4)
    ax.plot(x, pdf, '-k')
    ax.plot(x, pdf_individual, '--k')
    ax.text(0.04, 0.96, "Best-fit Mixture",
            ha='left', va='top', transform=ax.transAxes)
    ax.set_xlabel('$Velocity (\u03bcm/s)$')
    ax.set_ylabel('$Frequency$')


    # plot 2: AIC and BIC
    ax = fig.add_subplot(122)
    ax.plot(N, AIC, '-k', label='AIC')
    ax.plot(N, BIC, '--k', label='BIC')
    ax.set_xlabel('n. components')
    ax.set_ylabel('information criterion')
    ax.legend(loc=2)

    plt.show()