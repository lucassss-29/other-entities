from pypylon import pylon
from PIL import Image
from pypylon import genicam
import cv2
import time

''' This is the prepare part for initiating basler camera
    turn it on and set the default parameter.
    They are all in order and be compulsory
'''
timeStart = time.time()
globalTimes = 0
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

'''Use to convert to rgb opencv format.'''
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

'''This class is used for setting each parameters before grab an image.'''


class configCamera:
    def numberOfPic(self, numOP):
        return camera.StartGrabbingMax(numOP)  # set number of image want to grab

    def gain(self, gainValue):
        return camera.Gain.SetValue(gainValue)  # set gain in range: 0 to 24

    def exposure(self, exposureValue):
        return camera.ExposureTime.SetValue(exposureValue)  # set exposure in range: 10 to 1000000

    def brightness(self, brightnessValue):
        return camera.BslBrightness.SetValue(brightnessValue)  # set brightness in range: -1 to 1

    def constrast(self, constrasrValue):
        return camera.BslContrast.SetValue(constrasrValue)  # set contrast in range: -1 to 1

    def blackLevel(self, blackLevelValue):
        return camera.BlackLevel.SetValue(blackLevelValue)  # set black level in range: 0 to 32

    def gamma(self, gammaValue):
        return camera.Gamma.SetValue(gammaValue)  # set gamma in range: 0.25 to 2

    def RGB(self, redValue, greenValue, blueValue):  # set red, blue, green in range: 1 to 7.98
        def initial():
            camera.BalanceRatioSelector.SetValue("Red")
            camera.BalanceRatio.SetValue(redValue)
            camera.BalanceRatioSelector.SetValue("Green")
            camera.BalanceRatio.SetValue(greenValue)
            camera.BalanceRatioSelector.SetValue("Blue")
            camera.BalanceRatio.SetValue(blueValue)

        return initial()

    def hue(self, hueValue):
        return camera.BslHueValue.SetValue(hueValue)  # set hue in range: -180 to 180

    def saturation(self, saturationValue):
        return camera.BslSaturationValue.SetValue(saturationValue)  # set saturation in range: 0 to 4

    def loadFeature(self, nodeFile):
        def initial():
            pylon.FeaturePersistence.Load(nodeFile, camera.GetNodeMap(), True)
            return initial()

    '''Presets demo'''

    def originSetting(self):
        def initial():
            camera.Gain.SetValue(0)
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

        return initial()

    def blackBackground(self):
        def initial():
            camera.Gamma.SetValue(1.3)
            camera.ExposureTime.SetValue(10815)
            camera.BslContrast.SetValue(0.1)
            camera.BslBrightness.SetValue(0)
        return initial()
    def whiteBackground(self):
        def initial():
            camera.Gamma.SetValue(1.4)
            camera.ExposureTime.SetValue(7000)
            camera.BslContrast.SetValue(0.1)
            camera.BslBrightness.SetValue(0)
        return initial()
    def rectangleBackground(self):
        def initial():
            camera.Gamma.SetValue(1.3)
            camera.ExposureTime.SetValue(8100)
            camera.BslContrast.SetValue(0.3)
            camera.BslBrightness.SetValue(0)
        return initial()
    def inkBackground(self):
        def initial():
            camera.Gamma.SetValue(1.5)
            camera.ExposureTime.SetValue(6400)
            camera.BslContrast.SetValue(0.1)
            camera.BslBrightness.SetValue(0)
        return initial()
    def ledBackground(self):
        def initial():
            camera.Gamma.SetValue(1.1)
            camera.ExposureTime.SetValue(7800)
            camera.BslContrast.SetValue(0.1)
            camera.BslBrightness.SetValue(-0.2)
        return initial()


    ''' The method grab() should take place
        after finish setting th parameters '''

    '''Define to globalTimes to set global grabbing times for every grab'''
    global globalTimes
    globalTimes = 0

    '''Grab and Save with name file'''

    def grabAndSave(self, nameFile):
        def initial():
            varTimes = globalTimes
            while camera.IsGrabbing():
                grabResult = camera.RetrieveResult(5000,pylon.TimeoutHandling_ThrowException)  # return true if the call successfully retrieve a grab result, false otherwise
                '''One grab call result is retrieved per call'''
                # img = pylon.PylonImage.AttachGrabResultBuffer(grabResult) #comment out if want to use pypylon save
                if grabResult.GrabSucceeded():
                    ''' Access the image data from pypylon grab'''
                    print("SizeX: ", grabResult.Width)
                    print("SizeY: ", grabResult.Height)
                    varTimes += 1
                    print("Grab %d successful " % varTimes)
                    '''convert to image that opencv can use'''
                    image = converter.Convert(grabResult)
                    img = image.GetArray()
                    imageName = "/home/fossil/Documents/cameraPi/imageSource/rectangleSetting/{0}_{1}.jpeg".format(nameFile,varTimes)
                    cv2.imwrite(imageName, img)
                    print("Save {0}_{1} successful\n ".format(nameFile, varTimes))

                grabResult.Release()
            camera.Close()

        return initial()


'''___main___'''
cam = configCamera()
#cam.originSetting()

cam.numberOfPic(50)
#cam.blackBackground()
#cam.grabAndSave("two_black_holes")

#cam.whiteBackground()
#cam.grabAndSave("two_white_holes")

cam.rectangleBackground()
cam.grabAndSave("rectangle")

#cam.ledBackground()
#cam.grabAndSave("led")

timeStop = time.time()
print("time = ", timeStop - timeStart)

camera.StopGrabbing()
# cv2.destroyAllWindows()
