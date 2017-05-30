# Theme - Fits
A sublime text3 theme based on [SyncedSidebarBg](https://packagecontrol.io/packages/SyncedSidebarBg) that can automatic fits many(almost all) color schemes.

### Preview

![preview](Preview/preview.gif)

Note that I use [ColorSchemeSelector](https://packagecontrol.io/packages/ColorSchemeSelector) to random select color scheme. (But it may encounter a bug that color scheme cannot be switched, in this case, you should close all tabs and reopen them)

### Installation
Using **Package Control**: search "Theme - Fits"

Download from [Github](https://github.com/xxxzc/themefits): 

- open `Preferences -> Browse Packages...`.
- create new folder named `Theme - Fits`.
- download package and unzip into this folder

### Activation

Add following code into `Preferences -> Settings - User`:

```json
	"theme": "Fits.sublime-theme",
```

#### Issues

If your monitor scale is larger than 100% (like my win laptop is 2560x1440 resolution and I use 200% scale)

You can edit `Fits.sublime-theme` file: replace all `.png` with `@2x.png`, it may works.

### File Icons

It's highly recommended to use [A File Icon](https://packagecontrol.io/packages/A%20File%20Icon). 

### Credits

Based on Theme - Default and  [SyncedSidebarBg](https://packagecontrol.io/packages/SyncedSidebarBg) by aziz.

Some assets are from [Spacegray](https://packagecontrol.io/packages/Theme%20-%20Spacegray).

