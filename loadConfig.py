from pypylon import pylon
from PIL import Image
from pypylon import genicam

nodeFile = "NodeMap.pfs"
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

print("Using device ", camera.GetDeviceInfo().GetModelName())
print("Saving camera's node map to file...")
print(nodeFile)

pylon.FeaturePersistence.Save(nodeFile, camera.GetNodeMap())
print("Reading file back to camera's node map...")

pylon.FeaturePersistence.Load(nodeFile, camera.GetNodeMap(), True)
camera.PixelFormat ="RGB8"
camera.StartGrabbingMax(1)
img = pylon.PylonImage()
while camera.IsGrabbing():
        # timeout is 1000ms
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        img.AttachGrabResultBuffer(grabResult)
        if grabResult.GrabSucceeded():
            # Access the image data.
            print("SizeX: ", grabResult.Width)
            print("SizeY: ", grabResult.Height)
            print("Grab 1 successful")
            Image.fromarray(grabResult.Array).save("/home/fossil/Documents/camera_test_case/ImageGrabbed/load1.tiff")
        grabResult.Release()
camera.Close()

