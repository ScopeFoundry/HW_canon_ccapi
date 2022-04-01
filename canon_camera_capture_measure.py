from ScopeFoundry import Measurement
import pyqtgraph as pg
import time

class CanonCCAPICaptureMeasure(Measurement):
    
    name = 'canon_camera_capture'
    
    def setup(self):
        pass
    
    def setup_figure(self):
        # self.ui = self.graph_layout = pg.GraphicsLayoutWidget()
        #
        # self.plot = self.graph_layout.addPlot()
        # self.plot.setAspectLocked(1)
        # self.img_item = pg.ImageItem()
        # self.plot.addItem(self.img_item)
        #
        self.ui = self.imgview = pg.ImageView()
        
    def run(self):
        
        while not self.interrupt_measurement_called:
            time.sleep(0.1)
        
    def update_display(self):
        
        #self.img_item.
        self.imgview.setImage(self.app.hardware.canon_camera.cam.get_live_img().swapaxes(0,1),
                               autoLevels=False)
        self.imgview.setLevels(0,255)