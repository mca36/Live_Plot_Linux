from PyQt5 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg
import numpy as np
x = np.random.normal(size=1000)
y = np.random.normal(size=1000)
pg.plot(x, y, pen=None, symbol='o')
