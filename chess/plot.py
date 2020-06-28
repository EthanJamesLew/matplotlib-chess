""" Plot and Interact with Chess Board
Ethan Lew
elew@pdx.edu
"""
import os
import string
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

highlight_patches = []
patch_count =0

def get_image(name, color):
    """given a piece name and a color, get sprite image"""
    script_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(script_path, 'img','chess_pieces_large.png')
    base_width = int(1000/6.0)
    order = ['king', 'queen', 'bishop', 'knight', 'rook', 'pawn']
    ycrop = int(order.index(name)*base_width)
    xcrop = int(int(not color) * base_width)
    img = plt.imread(path)
    return OffsetImage(img[xcrop:(xcrop+base_width), ycrop:(ycrop+base_width), :], zoom=0.25, zorder=1000)


def enter_board(event, tile_size=10, size=8, direction=True, chess_board=None, ax=None, fig=None):
    global highlight_patches
    [p.remove() for p in highlight_patches]
    highlight_patches =[]
    plt.draw()
    if event.xdata is None or event.ydata is None:
       return
    posx = int(event.xdata//tile_size)
    posy = int(event.ydata//tile_size)
    if not direction:
        posx, posy = size - posx - 1, size - posy - 1
    moves = chess_board.get_moves((posx, posy))
    patch_count = 0
    for xidx, yidx in moves:
        if not direction:
            xidx, yidx = size-xidx-1, size-yidx-1
        highlight_patches.append(patches.Rectangle(((xidx)*tile_size,yidx*tile_size),tile_size,tile_size,
                                       linewidth=1,edgecolor='k',facecolor='y', alpha=0.5, zorder=100))
        ax.add_patch(highlight_patches[-1])
        patch_count += 1
        fig.canvas.draw()


def plot_chess_board(chess_board, direction=True, highlight_moves=[]):
    """plot state of chess board"""

    size = chess_board.board_size
    tile_size = 10
    fig, ax = plt.subplots()

    # plot tiles
    for yidx in range(size):
        for xidx in range(0, size, 2):
            stagger = 0 if yidx % 2 == 0 else 1
            ax.add_patch(patches.Rectangle(((stagger+xidx)*tile_size,yidx*tile_size),tile_size,tile_size,
                                           linewidth=1,edgecolor='k',facecolor='k', alpha=0.5))

    # plot edges
    ax.plot([0, size*tile_size], [0, 0], 'k')
    ax.plot([0, size*tile_size], [size*tile_size, size*tile_size], 'k')
    ax.plot([0, 0], [0, size*tile_size], 'k')
    ax.plot([size*tile_size, size*tile_size], [0, size*tile_size], 'k')
    plt.axis('equal')
    plt.axis('off')

    # plot chess coordinate label
    for idx in range(size):
        xname = string.ascii_uppercase[idx] if direction else string.ascii_uppercase[size-idx-1]
        yname = str(idx+1) if direction else str(size-idx)
        ax.text(-tile_size/2, (idx+0.25)*tile_size, yname, fontsize=tile_size*1.5)
        ax.text((idx+0.25)*tile_size, -tile_size/2, xname, fontsize=tile_size*1.5)

    #for m in highlight_moves:
    #    moves = chess_board.get_moves(m)
    #    for xidx, yidx in moves:
    #        if not direction:
    #            xidx, yidx = size-xidx-1, size-yidx-1
    #        ax.add_patch(patches.Rectangle(((xidx)*tile_size,yidx*tile_size),tile_size,tile_size,
    #                                       linewidth=1,edgecolor='y',facecolor='y', alpha=0.5))
    # plot pieces
    for pos in chess_board.positions:
        name, color = chess_board._positions[pos]
        if direction:
            coor = (0.5+pos[0])*tile_size, (0.5+pos[1])*tile_size
        else:
            coor = (0.5+size-pos[0]-1)*tile_size, (0.5+size-pos[1]-1)*tile_size
        ab = AnnotationBbox(get_image(name.lower(), color),
                        coor,
                        frameon=False)
        ab.set_zorder(500)
        ax.add_artist(ab)

    fig.canvas.mpl_connect('motion_notify_event', lambda e: enter_board(e, size=size, tile_size=tile_size, chess_board=chess_board, ax=ax, fig=fig))
    return fig, ax