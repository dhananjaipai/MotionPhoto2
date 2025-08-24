# 📸 MotionPhoto2 CLI

[MIT](https://opensource.org/licenses/MIT)
[Issues](https://www.google.com/search?q=https://github.com/dhananjaipai/MotionPhoto2/issues)

Effortlessly combine your images (`HEIC` or `JPG`) and corresponding Live videos (`MOV` or `MP4`) into Google Photos-compatible Motion Photos, right from your Android device using Termux

This project is an updated and Android-focused port of the original GUI-based script from [PetrVys/MotionPhoto2](https://github.com/PetrVys/MotionPhoto2), specifically optimized for a command-line interface.

## ✨ Key Features

  * **Google & Samsung Compatible:** Creates Motion Photos (v2/v3) that work seamlessly in Google Photos and Samsung Gallery.
  * **Android-Optimized:** Designed to run directly on Android devices via the [Termux](https://termux.dev/en/) terminal.
  * **Preserves iPhone Live Photos:** Migrates the presentation timestamp from iPhone Live Photos, ensuring your motion starts at the correct keyframe.
  * **Intelligent Matching:** Use EXIF metadata to accurately pair images and videos, even when filenames don't match—perfect for exports from Google Takeout or iCloud.
  * **Powerful Batch Processing:** Convert entire directories of photos recursively with a single command.
  * **Modern Format:** Mimics the Motion Photo format used by modern flagship devices and allows you to preserve Live images from Vivo Camera with Google Photos backups

## 🚀 Installation

### Android (Termux)

This script is optimized for Android using the Termux terminal environment.

1.  **Install Termux:** Follow the official [Termux Installation Guide](https://github.com/termux/termux-app?tab=readme-ov-file#installation) (we recommend installing from F-Droid).

2.  **Set up the Environment:** Open Termux and run the following commands to grant storage access, update packages, and install dependencies.

    ```bash
    # Grant storage access
    termux-setup-storage

    # Update packages and install essential tools
    pkg update && pkg upgrade
    pkg install git curl nano python

    # Clone this repository
    git clone https://github.com/dhananjaipai/motionphoto2-cli
    cd motionphoto2-cli

    # Install required Dependencies
    pkg install exiftool
    pkg install python-lxml # Dependency for the script, use a pre-build binary for tmux
    pip install -r requirements.txt
    ```

You're all set\! You can now run the script using `python motionphoto2.py [options]`.

### Windows, macOS, & Linux

For other platforms, please follow the upstream documentation provided in the original repository:

  * [**Windows Instructions**](https://github.com/PetrVys/MotionPhoto2?tab=readme-ov-file#windows)
  * [**Unix and macOS Instructions**](https://github.com/PetrVys/MotionPhoto2?tab=readme-ov-file#unix-and-macos)

## 💻 Usage

### Convert a Single Photo

The most basic usage involves specifying an input image and its corresponding video file.

```bash
python motionphoto2.py --input-image ImageFile.HEIC --input-video VideoFile.MP4
```

> The output file will be named `ImageFile.LIVE.ext` by default.

### Batch Convert a Directory

Process all images and their matching videos in a directory (and its sub-directories). The script matches files by filename (e.g., `IMG_01.jpg` + `IMG_01.mp4`).

```bash
# Process photos from the Camera folder and save them to a new Live folder
python motionphoto2.py \
  --recursive \
  --input-directory '/storage/emulated/0/DCIM/Camera' \
  --output-directory '/storage/emulated/0/DCIM/Live'
```

### Batch Convert and Overwrite

> **Warning:** Use the `--overwrite` and `--delete-video` flags with caution, as they will modify and remove your original files.

This example processes a directory, overwrites the original image file with the new motion photo, and deletes the source video file after a successful conversion.

```bash
python motionphoto2.py \
  --recursive \
  --overwrite \
  --delete-video \
  --input-directory '/storage/emulated/0/DCIM/Camera'
```

## ⚙️ Command-Line Options

Here are all the available flags to customize the script's behavior.

| Option | Description |
| :--- | :--- |
| `--input-image` | Path to the source image file (`.jpg` or `.heic`). |
| `--input-video` | Path to the source video file (`.mp4` or `.mov`). |
| `--input-directory` | Path to the source directory for batch processing. |
| `--output-directory` | Path to the destination directory. If not provided, output is saved in the input directory. |
| `--recursive` | Process all sub-directories within the input directory. |
| `--exif-match` | Use EXIF metadata to match image/video pairs instead of filenames. Highly recommended for iCloud/Google Takeout exports. |
| `--overwrite` | Replace the original image file with the new motion photo. **Use with caution.** |
| `--delete-video` | Delete the original video file after a successful conversion. **Use with caution.** |
| `--copy-unmuxed` | In directory mode, copy any files that were not converted into motion photos to the output directory. |
| `--incremental-mode`| Skip conversion if a motion photo with the same name already exists in the destination. Useful for library updates. |
| `--keep-temp` | Do not delete the temporary files created during the conversion process. |

## ⚠️ Limitations

### HDR Compatibility in Google Photos

There is a known limitation regarding HDR playback specifically within the Google Photos cloud environment.

> Google Photos may not recognize the output as an HDR photo unless the source `HEIC` file was created by an **iPhone 15+ on iOS 18+**.

This is because Google Photos currently checks for a specific Google Camera XMP tag (`GCamera:IsHdr`) to identify HDR content in motion photos. If this tag is absent, it doesn't fall back to checking for the standard Apple or ISO HDR metadata.

Interestingly, the resulting photo *is* still HDR. If you save it back to an iPhone's camera roll or view it locally on an iOS device, it will display in full HDR. The issue is strictly with the server-side processing of Google Photos.

Workarounds for `JPG` and other `HEIC` files are being explored and are on the project roadmap.

## 🙏 Credits & Acknowledgements

This project would not be possible without the work of many talented developers.

  * **Original Source [@PetrVys](https://github.com/PetrVys/MotionPhoto2)** for a working script that converts image+video into compatible motion/live photos
  * **Huge thanks to [@Tkd-Alex](https://github.com/Tkd-Alex)** for porting the original PowerShell script to Python, making it faster and more versatile.
  * Thanks to [@NightMean](https://github.com/NightMean) for implementing the EXIF metadata matching feature.
  * Thanks to [@sahilph](https://github.com/sahilph) for adding the feature to copy non-live photos in directory mode.
  * Thanks to [@tribut](https://github.com/tribut), [@4Urban](https://github.com/4Urban), [@IamRysing](https://github.com/IamRysing) for providing sample Motion Photo pictures, which can be viewed at [PetrVys/MotionPhotoSamples](https://github.com/PetrVys/MotionPhotoSamples).

## 📚 Technical Documentation

For those interested in the underlying format and standards:

  * **Google's Official Documentation:** [Motion Photo Format](https://developer.android.com/media/platform/motion-photo-format)
  * **Samsung Trailer Tags:** Explained in detail at [doodspav/motionphoto](https://github.com/doodspav/motionphoto).
  * **HEIC Muxing:** The approach is similar to `doodspav`'s work but uses top-level MP4 boxes (`mpvd` and `sefd`) for a more standard-compliant implementation.