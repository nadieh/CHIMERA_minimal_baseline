"""
The following is a simple example algorithm.

It is meant to run within a container.

To run the container locally, you can call the following bash script:

  ./do_test_run.sh

This will start the inference and reads from ./test/input and writes to ./test/output

To save the container and prep it for upload to Grand-Challenge.org you can call:

  ./do_save.sh

Any container that shows the same behaviour will do, this is purely an example of how one COULD do it.

Reference the documentation to get details on the runtime environment on the platform:
https://grand-challenge.org/documentation/runtime-environment/

Happy programming!
"""

from pathlib import Path
import json
from glob import glob
import pyvips
import SimpleITK
import numpy
import random

INPUT_PATH = Path("/input")
OUTPUT_PATH = Path("/output")
RESOURCE_PATH = Path("resources")


def run():
    # The key is a tuple of the slugs of the input sockets
    interface_key = get_interface_key()

    # Lookup the handler for this particular set of sockets (i.e. the interface)
    handler = {
        (
            "bladder-cancer-tissue-biopsy-whole-slide-image",
            "bulk-rna-seq-bladder-cancer",
            "chimera-clinical-data-of-bladder-cancer-recurrence",
            "tissue-mask",
        ): interf0_handler,
    }[interface_key]

    # Call the handler
    return handler()


def interf0_handler():
    # Read the input - use thumbnail loading for tissue mask to avoid memory issues with large WSI tissue masks
    input_tissue_mask = load_image_file_as_thumbnail(
        location=INPUT_PATH / "images/tissue-mask",
        max_size=1024,
    )
    # Use thumbnail loading for large WSI to avoid memory issues
    input_bladder_cancer_tissue_biopsy_whole_slide_image = load_image_file_as_thumbnail(
        location=INPUT_PATH / "images/bladder-cancer-tissue-biopsy-wsi",
        max_size=1024,
    )
    input_bulk_rna_seq_bladder_cancer = load_json_file(
        location=INPUT_PATH / "bulk-rna-seq-bladder-cancer.json",
    )
    input_chimera_clinical_data_of_bladder_cancer_recurrence = load_json_file(
        location=INPUT_PATH
        / "chimera-clinical-data-of-bladder-cancer-recurrence-patients.json",
    )

    # Process the inputs: any way you'd like
    _show_torch_cuda_info()

    # Debug: Print information about loaded data
    print("=+=" * 10)
    print("Data Loading Summary:")
    # Handle PyVips objects for tissue mask
    if hasattr(input_tissue_mask, 'width'):
        print(f"Tissue mask size: {input_tissue_mask.width}x{input_tissue_mask.height}")
    else:
        print(f"Tissue mask shape: {input_tissue_mask.shape}")
    
    print(f"Pathology WSI type: {type(input_bladder_cancer_tissue_biopsy_whole_slide_image)}")
    if hasattr(input_bladder_cancer_tissue_biopsy_whole_slide_image, 'width'):
        print(f"Pathology WSI size: {input_bladder_cancer_tissue_biopsy_whole_slide_image.width}x{input_bladder_cancer_tissue_biopsy_whole_slide_image.height}")
    
    print(f"RNA-seq data keys: {list(input_bulk_rna_seq_bladder_cancer.keys()) if input_bulk_rna_seq_bladder_cancer else 'None'}")
    print(f"Clinical data keys: {list(input_chimera_clinical_data_of_bladder_cancer_recurrence.keys()) if input_chimera_clinical_data_of_bladder_cancer_recurrence else 'None'}")
    print("=+=" * 10)

    # Some additional resources might be required, include these in one of two ways.

    # Option 1: part of the Docker-container image: resources/
    resource_dir = Path("/opt/app/resources")
    with open(resource_dir / "some_resource.txt", "r") as f:
        print(f.read())

    # Option 2: upload them as a separate tarball to Grand Challenge (go to your Algorithm > Models). The resources in the tarball will be extracted to `model_dir` at runtime.
    model_dir = Path("/opt/ml/model")
    try:
        with open(
            model_dir / "a_tarball_subdirectory" / "some_tarball_resource.txt", "r"
        ) as f:
            print(f.read())
    except FileNotFoundError:
        print("Model resource file not found - this is expected in test environment")

    # For now, let us make bogus predictions
    # Generate random float between 0 and 80 with one decimal place
    output_likelihood_of_bladder_cancer_recurrence = round(random.uniform(0, 80), 1)

    # Save your output
    write_json_file(
        location=OUTPUT_PATH / "likelihood-of-bladder-cancer-recurrence.json",
        content=output_likelihood_of_bladder_cancer_recurrence,
    )

    return 0


def get_interface_key():
    # The inputs.json is a system generated file that contains information about
    # the inputs that interface with the algorithm
    inputs = load_json_file(
        location=INPUT_PATH / "inputs.json",
    )
    socket_slugs = [sv["interface"]["slug"] for sv in inputs]
    return tuple(sorted(socket_slugs))


def load_json_file(*, location):
    # Reads a json file
    with open(location, "r") as f:
        return json.loads(f.read())


def write_json_file(*, location, content):
    # Writes a json file
    with open(location, "w") as f:
        f.write(json.dumps(content, indent=4))


def load_image_file_as_array(*, location):
    """
    Load image files using appropriate library based on file type:
    - PyVips for pathology images: .tif, .tiff, .mrxs, .svs, .ndpi
    - SimpleITK for radiology images: .mha
    """
    # Find all compatible files
    input_files = (
        glob(str(location / "*.tif"))
        + glob(str(location / "*.tiff"))
        + glob(str(location / "*.mha"))
        + glob(str(location / "*.mrxs"))
        + glob(str(location / "*.svs"))
        + glob(str(location / "*.ndpi"))
    )
    
    if not input_files:
        raise FileNotFoundError(f"No compatible image files found in {location}")
    
    file_path = input_files[0]
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension == '.mha':
        # Use SimpleITK for radiology images (.mha)
        print(f"Loading radiology image using SimpleITK: {file_path}")
        image = SimpleITK.ReadImage(file_path)
        array = SimpleITK.GetArrayFromImage(image)
        return array
    
    else:
        # Use PyVips for pathology images (.tif, .tiff, .mrxs, .svs, .ndpi)
        print(f"Loading pathology image using PyVips: {file_path}")
        image = pyvips.Image.new_from_file(file_path)
        
        # For very large images, you might want to downsample first
        # Uncomment the next line to downsample by factor of 4 to save memory
        # image = image.resize(0.25)
        
        # Convert to numpy array
        # Note: This will load the entire image into memory
        # For production use, consider processing tiles instead
        memory_image = image.write_to_memory()
        array = numpy.frombuffer(memory_image, dtype=numpy.uint8)
        
        # Reshape based on image dimensions and bands
        height = image.height
        width = image.width
        bands = image.bands
        
        if bands == 1:
            # Grayscale image
            array = array.reshape((height, width))
        else:
            # Multi-channel image (RGB, RGBA, etc.)
            array = array.reshape((height, width, bands))
        
        return array


def load_image_file_as_thumbnail(*, location, max_size=1024):
    """
    Load image as a thumbnail for memory-efficient processing of WSIs
    This is recommended for actual whole slide images
    Returns the PyVips image object directly for memory efficiency
    """
    input_files = (
        glob(str(location / "*.tif"))
        + glob(str(location / "*.tiff"))
        + glob(str(location / "*.mha"))
        + glob(str(location / "*.mrxs"))
        + glob(str(location / "*.svs"))
        + glob(str(location / "*.ndpi"))
    )
    
    if not input_files:
        raise FileNotFoundError(f"No compatible image files found in {location}")
    
    file_path = input_files[0]
    print(f"Loading pathology image as thumbnail using PyVips: {file_path}")
    
    # Load image with PyVips
    image = pyvips.Image.new_from_file(file_path)
    
    # Calculate downsampling factor to fit within max_size
    scale_factor = min(max_size / image.width, max_size / image.height)
    if scale_factor < 1.0:
        print(f"Downsampling image by factor {scale_factor:.3f} (from {image.width}x{image.height} to {int(image.width*scale_factor)}x{int(image.height*scale_factor)})")
        image = image.resize(scale_factor)
    else:
        print(f"Image size {image.width}x{image.height} is within max_size={max_size}, no downsampling needed")
    
    # Return the PyVips image object directly (much more memory efficient)
    return image


def _show_torch_cuda_info():
    import torch

    print("=+=" * 10)
    print("Collecting Torch CUDA information")
    print(f"Torch CUDA is available: {(available := torch.cuda.is_available())}")
    if available:
        print(f"\tnumber of devices: {torch.cuda.device_count()}")
        print(f"\tcurrent device: { (current_device := torch.cuda.current_device())}")
        print(f"\tproperties: {torch.cuda.get_device_properties(current_device)}")
    print("=+=" * 10)


if __name__ == "__main__":
    raise SystemExit(run())
