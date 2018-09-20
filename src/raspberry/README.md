# Raspberry Pi Documentation

## Documentation

OpenCV
Raspbian Stretch


## General Installation

I used the [tutorial](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) at pyimagesearch. I highlight some of the important steps when installing Python and OpenCV on the Raspberry Pi.

### Download Raspbian Stretch and Load the image on a memory card

1. Download the ZIP file for RASPBIAN STRETCH WITH DESKTOP (1.6 GB)
[Download Link](https://www.raspberrypi.org/downloads/raspbian/)

2. Copy the Raspbian Stretch image to the microSD card.
https://howchoo.com/g/ndg2mtbmnmn/how-to-install-raspbian-stretch-on-the-raspberry-pi

  Optional: Add ssh file to the /Volumes/boot directory to enable ssh

3. Eject microSD

4. Load microSD into Raspberry Pi unit

5. Plug in keyboard and monitor

6. Plug into power. The Pi will now turn on and boot up.


### Setup on the Raspberry Pi

For the following steps, I followed the tutorial closely because all of the steps were laid out and easy to follow. I initially intended to include all of the syntax for the installation, but the tutorial already does a good job.

#### Initial setup

#### Update Packages

#### Download OpenCV

#### Download and Setup Python

#### Compile and Install OpenCV

- Configuring swap size: this was a new concept to me and is an important step to the installation. If you skip these steps, then the installation might stall during the process.

#### Testing the OpenCV Installation

- Changing swap size back

## Next steps

- [ ] Connecting to Raspberry Pi using ssh

- [ ] InstallingTensorFlow Lite
