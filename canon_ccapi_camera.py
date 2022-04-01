import requests
import json
import imageio
import time
from urllib.error import HTTPError

class CanonCCAPICamera(object):
    
    def __init__(self, url="http://192.168.1.2:8080/ccapi/ver100"):
        
        self.url = url
        
    def _get_json(self, path,params=None, **kwargs):
        resp = requests.get(f"{self.url}/{path}", params, **kwargs)
        j = resp.json()
        #print(j)
        return j

    def get_device_info(self):
        resp = self._get_json('deviceinformation')
        return resp
        
    def get_aperture_options(self):        
        resp = self._get_json('shooting/settings/av')
        return resp['ability']



    
    def get_iso(self):
        resp = self._get_json('shooting/settings/iso')
        return resp['value']
    
    def get_iso_options(self):
        resp = self._get_json('shooting/settings/iso')
        return resp['ability']
    
    def set_iso(self, iso):
        resp = requests.put(f'{self.url}/shooting/settings/iso', json={"value": str(iso)})
        resp.json()

    def get_exp_time(self):
        resp = self._get_json('shooting/settings/tv')
        return resp['value']
    
    def get_exp_time_options(self):
        resp = self._get_json('shooting/settings/tv')
        return resp['ability']

    def set_exp_time(self, tv):
        resp = requests.put(f'{self.url}/shooting/settings/tv', json={"value": str(tv)})
        resp.json()
    
    
    def get_shooting_settings(self):
        resp = self._get_json('shooting/settings')
        return resp
        
    def get_shootingmode(self):
        resp = self._get_json('shooting/settings/shootingmodedial')
        return resp['value']
    
    def get_colortemp(self):
        resp = self._get_json('shooting/settings/colortemperature')
        # Example resp:
        # {'value': 6000, 'ability': {'min': 2500, 'max': 10000, 'step': 100}}
        return resp['value']
        
    def get_colortemp_options(self):
        resp = self._get_json('shooting/settings/colortemperature')
        # Example resp:
        # {'value': 6000, 'ability': {'min': 2500, 'max': 10000, 'step': 100}}
        x = resp['ability']
        return list(range(x['min'], x['max']+1, x['step']))
    
    def set_colortemp(self, temp):
        resp = requests.put(f'{self.url}/shooting/settings/colortemperature', json={"value": int(temp)})
        resp.json()
    
    def get_whitebalance(self):
        resp = self._get_json('shooting/settings/wb')
        # Example resp:
        # {'value': 'colortemp',
        #  'ability': [...] }
        return resp['value']
    
    def get_whitebalance_options(self):
        resp = self._get_json('shooting/settings/wb')
        # Example resp:
        # {'value': 'colortemp',
        #  'ability': ['auto',
        #   'awbwhite',
        #   'daylight',
        #   'shade',
        #   'cloudy',
        #   'tungsten',
        #   'whitefluorescent',
        #   'flash',
        #   'custom',
        #   'colortemp']}
        return resp['ability']
        
    def set_whitebalance(self, wb):
        resp = requests.put(f'{self.url}/shooting/settings/wb', json={"value": str(wb)})
        resp.json()
    
    
    ## Live View Images
        
    def activate_liveview(self, size='medium', cameradisplay='on'):
        resp = requests.post(f"{self.url}/shooting/liveview",
                     data=json.dumps({'liveviewsize':size,'cameradisplay':cameradisplay}))
        resp        
    
    def get_live_img(self):
        try:
            im = imageio.imread(f"{self.url}/shooting/liveview/flip")
        except HTTPError:
            time.sleep(0.1)
            im = imageio.imread(f"{self.url}/shooting/liveview/flip")

        return im
    
    ### Take photos
    
    def activate_shutter_button(self,af=False):
        resp = requests.post(f'{self.url}/shooting/control/shutterbutton', json={"af": bool(af)})
        print(resp, resp.content)        
    
    #def get_last_img_path(self, storage='sd', type='jpeg'):
        
    # TODO
    ## Set time to computer clock
    ## set image quality and type
    
    def get_event_polling(self):
        return self._get_json('event/polling')
    
    def acquire_img_and_wait(self, af=False,timeout=10.0):
        "blocking image acquisition"
        
        # clear event buffer by polling once
        print(self.get_event_polling())
        # snap!
        self.activate_shutter_button(af)
        time.sleep(0.010)
        t0 = time.monotonic()
        # wait
        while (time.monotonic() - t0) < timeout:
            events = self.get_event_polling()
            #print( time.monotonic() - t0, events )
            time.sleep(0.01)
            if 'addedcontents' in events:
                new_files = events['addedcontents']
                print(new_files, time.monotonic() - t0)
                return new_files
            
    
    def get_save_raw(self):
        resp = self._get_json('shooting/settings/stillimagequality')
        # example response:
        #        {'value': {'raw': 'raw', 'jpeg': 'none'},
        # 'ability': {'raw': ['none', 'raw', 'craw'],
        #  'jpeg': ['none',
        #   'large_fine',
        #   'large_normal',
        #   'medium_fine',
        #   'medium_normal',
        #   'small1_fine',
        #   'small1_normal',
        #   'small2']}}
        return resp['value']['raw']
    
    def get_save_raw_options(self):
        resp = self._get_json('shooting/settings/stillimagequality')
        # example response:
        #        {'value': {'raw': 'raw', 'jpeg': 'none'},
        # 'ability': {'raw': ['none', 'raw', 'craw'],
        #  'jpeg': ['none',
        #   'large_fine',
        #   'large_normal',
        #   'medium_fine',
        #   'medium_normal',
        #   'small1_fine',
        #   'small1_normal',
        #   'small2']}}
        return resp['ability']['raw']
    
    def set_save_raw(self, x):
        # note: options may be different for other cameras
        assert x in ('none', 'raw', 'craw') 
        imqual = self._get_json('shooting/settings/stillimagequality')
        # update value dict
        imqual['value']['raw'] = x
        resp = requests.put(f'{self.url}/shooting/settings/stillimagequality',
                            json=imqual)
        resp.json()
            
    def get_save_jpg(self):
        resp = self._get_json('shooting/settings/stillimagequality')
        # example response:
        #        {'value': {'raw': 'raw', 'jpeg': 'none'},
        # 'ability': {'raw': ['none', 'raw', 'craw'],
        #  'jpeg': ['none',
        #   'large_fine',
        #   'large_normal',
        #   'medium_fine',
        #   'medium_normal',
        #   'small1_fine',
        #   'small1_normal',
        #   'small2']}}
        return resp['value']['jpeg']
    
    def get_save_jpg_options(self):
        resp = self._get_json('shooting/settings/stillimagequality')
        # example response:
        #        {'value': {'raw': 'raw', 'jpeg': 'none'},
        # 'ability': {'raw': ['none', 'raw', 'craw'],
        #  'jpeg': ['none',
        #   'large_fine',
        #   'large_normal',
        #   'medium_fine',
        #   'medium_normal',
        #   'small1_fine',
        #   'small1_normal',
        #   'small2']}}
        return resp['ability']['jpeg']    
    
    def set_save_jpg(self, x):
        imqual = self._get_json('shooting/settings/stillimagequality')
        # update value dict
        imqual['value']['jpeg'] = x
        resp = requests.put(f'{self.url}/shooting/settings/stillimagequality',
                            json=imqual)
        resp.json()
        
    def download_img_url(self, url, filename):
        resp = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(resp.content)
            
    def delete_img_url(self, url):
        requests.delete(url)

        
# shooting/settings:
"""
{'shootingmodedial': {'value': 'm'},
 'av': {'value': '', 'ability': []},
 'tv': {'value': '1/2000',
  'ability': ['bulb',
   '30"',
   '25"',
   '20"',
   '15"',
   '13"',
   '10"',
   '8"',
   '6"',
   '5"',
   '4"',
   '3"2',
   '2"5',
   '2"',
   '1"6',
   '1"3',
   '1"',
   '0"8',
   '0"6',
   '0"5',
   '0"4',
   '0"3',
   '1/4',
   '1/5',
   '1/6',
   '1/8',
   '1/10',
   '1/13',
   '1/15',
   '1/20',
   '1/25',
   '1/30',
   '1/40',
   '1/50',
   '1/60',
   '1/80',
   '1/100',
   '1/125',
   '1/160',
   '1/200',
   '1/250',
   '1/320',
   '1/400',
   '1/500',
   '1/640',
   '1/800',
   '1/1000',
   '1/1250',
   '1/1600',
   '1/2000',
   '1/2500',
   '1/3200',
   '1/4000',
   '1/5000',
   '1/6400',
   '1/8000',
   '1/10000',
   '1/12800',
   '1/16000']},
 'iso': {'value': '100',
  'ability': ['auto',
   '100',
   '125',
   '160',
   '200',
   '250',
   '320',
   '400',
   '500',
   '640',
   '800',
   '1000',
   '1250',
   '1600',
   '2000',
   '2500',
   '3200',
   '4000',
   '5000',
   '6400',
   '8000',
   '10000',
   '12800',
   '16000',
   '20000',
   '25600']},
 'exposure': {'value': '', 'ability': []},
 'wb': {'value': 'colortemp',
  'ability': ['auto',
   'awbwhite',
   'daylight',
   'shade',
   'cloudy',
   'tungsten',
   'whitefluorescent',
   'flash',
   'custom',
   'colortemp']},
 'colortemperature': {'value': 6000,
  'ability': {'min': 2500, 'max': 10000, 'step': 100}},
 'afoperation': {'value': 'manual'},
 'afmethod': {'value': 'face+tracking',
  'ability': ['face+tracking', 'spot', '1point', 'zone']},
 'stillimagequality': {'value': {'raw': 'raw', 'jpeg': 'none'},
  'ability': {'raw': ['none', 'raw', 'craw'],
   'jpeg': ['none',
    'large_fine',
    'large_normal',
    'medium_fine',
    'medium_normal',
    'small1_fine',
    'small1_normal',
    'small2']}},
 'stillimageaspectratio': {'value': '3:2',
  'ability': ['3:2', '4:3', '16:9', '1:1']},
 'flash': {'value': '', 'ability': []},
 'metering': {'value': 'evaluative',
  'ability': ['evaluative', 'partial', 'spot', 'center_weighted_average']},
 'drive': {'value': 'single',
  'ability': ['single', 'self_10sec', 'self_2sec']},
 'aeb': {'value': '', 'ability': []},
 'wbshift': {'value': {'ba': 0, 'mg': 0},
  'ability': {'ba': {'min': -9, 'max': 9, 'step': 1},
   'mg': {'min': -9, 'max': 9, 'step': 1}}},
 'wbbracket': {'value': '0',
  'ability': ['0', 'ba1', 'ba2', 'ba3', 'mg1', 'mg2', 'mg3']},
 'colorspace': {'value': 'srgb', 'ability': ['srgb', 'adobe_rgb']},
 'picturestyle': {'value': 'auto',
  'ability': ['auto',
   'standard',
   'portrait',
   'landscape',
   'finedetail',
   'neutral',
   'faithful',
   'monochrome',
   'userdef1',
   'userdef2',
   'userdef3']},
 'picturestyle_auto': {'value': {'sharpness_strength': 4,
   'sharpness_fineness': 2,
   'sharpness_threshold': 4,
   'contrast': 0,
   'saturation': 0,
   'colortone': 0},
  'ability': {'sharpness_strength': {'min': 0, 'max': 7, 'step': 1},
   'sharpness_fineness': {'min': 1, 'max': 5, 'step': 1},
   'sharpness_threshold': {'min': 1, 'max': 5, 'step': 1},
   'contrast': {'min': -4, 'max': 4, 'step': 1},
   'saturation': {'min': -4, 'max': 4, 'step': 1},
   'colortone': {'min': -4, 'max': 4, 'step': 1}}},
 'picturestyle_standard': {'value': {'sharpness_strength': 4,
   'sharpness_fineness': 2,
   'sharpness_threshold': 4,
   'contrast': 0,
   'saturation': 0,
   'colortone': 0},
  'ability': {'sharpness_strength': {'min': 0, 'max': 7, 'step': 1},
   'sharpness_fineness': {'min': 1, 'max': 5, 'step': 1},
   'sharpness_threshold': {'min': 1, 'max': 5, 'step': 1},
   'contrast': {'min': -4, 'max': 4, 'step': 1},
   'saturation': {'min': -4, 'max': 4, 'step': 1},
   'colortone': {'min': -4, 'max': 4, 'step': 1}}},
 'picturestyle_portrait': {'value': {'sharpness_strength': 3,
   'sharpness_fineness': 2,
   'sharpness_threshold': 4,
   'contrast': 0,
   'saturation': 0,
   'colortone': 0},
  'ability': {'sharpness_strength': {'min': 0, 'max': 7, 'step': 1},
   'sharpness_fineness': {'min': 1, 'max': 5, 'step': 1},
   'sharpness_threshold': {'min': 1, 'max': 5, 'step': 1},
   'contrast': {'min': -4, 'max': 4, 'step': 1},
   'saturation': {'min': -4, 'max': 4, 'step': 1},
   'colortone': {'min': -4, 'max': 4, 'step': 1}}},
 'picturestyle_landscape': {'value': {'sharpness_strength': 5,
   'sharpness_fineness': 2,
   'sharpness_threshold': 4,
   'contrast': 0,
   'saturation': 0,
   'colortone': 0},
  'ability': {'sharpness_strength': {'min': 0, 'max': 7, 'step': 1},
   'sharpness_fineness': {'min': 1, 'max': 5, 'step': 1},
   'sharpness_threshold': {'min': 1, 'max': 5, 'step': 1},
   'contrast': {'min': -4, 'max': 4, 'step': 1},
   'saturation': {'min': -4, 'max': 4, 'step': 1},
   'colortone': {'min': -4, 'max': 4, 'step': 1}}},
 'picturestyle_finedetail': {'value': {'sharpness_strength': 4,
   'sharpness_fineness': 1,
   'sharpness_threshold': 1,
   'contrast': 0,
   'saturation': 0,
   'colortone': 0},
  'ability': {'sharpness_strength': {'min': 0, 'max': 7, 'step': 1},
   'sharpness_fineness': {'min': 1, 'max': 5, 'step': 1},
   'sharpness_threshold': {'min': 1, 'max': 5, 'step': 1},
   'contrast': {'min': -4, 'max': 4, 'step': 1},
   'saturation': {'min': -4, 'max': 4, 'step': 1},
   'colortone': {'min': -4, 'max': 4, 'step': 1}}},
 'picturestyle_neutral': {'value': {'sharpness_strength': 0,
   'sharpness_fineness': 2,
   'sharpness_threshold': 2,
   'contrast': 0,
   'saturation': 0,
   'colortone': 0},
  'ability': {'sharpness_strength': {'min': 0, 'max': 7, 'step': 1},
   'sharpness_fineness': {'min': 1, 'max': 5, 'step': 1},
   'sharpness_threshold': {'min': 1, 'max': 5, 'step': 1},
   'contrast': {'min': -4, 'max': 4, 'step': 1},
   'saturation': {'min': -4, 'max': 4, 'step': 1},
   'colortone': {'min': -4, 'max': 4, 'step': 1}}},
 'picturestyle_faithful': {'value': {'sharpness_strength': 0,
   'sharpness_fineness': 2,
   'sharpness_threshold': 2,
   'contrast': 0,
   'saturation': 0,
   'colortone': 0},
  'ability': {'sharpness_strength': {'min': 0, 'max': 7, 'step': 1},
   'sharpness_fineness': {'min': 1, 'max': 5, 'step': 1},
   'sharpness_threshold': {'min': 1, 'max': 5, 'step': 1},
   'contrast': {'min': -4, 'max': 4, 'step': 1},
   'saturation': {'min': -4, 'max': 4, 'step': 1},
   'colortone': {'min': -4, 'max': 4, 'step': 1}}},
 'picturestyle_monochrome': {'value': {'sharpness_strength': 4,
   'sharpness_fineness': 2,
   'sharpness_threshold': 4,
   'contrast': 0,
   'filtereffect': 'none',
   'toningeffect': 'none'},
  'ability': {'sharpness_strength': {'min': 0, 'max': 7, 'step': 1},
   'sharpness_fineness': {'min': 1, 'max': 5, 'step': 1},
   'sharpness_threshold': {'min': 1, 'max': 5, 'step': 1},
   'contrast': {'min': -4, 'max': 4, 'step': 1},
   'filtereffect': ['none', 'yellow', 'orange', 'red', 'green'],
   'toningeffect': ['none', 'sepia', 'blue', 'purple', 'green']}},
 'picturestyle_userdef1': {'value': {'basepicturestyle': 'auto',
   'sharpness_strength': 4,
   'sharpness_fineness': 2,
   'sharpness_threshold': 4,
   'contrast': 0,
   'saturation': 0,
   'colortone': 0},
  'ability': {'basepicturestyle': [],
   'sharpness_strength': {'min': 0, 'max': 7, 'step': 1},
   'sharpness_fineness': {'min': 1, 'max': 5, 'step': 1},
   'sharpness_threshold': {'min': 1, 'max': 5, 'step': 1},
   'contrast': {'min': -4, 'max': 4, 'step': 1},
   'saturation': {'min': -4, 'max': 4, 'step': 1},
   'colortone': {'min': -4, 'max': 4, 'step': 1}}},
 'picturestyle_userdef2': {'value': {'basepicturestyle': 'auto',
   'sharpness_strength': 4,
   'sharpness_fineness': 2,
   'sharpness_threshold': 4,
   'contrast': 0,
   'saturation': 0,
   'colortone': 0},
  'ability': {'basepicturestyle': [],
   'sharpness_strength': {'min': 0, 'max': 7, 'step': 1},
   'sharpness_fineness': {'min': 1, 'max': 5, 'step': 1},
   'sharpness_threshold': {'min': 1, 'max': 5, 'step': 1},
   'contrast': {'min': -4, 'max': 4, 'step': 1},
   'saturation': {'min': -4, 'max': 4, 'step': 1},
   'colortone': {'min': -4, 'max': 4, 'step': 1}}},
 'picturestyle_userdef3': {'value': {'basepicturestyle': 'auto',
   'sharpness_strength': 4,
   'sharpness_fineness': 2,
   'sharpness_threshold': 4,
   'contrast': 0,
   'saturation': 0,
   'colortone': 0},
  'ability': {'basepicturestyle': [],
   'sharpness_strength': {'min': 0, 'max': 7, 'step': 1},
   'sharpness_fineness': {'min': 1, 'max': 5, 'step': 1},
   'sharpness_threshold': {'min': 1, 'max': 5, 'step': 1},
   'contrast': {'min': -4, 'max': 4, 'step': 1},
   'saturation': {'min': -4, 'max': 4, 'step': 1},
   'colortone': {'min': -4, 'max': 4, 'step': 1}}},
 'picturestyle_userdef1_basepicturestyle': {'value': 'auto',
  'ability': ['auto',
   'standard',
   'portrait',
   'landscape',
   'finedetail',
   'neutral',
   'faithful',
   'monochrome']},
 'picturestyle_userdef2_basepicturestyle': {'value': 'auto',
  'ability': ['auto',
   'standard',
   'portrait',
   'landscape',
   'finedetail',
   'neutral',
   'faithful',
   'monochrome']},
 'picturestyle_userdef3_basepicturestyle': {'value': 'auto',
  'ability': ['auto',
   'standard',
   'portrait',
   'landscape',
   'finedetail',
   'neutral',
   'faithful',
   'monochrome']},
 'moviequality': {'value': '', 'ability': []},
 'soundrecording': {'value': '', 'ability': []},
 'soundrecording_level': {'value': None,
  'ability': {'min': None, 'max': None, 'step': None}},
 'soundrecording_windfilter': {'value': '', 'ability': []},
 'soundrecording_attenuator': {'value': '', 'ability': []}}
 """

if __name__ == '__main__':
    c = CanonCCAPICamera()
    
    c.get_device_info()
    c.activate_liveview()
    
    print(c.get_iso())
    print(c.get_iso_options())
    print(c.get_shooting_settings())
    print(c.get_shootingmode())
    print(c.get_live_img().shape)
    #c.get_aperture_list()