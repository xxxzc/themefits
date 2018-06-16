# Theme - Fits
#### Notice! This theme can't support built-in color schemes(like Celeste, Monokai) currently since file format has been changed, I will fix it asap.

**An adaptive flat theme based on [SyncedSidebarBg](https://packagecontrol.io/packages/SyncedSidebarBg).** 

### Preview

![img](https://raw.githubusercontent.com/xxxzc/themefits/master/Preview/mariana.png)

![img](https://raw.githubusercontent.com/xxxzc/themefits/master/Preview/preview.gif)

### Features

- Adaptive Flat UI
- Adapt to almost all color schemes
- Immediate effect after you change color scheme
- Accent color got from current color scheme
- Customizable accent color

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

#### File Icons
Please install [A File Icon](https://packagecontrol.io/packages/A%20File%20Icon) to get more file-specific icons.

**Adaptation**

Make icons being adaptive by adding following code into `Preferences -> Package Settings -> A File Icon`.

```json
  "color": "#fff",
```
#### Color Settings

Although this theme can handle most of color schemes, there are still a few can't be resolved. In case, you can configure colors by yourself. You can get detailed information in  `Preferences -> Package Settings -> Theme - Fits`:

```json
// scope is a key word to determine the accent color.
"scope": "function",
// Set up an accent color directly.
"accent": "#abcdef"
```

#### Modify Theme

1. install [PackageResourceViewer](https://packagecontrol.io/packages/PackageResourceViewer)
2. open `quick panel`, search `open source`, enter
3. search `theme - fits`, enter
4. select `Fits.sublime-theme`, it will open this file
5. now you can modify it by yourself.

You can check the official docs -> [Documentation Themes](http://www.sublimetext.com/docs/3/themes.html)

#### Screen Resolution

If your screen size is larger than 100% (like my win laptop is 2560x1440 and I use 200%)

You can edit `Fits.sublime-theme` file: replace all `.png` with `@2x.png`, it may works.

### Changelog

1.1.3:

[FIX] font display

1.1.2：

[FIX] clear debug message

1.1.1:

[FIX] solve the problem that some styles can't load. Now, this theme can adapt to almost all color schemes

[IMPROVE] display content under dark color scheme

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



Sorry for my poor English.