from pypylon import pylon
import cv2

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
camera.PixelFormat = "RGB8"
camera.BslColorSpaceMode.SetValue("sRGB")
camera.SensorShutterMode.SetValue("Rolling")
camera.GainAuto.SetValue("Off")
camera.ExposureAuto.SetValue("Off")
camera.BalanceWhiteAuto.SetValue("Off")
camera.BslContrastMode.SetValue("Linear")
camera.MaxNumBuffer = 500
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

class BaslerdaA250014uc:
    def originSetting(self):
        '''
        The original Basler preset
        :return: None
        '''
        camera.Gain.SetValue(1)
        camera.BlackLevel.SetValue(0)
        camera.Gamma.SetValue(1)
        camera.ExposureTime.SetValue(1246)
        camera.BalanceRatioSelector.SetValue("Red")
        camera.BalanceRatio.SetValue(1.297)
        camera.BalanceRatioSelector.SetValue("Green")
        camera.BalanceRatio.SetValue(1.063)
        camera.BalanceRatioSelector.SetValue("Blue")
        camera.BalanceRatio.SetValue(1)
        camera.BslHueValue.SetValue(0)
        camera.BslSaturationValue.SetValue(1)
        camera.BslContrast.SetValue(0)
        camera.BslBrightness.SetValue(0)

    def captureImage(self, path, name, format='.jpeg'):
        '''
        Capture image with name and save in path
        :param path:
        :param name:
        :param format:
        :return:
        '''
        camera.StartGrabbingMax(1)
        while camera.IsGrabbing():
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                image = converter.Convert(grabResult)
                img = image.GetArray()
                imageName = path + name + format
                cv2.imwrite(imageName, img)
            grabResult.Release()
            
    def closeCamera(self): 
        '''
        Close the camera
        :return:
        '''
        camera.Close()

# '''___Demonstration___'''
cam = BaslerdaA250014uc()
#cam.exposure(5000)
cam.captureImage('/home/fossil/Documents/cameraPi/baslerCaptureWithCode/Experiment/', 'testing')
cam.closeCamera()
