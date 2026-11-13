# Image Processing - BCA 454 (Semester VIII, Elective IV, 3 credits)

Study notes for the TU Image Processing elective (course code CACS404 in the TU outline, Year IV, 5 hours a week: 3 theory and 2 practical; recommended text: Gonzalez and Woods, *Digital Image Processing*). Five units follow the outline in its order.

| Unit | Title | Hours | Outline topics covered |
|---|---|---|---|
| 1 | Fundamentals of Image Processing | 8 | image representation, pixel relationships, elements of a DIP system, visual perception, image formation model, sampling and quantization, colour fundamentals and models, file formats, image operations, brightness, contrast, hue, saturation, Mach band effect |
| 2 | Image Enhancement | 12 | image transforms (DFT, FFT, cosine), frequency-domain enhancement (low-pass, high-pass, homomorphic, Gaussian), spatial-domain enhancement (point processing, contrast stretching, clipping, thresholding, negative, level slicing), histogram processing, spatial filtering |
| 3 | Image Restoration | 9 | degradation model, noise models, blur, inverse filtering, linear motion blur, Wiener filtering, morphological operations (erosion, dilation) |
| 4 | Image Coding and Compression | 9 | need for compression, redundancy, pixel coding, run-length and Huffman coding, information theory, error-free and lossy compression, JPEG and MPEG, wavelet compression |
| 5 | Image Segmentation and Feature Extraction | 10 | thresholding, region-based segmentation, edges, lines and curves, edge operators, features, texture, feature reduction, classification, clustering, and case studies (image security, steganography, watermarking, visual effects, medical imaging, remote sensing) |

## Verification

Every Python program is executed by `bca/tools/fill_script_outputs.py` on NumPy (no image files are needed: all test images are generated in the code), so every printed number is real. Hand-worked exercise answers were checked against the programs.

## Source and honesty

Units and topics follow the TU CACS404 outline as reproduced on notebahadur.com and a college copy of the syllabus PDF; wording, examples and numbers are original. The outline gives hours only partly, the hours above (8, 12, 9, 9, 10) follow the published listing. Standard facts (JPEG tables, Sobel/Canny details, eye anatomy figures, sensor values) are from the textbook and standard references and should be checked against your teacher's notes. No subject-teacher review.
