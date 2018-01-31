# ln-pay
## A minimalistic payment only 'wallet' for lnd

# DISCLAIMER: Do not use this on mainnet, this is still untested for security

## Features
- Extremely small, ~532 kB size on disk
- Firefox integration through protocol handlers
- Pay without confirmation on whitelisted public keys
- CLI
- GUI through [Desktop Notification Specification](https://developer.gnome.org/notification-spec/)

## Features not included
- Channel management
- Show channel balance
- Show wallet balance
- On-chain transaction

Use `lncli` to do those things

## Why?

Existing lnd frontends such as `lightning-pay` or `zap` is extremely large, pulling over hundreds of megabytes of `node.js` and `electron` dependencies, and both of them does not install on my computer for some reason. `ln-pay` only have 1 required dependency and 2 optional dependency

## Dependencies

- Python 3.x
- [grpc](https://grpc.io/docs/quickstart/python.html)
- [lnd](https://github.com/lightningnetwork/lnd)

## Optional dependencies for headless mode

- [PyGObject](https://pygobject.readthedocs.io/en/latest/getting_started.html)
- [notify2](https://pypi.python.org/pypi/notify2)


## Installation
`git clone` this repository, and run `ln-pay.py` on this directory for CLI mode.

## `lightning:` protocol integration
To register `ln-pay` as `lightning:` protocol handler so that you can click the `lightning:` link in your browser:

### Linux

Add this snippet to `~/.local/share/applications` as `ln-pay.desktop`:

```
[Desktop Entry]
Version=1.0
Type=Application
Name=Pay with Lightning Network
Exec=/path/to/ln-pay.py %u
MimeType=x-scheme-handler/lightning;
Terminal=true
Icon=
Comment=
Path=
StartupNotify=false
```

and append `x-scheme-handler/lightning=ln-pay.desktop` to `~/.local/share/applications/mimeapps.list`

This will launch a terminal running `ln-pay.py` every time `lightning:` links are clicked. To use Desktop Notifications GUI, replace `Terminal=true` in `ln-pay.desktop` to `Terminal=false`


## How to Use

`ln-pay` supports 2 modes, terminal/CLI interactive mode, and headless
 mode, where it interacts using [Desktop Notification Specification](https://developer.gnome.org/notification-spec/)

 ### Terminal mode

 ```
./ln-pay.py lntb1u1pd8z46jpp5js40pevvggapufa64p6t5muec3u5lxqnnt9xm9e0wzzwtnqw2weqdrq0v3xgg36yfqkgepq8faxzup6ygkzy6fz8g3rvvrzvvmnsvnz94nrqwpk956rvcn995unxerp94jxvdfjv5ersv3jx5urzgnacqzysx93rdsprk25vwv94lueev0x0g38hnj3qlnqk6eenxrsqygwsmv2pjvuzzvsc272n52cwx8sq78ckvd2vpfa2y9fxmvwdfq5dt3d3rjgppzkmex
1685317000000 mBTC in Lightning Network
Pay to 02d28c3aac4b4f36746052a735831afbe65bc5698a7be5bd41b42fd1ddf2a1a358 for {"d":"Add :zap:","i":"60bc782b-f086-46be-93da-df52e2822581"} with 0.001 mBTC y/n: y
Transaction to 02d28c3aac4b4f36746052a735831afbe65bc5698a7be5bd41b42fd1ddf2a1a358 is successful
```

### Desktop Notifications GUI
Demo TBD

## Setting up automatic payment

Add public keys that `ln-pay` will automatically pay to this whitelist:
```
#Autopay setting
MAX_AUTOPAY_AMT = 0.05 #Maximum amount of mBTC that will be automatically paid
MIN_AUTOPAY_BALANCE = 2 #Minimum channel amount in mBTC for autopaying LN transaction
whitelist = [] #Whitelist of public keys that will be automatically paid by ln-pay
```
