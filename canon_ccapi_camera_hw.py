from ScopeFoundry import HardwareComponent
from .canon_ccapi_camera import CanonCCAPICamera

class CanonCCAPICameraHW(HardwareComponent):

    name = 'canon_camera'
    
    def setup(self):
        
        self.settings.New("url", dtype=str, initial = "http://192.168.1.2:8080/ccapi/ver100" )
        self.settings.New('iso', dtype=str, initial = '0', choices=('0'))
        self.settings.New('exp_time', dtype=str, initial = '0', choices=('0'))
        self.settings.New('color_temp', dtype=int, initial=0, choices=(0,))
        self.settings.New('save_raw', dtype=str, initial = '?', choices=('?'))
        self.settings.New('save_jpg', dtype=str, initial = '?', choices=('?'))
    
    def connect(self):
        
        self.cam = CanonCCAPICamera(url=self.settings['url'])
        
        self.settings.iso.change_choice_list(self.cam.get_iso_options())
        self.settings.iso.connect_to_hardware(
            read_func=self.cam.get_iso,
            write_func=self.cam.set_iso)
        
        self.settings.exp_time.change_choice_list(self.cam.get_exp_time_options())
        self.settings.exp_time.connect_to_hardware(
            read_func=self.cam.get_exp_time,
            write_func=self.cam.set_exp_time)
        
        self.settings.color_temp.change_choice_list(self.cam.get_colortemp_options())
        self.settings.color_temp.connect_to_hardware(
            read_func=self.cam.get_colortemp,
            write_func=self.cam.set_colortemp)      
        
        self.settings.save_raw.change_choice_list(self.cam.get_save_raw_options())
        self.settings.save_raw.connect_to_hardware(
            read_func=self.cam.get_save_raw,
            write_func=self.cam.set_save_raw)      

        self.settings.save_jpg.change_choice_list(self.cam.get_save_jpg_options())        
        self.settings.save_jpg.connect_to_hardware(
            read_func=self.cam.get_save_jpg,
            write_func=self.cam.set_save_jpg)      

        
        self.read_from_hardware()  
        
        
    def disconnect(self):
        self.settings.disconnect_all_from_hardware()
        
        if hasattr(self, 'cam'):
            del self.cam
        
