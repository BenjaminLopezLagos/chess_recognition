from PySide6.QtSvg import *
from PySide6.QtGui import *


def convertSvgToPng(svgFilepath,pngFilepath,width):
    r=QSvgRenderer(svgFilepath)
    height=r.defaultSize().height()*width/r.defaultSize().width()
    i=QImage(width,height,QImage.Format_ARGB32)
    p=QPainter(i)
    r.render(p)
    i.save(pngFilepath)
    p.end()

convertSvgToPng(svgFilepath='out2.svg', pngFilepath='test.png', width=1000)