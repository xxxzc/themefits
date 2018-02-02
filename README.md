# Theme - Fits
An adaptive flat theme based on [SyncedSidebarBg](https://packagecontrol.io/packages/SyncedSidebarBg). 

V1.1.0 maybe a final update. I spent two days rewriting and cleaning up code T T.

Wish u enjoy it!

### Preview

<img src="preview/preview.gif" width="600px"/>

### Features

- Adaptive Flat UI
- Accent Color got from color scheme
- Adapt to most of color schemes
- Customize color

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

### Customization

#### 1. File Icons
**File Icons**

Please install [A File Icon](https://packagecontrol.io/packages/A%20File%20Icon) to get more file-specific icons.

**Adaptation**

Make icons being adaptive by adding following code into `Preferences -> Package Settings -> A File Icon`.

```json
  "color": "#fff",
```
#### 2. Color Settings

Although this theme can handle most of color schemes, there are still a few can't be recognized. In case, you can configure colors by yourself. These color settings have higher priority. You can get detailed information in the setting file. Open `Preferences -> Package Settings -> Theme - Fits`:

```json
    // scope is a key word to determine the accent color.
    "scope": "function",

    // Set up an accent color directly.
    "accent": "#abcdef"
```

#### 3. Screen Resolution

If your screen size is larger than 100% (like my win laptop is 2560x1440 and I use 200%)

You can edit `Fits.sublime-theme` file: replace all `.png` with `@2x.png`, it may works.

### Changelog

1.1.0:

[CODE] Use new APIs to achieve color adaption, more natural

[CODE] Rewrite code to enhance code's readability and logicality

[FEATURE] Remove all unnecessary resources

[FEATURE] Better color scheme compatibility

[FEATURE] Add some configure items

1.0.5:

[FIX] add statusbar icon resource

[FIX] remove the border of input box

1.0.4:

[FEATURE] more colorized

[CODE] enhance code's readability and logicality

1.0.3:
[FIX] A theme can't be activated properly bug, which is caused by moving a file from one window to another window.

### Credits

Based on [SyncedSidebarBg](https://packagecontrol.io/packages/SyncedSidebarBg) by aziz and Theme - Default.

### Contact me
if you have any idea or found bug, please let me know:
- Github: [Issues](https://github.com/xxxzc/themefits/issues)
- Gmail: xxxzcwork@gmail.com
