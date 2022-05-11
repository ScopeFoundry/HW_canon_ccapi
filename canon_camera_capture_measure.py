from ScopeFoundry import Measurement
import pyqtgraph as pg
import time
from ScopeFoundry import h5_io

class CanonCCAPICaptureMeasure(Measurement):
    
    name = 'canon_camera_capture'
    
    def setup(self):
        self.add_operation('Snap', self.snap_and_save)
    
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
        
    def snap_and_save(self):
        cam = self.app.hardware['canon_camera']
        live_img = cam.cam.get_live_img()


        try:
            self.h5_file = h5_io.h5_base_file(self.app, measurement=self)
            self.h5_filename = self.h5_file.filename
            self.h5_m = h5_io.h5_create_measurement_group(measurement=self, h5group=self.h5_file)

            new_files = cam.cam.acquire_img_and_wait()
            
        
            print (new_files)
            for f in new_files:
                ext = f.split('.')[-1]
                self.last_img_path = self.h5_filename + f".{ext}"
                print("downloading", f, "to", self.last_img_path)
                cam.cam.download_img_url( f, self.last_img_path )
                print("deleting", f)
                cam.cam.delete_img_url(f)        
            
            self.h5_m['live_img'] = live_img
            self.h5_m['img_path'] = self.last_img_path

        finally:
            self.h5_file.close()