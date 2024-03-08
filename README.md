# WinPi64
 ARM64 Raspberry Pi emulator using QEMU for Windows.

## How to install
Please not that the uncompressed emulator requires about 8.5 GB for the Raspberry Pi OS image and the emulator files.

Within the repository, find the version you would like to download. Follow the link to the pre-compressed .zip file on Google Drive, download the .zip file, extract it into a folder of your choosing, and execute the run.bat script.

#### Note: Windows will likely prevent you from running the run.bat script the first time you run the emulator; this can be bypassed by clicking on "More Info" on the Microsoft Defender window that opens, and then clicking "Run Anyway".
(All of the source files are visible to the user, so you can verify their security on your own if you wish)

Alternatively, you can also download the most recent .zip package from the latest release on GitHub [here](https://github.com/Xachaeus/WinPi64/releases/tag/v0.1.1-beta).

If you would like to be able to run the emulator from your desktop without needing to open anything in the file explorer, simply create a shortcut for the run.bat script and add it to your desktop.

## Using the emulator
Once the emulator is up and running, use the following credentials to log in the first time:
~~~
username: pi
password: raspberry
~~~
You can change the password or set up a new user if you wish. The emulator also supports SSH interfacing, both to and from the virtual machine.
To SSH into another machine from within the emulator, simply run the SSH command as you usually would; no additional settings or commands need to be entered, as making SSH connections **from** the emulator is supported by default.
To SSH **into** the virtual machine, first you must enable SSH connections in the config.
To do this, run
~~~
sudo raspi-config
~~~
and select interface options. From there, you can select SSH and choose to enable/disable connections to the virtual machine.
To open a connection into the virtual machine, make the connection to your host machine's IP address (e.g. localhost, 192.168.1.93) and connect via port 2222.
The following command will let you SSH into your virtual machine from the host machine's command line, assuming the user "pi" exists:
~~~
ssh -p 2222 pi@localhost
~~~
