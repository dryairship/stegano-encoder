## Purpose
The program hides one PNG file into another.

## Principle
The data of the hidden image is stored in the last two bits of a color value. The last two bits of each color value of both the images are lost. However, the difference is too subtle for the human eye to notice.

## Usage
`stegano-encoder.py visible-image.png hidden-image.png [output.png]`
`stegano-decoder.py encoded.png [decoded.png]`
