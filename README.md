# ImageFlow

ImageFlow is a simple application to help user filter images between a pre-selection folder and raw image folder. It is
used after all photos from a shooting have been imported and splitted between jpg and raw folders. User can quickly
select interesting photos in the jpg folder and then filter the raw folder to keep only the corresponding raw files in
an output folder.

## Installation

#TODO

## Packaging

To package the application, run the following command:

```shell
pyinstaller --name "ImageFlow" --onefile --add-data "imageflow/ui/design/main_window.ui;imageflow/ui/design/" imageflow/__main__.py --icon="app_icon.ico"
```

## Contributions

Contributions to ImageFlow are welcome! If you have any ideas for new features or improvements, feel free to open an
issue or submit a pull request.

## License

ImageFlow is released under the MIT license. See LICENSE for more information.

## Credits

ImageFlow was developed by Julien LE SAUCE. The system uses several open-source libraries, see project configuration
file for more details.
