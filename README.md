# driverless

Website for controlling RC car hosted on Google Vision Kit where you can drive the car manually with display of the camera, collect data, and launch self-driving mode.

## Setup

The website uses GPIO pins to control movement of the car. GPIOA controls steering of the car and GPIOB controls the speed. Connect the pins to your RC car.

## Installation

1. Git clone the repository on the Vision Kit
2. Install dependencies

```
pip3 install -r requirements.txt
```

3. Run

```
python3 server.py
```

4. Access the website in the browser at http://\<your Vision Kit IP\>:4200

## I want my Edison!

*Because nothing is better than Tesla, except Edison.*

Here is the guide to train your own self-driving car based on Google Vision Kit.

#### Data acquisition

Launch the website. Specify folder name where your pictures will be saved. After that, you can start driving the car using the controls and the pictures will be saved as you drive. For a good model, each category (direction) should have around 1000 images. After your collected images, you can download them in the archive. This may take a minute if you have a lot of pictures.

#### Training

I recommend to use Google Cloud Planform for the training process. Save your data to Cloud Storage bucket. Go to the Marketplace and create Deep Learning VM. Go to the Compute Engine tab and press on SSH near the instance you created. You may need to install the driver the first time you connect. Transfer your files from the bucket to the instance. You won't need now the folder with `unlabeled` images that were captured between different directions so you can delete that folder. Follow Extension to Poet Tutorial from Google to create `.binaryproto` file [here](https://aiyprojects.withgoogle.com/vision/#extension-to-poet-tutorial).

#### Self-driving

Transfer the `.binaryproto` file to the Vision Kit using scp command. Copy it to `/opt/aiy/models`. Check in `app/model.py` that name of your file and labels correspond to ones in the file. If not, modify the file. Launch the website again and you can try self-driving mode from there.

## Documentation

#### Structure

The website is build on top of Flask framework. All pages are handled in `app/main/views.py`. All API calls to handle driving of the car and accessing photos are handled in `app/control/views.py`. You can see examples of the functions below in those files.

#### Control

##### app/camera.py

Main file that operates the camera. The only public method that should be called on an object of Camera class is `add_label`:

```
def add_label(self, new_label, new_duration, folder=None)
```

- new_label - string, label that will be associated with upcoming pictures.
- new_duration - float, time to record images with specified label.
- folder - string, name of the folder where images will be saved as `<folder>/<label>/<timestamp>.png`. If None, images won't be saved.

It will override previous label. If you pass same labels during consecutive calls, the pictures captured in between 2 calls will be saved to the same label folder if you specified folder parameter. Value of `new_duration` should be obtained from function `Car.drive` so camera only saves pictures while the car is driving. Check function `def drive()` at `app/control/views.py` to see an example of usage.


##### app/car.py

Main file that drives the car. There are 2 public functions:

```
def load_config(cls)
```

Load the configuration of the car from the file `app/config.json`. This configuration includes speed, steering and duration of different directions. This can be updated directly from the website.

```
def drive(self, direction)
```

Drive in the direction that is specified in the `app/config.json`. The default directions are 'forward', 'right', 'left', 'back', 'stop'. It will override previous direction and stop driving after time specified in the configuration.

##### app/model.py

Main file that launches self-driving mode. The name of the model file is specified in the variable `MODEL_NAME`. Labels that model is producing are stored in `labels` variable. The model file should be put in `/opt/aiy/models`. This file automatically passes directions to the `Car` class, so the car will be driving in predicted directions. There are 2 public functions:

```
def start(self)
```

Start self-driving mode.

```
def end(self)
```

End self-driving mode.
