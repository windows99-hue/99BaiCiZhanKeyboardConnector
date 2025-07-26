# 99 Baicizhan Keyboard Connector

> Still 3000 words to go...
>
> Marking the beginning of my journey into mobile automation in my domain of expertise

This is a tool that allows your computer to forward keyboard signals to the Baicizhan app on your phone. Works best with Android emulators.

## Foreword

Why doesn't Baicizhan support external Bluetooth keyboards? Sob.

## Installation

Download or clone this repository, then install the required libraries:

```shell
pip install -r requirements.txt
```

After installing `uiautomator2`, connect your phone to your computer and ensure adb can connect to your device (don't forget to enable USB debugging and allow RSA fingerprint).

Execute this command to let `uiautomator2` install necessary components on your computer:

```shell
python -m uiautomator2 init
```

If needed, find instructions for WiFi connection separately.

## Usage

When ready, connect your phone to the computer via your preferred method and run:

```shell
python main.py
```

After the program completes self-check, follow the on-screen instructions to start using it.

Press <kbd>F2</kbd> to switch modes during operation.

## Afterword

This program uses the `MIT License`. If you have suggestions or want to report bugs, feel free to fork my repository or submit an `Issue`.

Thanks for your support! May you memorize all your vocabulary soon!