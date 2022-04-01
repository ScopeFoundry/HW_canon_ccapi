from ScopeFoundry.base_app import BaseMicroscopeApp

class CanonCCAPITestApp(BaseMicroscopeApp):
    
    name = 'canon_ccapi_test_app'
    
    def setup(self):
        
        from ScopeFoundryHW.canon_ccapi.canon_ccapi_camera_hw import CanonCCAPICameraHW
        self.add_hardware(CanonCCAPICameraHW(self))
        
        from ScopeFoundryHW.canon_ccapi.canon_camera_capture_measure import CanonCCAPICaptureMeasure
        self.add_measurement(CanonCCAPICaptureMeasure(self))
        
    
if __name__ == '__main__':
    import sys
    app = CanonCCAPITestApp(sys.argv)
    app.exec_()