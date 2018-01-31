# Theme - Fits
An Adaptive theme based on [SyncedSidebarBg](https://packagecontrol.io/packages/SyncedSidebarBg).

> v1.0.5 update is just some bug fixes. Since ST3 provides Adaptive Theme as Default and can be modified without any python file, I am rewriting this theme from python to json.

### Preview

![preview](Preview/preview.gif)

Note that I use [ColorSchemeSelector](https://packagecontrol.io/packages/ColorSchemeSelector) to random select color scheme. 

### Features

- Adaptive Flat UI
- Automatic fits color schemes

### Installation
#### Download
Using **Package Control**: search "Theme - Fits" \
  or Download from [Github](https://github.com/xxxzc/themefits): 
  - open `Preferences -> Browse Packages...`
  - create new folder named `Theme - Fits`
  - download package and unzip into this folder

#### Activation
Open  `Preferences -> Theme -> Fits - Theme`

or Add following code into `Preferences -> Settings - User`:

```json
  	"theme": "Fits.sublime-theme",
```

### Tips

#### 1. File Icons
**More Icons**

Install [A File Icon](https://packagecontrol.io/packages/A%20File%20Icon) to get more file-specific file icons.

**Adaptive**

Get adaptive colored icons by adding following code into `Preferences -> Package Settings -> A File Icon`.

```json
  "color": "#fff",
```
#### 2. Screen Resolution

If your screen size is larger than 100% (like my win laptop is 2560x1440 and I use 200%)

You can edit `Fits.sublime-theme` file: replace all `.png` with `@2x.png`, it may works.

### Changelog

1.0.5:
[FIX] add statusbar icon resource
[FIX] remove the border of input box

1.0.4:

[IMPROVE] more colorized

[CODE] enhance code's readability and logicality

1.0.3:
[FIX] A theme can't be activated properly bug, which is caused by moving a file from one window to another window.

### Credits

Based on [SyncedSidebarBg](https://packagecontrol.io/packages/SyncedSidebarBg) by aziz and Default Theme.

Some assets are from [Spacegray](https://packagecontrol.io/packages/Theme%20-%20Spacegray).

### Contact me
if you have any idea or found bug, please let me know:
- Github: [Issues](https://github.com/xxxzc/themefits/issues)
- Gmail: xxxzcwork@gmail.com
