import numpy as np
import matplotlib.pyplot as plt
import torch

def transform(y, nz):
    model_true = torch.ones(nz, 1)    
    for i, v in enumerate(y):
        model_true[40*i:40*(i+1), :] = v.item()
        
    return model_true

def plot_amplitudes_grid(amplitudes, nt, nrec):
    fig, axarr = plt.subplots(5, 5, figsize=(12, 12))
    for ax, x in zip(axarr.flatten(), amplitudes.cpu().numpy()[::5]):   
        vmin, vmax = np.percentile(x, [1, 99])
        ax.imshow(x.reshape(nt, nrec), aspect='auto', vmin=vmin, vmax=vmax)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
    return axarr

def plot_velocity_profiles_grid(y, y_, nz):
    fig, axarr = plt.subplots(5, 5, figsize=(12, 12))
    for ax, y, y_ in zip(axarr.flatten(), y.cpu().numpy()[::5], y_.cpu().numpy()[::5]):   
        ax.plot(transform(y, nz).numpy(), color="black")
        ax.plot(transform(y_, nz).numpy(), color="red")
        ax.set_ylim(0.25, 1.0)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
    return axarr

def plot_velocity_profile_grid(y, nz):
    fig, axarr = plt.subplots(5, 5, figsize=(12, 12))
    for ax, y in zip(axarr.flatten(), y.cpu().numpy()):   
        ax.plot(transform(y, nz).numpy(), color="black")
        ax.set_ylim(0.25, 1.1)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
    return axarr

def plot_velocity_models(ax, models, colors=["blue", "black", "beige"], legend="Data", alpha=0.5):
    dev = models[:, :, 0].std(0).numpy()
    mean = models[:, :, 0].mean(0).numpy()
    sc = ax.plot(mean, color=colors[0], label=legend)
    upper = ax.plot(mean+dev, linestyle="--", color=colors[1])
    lower = ax.plot(mean-dev, linestyle="--", color=colors[1])
    sc2 = ax.fill_between(range(mean.shape[0]), mean-dev, mean+dev, alpha=alpha, color=colors[2])
    for curve in models[:, :, 0].numpy():
        ax.plot(range(len(curve)), curve, color=colors[0], alpha=0.01)

def plot_losses(ax, losses):
    ax.plot(losses[:, 0], color="black", label="Train")
    ax.plot(losses[:, 1], color="red", label="Test")


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def store_model_checkpoint(path, epoch, model, optimizer, loss):
    torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
            }, path)
    return True

def load_model_checkpoint(path, model, optimizer):
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    epoch = checkpoint['epoch']
    loss = checkpoint['loss']
    return model, optimizer, epoch, loss

def plot_losses_vs_noise(ax, mean_correls, out_losses):
    ax.plot(1-np.array(mean_correls)**2, out_losses, color="black")
    ax.set_xlim(0, 1.0)
    ax.axvline(0.5, label="50% Noise Cutoff", linestyle="--", color="red")
    ax.set_ylabel("Mean Squared Error - Interval Velocities", fontsize=24)
    ax.set_xlabel("Percentage of Noise in Input", fontsize=24)

def plot_wiggle_traces(fig, xample, n_recorders):
    for i in range(1, n_recorders):
        ax = fig.add_subplot(n_recorders, 1, i)
        ax.plot(xample[:, -i], color="black")
        if i != n_recorders-1:
            ax.set_axis_off()
        else:
            ax.axes.get_yaxis().set_visible(False)
            ax.set_frame_on(False)
            ax.set_xlabel("Time [10 ms]", fontsize=20)
