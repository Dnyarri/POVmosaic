#!/usr/bin/env python3

"""
POV-Ray Mosaic - Program for conversion of image into mosaic of solid 3D objects in POV-Ray format
---

Created by: `Ilya Razmanov <mailto:ilyarazmanov@gmail.com>`_ aka `Ilyich the Toad <mailto:amphisoft@gmail.com>`_.

History:
---

1.14.1.0    Single task standalone programs 63zaika, 44zaika and 36zaika replaced with common GUI and zaika63, zaika44 and zaika36 modules correspondingly. Apparently PNM input support added with PyPNM; PNG support reworked to more common.

---
Main site: `The Toad's Slimy Mudhole <https://dnyarri.github.io>`_

Git repositories:
`Main at Github <https://github.com/Dnyarri/POVmosaic>`_; `Gitflic mirror <https://gitflic.ru/project/dnyarri/povmosaic>`_

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '1.15.01.10'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import random
from pathlib import Path
from tkinter import Button, Frame, Label, PhotoImage, Tk, filedialog

from povzaika import zaika36, zaika44, zaika63
from pypng import pnglpng
from pypnm import pnmlpnm


def DisMiss():
    """Kill dialog and continue"""

    sortir.destroy()


def UINormal():
    """Normal UI state, buttons enabled"""
    for widget in frame_left.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='normal')
    info_string.config(text=info_normal['txt'], foreground=info_normal['fg'], background=info_normal['bg'])


def UIBusy():
    """Busy UI state, buttons disabled"""
    for widget in frame_left.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='disabled')
    info_string.config(text=info_busy['txt'], foreground=info_busy['fg'], background=info_busy['bg'])
    sortir.update()


def GetSource():
    """Opening source image and redefining other controls state"""

    global zoom_factor, sourcefilename, preview, preview_data  # some have to be globals for preview to work
    global maxcolors, image3D  # will be reused by export functions
    zoom_factor = 1
    sourcefilename = filedialog.askopenfilename(title='Open image file', filetypes=[('Supported formats', '.png .ppm .pgm .pbm'), ('PNG', '.png'), ('PNM', '.ppm .pgm .pbm')])
    if sourcefilename == '':
        return

    """ ┌───────────────────────────────────────┐
        │ Loading file, converting data to list │
        │ NOTE: maxcolors, image3D are GLOBALS! │
        └───────────────────────────────────────┘ """

    if Path(sourcefilename).suffix == '.png':
        # Reading image as list
        X, Y, Z, maxcolors, image3D, info = pnglpng.png2list(sourcefilename)

    elif Path(sourcefilename).suffix in ('.ppm', '.pgm', '.pbm'):
        # Reading image as list
        X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(sourcefilename)

    else:
        raise ValueError('Extension not recognized')

    """ ┌─────────────────────────────────────────────────────────────────────────┐
        │ Converting list to bytes of PPM-like structure "preview_data" in memory │
        └─────────────────────────────────────────────────────────────────────────┘ """
    preview_data = pnmlpnm.list2bin(image3D, maxcolors, True)

    """ ┌────────────────────────────────────────────────┐
        │ Now showing "preview_data" bytes using Tkinter │
        └────────────────────────────────────────────────┘ """
    preview = PhotoImage(data=preview_data)
    preview = preview.zoom(zoom_factor, zoom_factor)  # "zoom" zooms in, "subsample" zooms out
    zanyato.config(text='Source', image=preview, compound='top')

    """ ┌──────────────────────────┐
        │ Updating controls status │
        └──────────────────────────┘ """
    label_zoom.config(state='normal')
    butt_plus.config(state='normal', cursor='hand2')
    # updating zoom factor display
    label_zoom.config(text=f'Zoom {zoom_factor}:1')
    # updating "Export..." status
    butt02.config(state='normal', cursor='hand2')
    butt03.config(state='normal', cursor='hand2')
    butt04.config(state='normal', cursor='hand2')


def SaveAs63():
    """Once pressed on Export 63"""
    # Open "Save as..." file
    savefilename = filedialog.asksaveasfilename(
        title='Save POV-Ray file',
        filetypes=[
            ('POV-Ray file', '.pov'),
            ('All Files', '*.*'),
        ],
        defaultextension=('POV-Ray scene file', '.pov'),
    )
    if savefilename == '':
        return

    """ ┌─────────────────────────────────────────────────────┐
        │ Converting list to POV and saving as "savefilename" │
        │ using global maxcolors, image3D                     │
        └─────────────────────────────────────────────────────┘ """

    UIBusy()

    zaika63.zaika63(image3D, maxcolors, savefilename)

    UINormal()


def SaveAs44():
    """Once pressed on Export 44"""
    # Open "Save as..." file
    savefilename = filedialog.asksaveasfilename(
        title='Save POV-Ray file',
        filetypes=[
            ('POV-Ray file', '.pov'),
            ('All Files', '*.*'),
        ],
        defaultextension=('POV-Ray scene file', '.pov'),
    )
    if savefilename == '':
        return

    """ ┌─────────────────────────────────────────────────────┐
        │ Converting list to POV and saving as "savefilename" │
        │ using global maxcolors, image3D                     │
        └─────────────────────────────────────────────────────┘ """

    UIBusy()

    zaika44.zaika44(image3D, maxcolors, savefilename)

    UINormal()


def SaveAs36():
    """Once pressed on Export 36"""
    # Open "Save as..." file
    savefilename = filedialog.asksaveasfilename(
        title='Save POV-Ray file',
        filetypes=[
            ('POV-Ray file', '.pov'),
            ('All Files', '*.*'),
        ],
        defaultextension=('POV-Ray scene file', '.pov'),
    )
    if savefilename == '':
        return

    """ ┌─────────────────────────────────────────────────────┐
        │ Converting list to POV and saving as "savefilename" │
        │ using global maxcolors, image3D                     │
        └─────────────────────────────────────────────────────┘ """

    UIBusy()

    zaika36.zaika36(image3D, maxcolors, savefilename)

    UINormal()


def zoomIn():
    """Zoom +"""
    global zoom_factor, preview
    zoom_factor = min(zoom_factor + 1, 3)  # max zoom 3
    preview = PhotoImage(data=preview_data)
    preview = preview.zoom(zoom_factor, zoom_factor)
    zanyato.config(text='Source', image=preview, compound='top')
    # updating zoom factor display
    label_zoom.config(text=f'Zoom {zoom_factor}:1')
    # reenabling +/- buttons
    butt_minus.config(state='normal', cursor='hand2')
    if zoom_factor == 3:  # max zoom 3
        butt_plus.config(state='disabled', cursor='arrow')
    else:
        butt_plus.config(state='normal', cursor='hand2')


def zoomOut():
    """Zoom -"""
    global zoom_factor, preview
    zoom_factor = max(zoom_factor - 1, 1)  # min zoom 1
    preview = PhotoImage(data=preview_data)
    preview = preview.zoom(zoom_factor, zoom_factor)
    zanyato.config(text='Source', image=preview, compound='top')
    # updating zoom factor display
    label_zoom.config(text=f'Zoom {zoom_factor}:1')
    # reenabling +/- buttons
    butt_plus.config(state='normal', cursor='hand2')
    if zoom_factor == 1:  # min zoom 1
        butt_minus.config(state='disabled', cursor='arrow')
    else:
        butt_minus.config(state='normal', cursor='hand2')


""" ╔═══════════╗
    ║ Main body ║
    ╚═══════════╝ """

sortir = Tk()

zoom_factor = 1
sortir.iconphoto(True, PhotoImage(data='P6\n2 8\n255\n'.encode(encoding='ascii') + random.randbytes(2 * 8 * 3)))

sortir.title('POV-Ray Mosaic')
sortir.geometry('+200+100')
sortir.minsize(300, 280)

# Info statuses dictionaries
info_normal = {'txt': f'POV-Ray Mosaic {__version__}', 'fg': 'grey', 'bg': 'light grey'}
info_busy = {'txt': 'BUSY, PLEASE WAIT', 'fg': 'red', 'bg': 'yellow'}

info_string = Label(sortir, text=info_normal['txt'], font=('courier', 8), foreground=info_normal['fg'], background=info_normal['bg'], relief='groove')
info_string.pack(side='bottom', padx=0, pady=1, fill='both')

frame_left = Frame(sortir, borderwidth=2, relief='groove')
frame_left.pack(side='left', anchor='nw')
frame_right = Frame(sortir, borderwidth=2, relief='groove')
frame_right.pack(side='right', anchor='nw')

butt01 = Button(frame_left, text='Open image...'.center(30, ' '), font=('helvetica', 14), cursor='hand2', justify='center', command=GetSource)
butt01.pack(side='top', padx=4, pady=[4, 12], fill='both')

butt02 = Button(frame_left, text='Export 6/3 mosaic\n(honeycomb)...', font=('helvetica', 14), cursor='arrow', justify='center', state='disabled', command=SaveAs63)
butt02.pack(side='top', padx=4, pady=2, fill='both')

butt03 = Button(frame_left, text='Export 4/4 mosaic\n(square)...', font=('helvetica', 14), cursor='arrow', justify='center', state='disabled', command=SaveAs44)
butt03.pack(side='top', padx=4, pady=2, fill='both')

butt04 = Button(frame_left, text='Export 3/6 mosaic\n(triangle)...', font=('helvetica', 14), cursor='arrow', justify='center', state='disabled', command=SaveAs36)
butt04.pack(side='top', padx=4, pady=2, fill='both')

butt99 = Button(frame_left, text='Exit', font=('helvetica', 14), cursor='hand2', justify='center', command=DisMiss)
butt99.pack(side='bottom', padx=4, pady=[24, 4], fill='both')

zanyato = Label(frame_right, text='Preview area', font=('helvetica', 10), justify='center', borderwidth=2, relief='groove')
zanyato.pack(side='top')

frame_zoom = Frame(frame_right, width=300, borderwidth=2, relief='groove')
frame_zoom.pack(side='bottom')

butt_plus = Button(frame_zoom, text='+', font=('courier', 8), width=2, cursor='arrow', justify='center', state='disabled', command=zoomIn)
butt_plus.pack(side='left', padx=0, pady=0, fill='both')

butt_minus = Button(frame_zoom, text='-', font=('courier', 8), width=2, cursor='arrow', justify='center', state='disabled', command=zoomOut)
butt_minus.pack(side='right', padx=0, pady=0, fill='both')

label_zoom = Label(frame_zoom, text=f'Zoom {zoom_factor}:1', font=('courier', 8), state='disabled')
label_zoom.pack(side='left', anchor='n', padx=2, pady=0, fill='both')

sortir.mainloop()
