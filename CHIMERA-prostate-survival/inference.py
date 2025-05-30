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
import SimpleITK
import numpy

INPUT_PATH = Path("/input")
OUTPUT_PATH = Path("/output")
RESOURCE_PATH = Path("resources")


def run():
    # The key is a tuple of the slugs of the input sockets
    interface_key = get_interface_key()

    # Lookup the handler for this particular set of sockets (i.e. the interface)
    handler = {
        (
            "axial-adc-prostate-mri",
            "axial-dwi-prostate-mri",
            "axial-t2-prostate-mri",
            "chimera-clinical-data-of-prostate-cancer-patients",
            "prostate-tissue-mask-for-axial-adc-prostate-mri",
            "prostate-tissue-mask-for-axial-dwi-prostate-mri",
            "prostate-tissue-mask-for-axial-t2-prostate-mri",
            "prostate-tissue-mask-for-transverse-dce-mri",
            "prostatectomy-tissue-mask",
            "prostatectomy-tissue-whole-slide-image",
            "transverse-dce-prostate-mri",
        ): interface_0_handler,
        (
            "axial-adc-prostate-mri",
            "axial-dwi-prostate-mri",
            "axial-t2-prostate-mri",
            "chimera-clinical-data-of-prostate-cancer-patients",
            "prostate-tissue-mask-for-axial-adc-prostate-mri",
            "prostate-tissue-mask-for-axial-dwi-prostate-mri",
            "prostate-tissue-mask-for-axial-t2-prostate-mri",
            "prostate-tissue-mask-for-transverse-dce-mri",
            "prostatectomy-tissue-mask",
            "prostatectomy-tissue-whole-slide-image",
            "prostatectomy-tissue-whole-slide-image-1",
            "prostatectomy-tissue-whole-slide-image-1-2",
            "transverse-dce-prostate-mri",
        ): interface_1_handler,
        (
            "axial-adc-prostate-mri",
            "axial-dwi-prostate-mri",
            "axial-t2-prostate-mri",
            "chimera-clinical-data-of-prostate-cancer-patients",
            "prostate-tissue-mask-for-axial-adc-prostate-mri",
            "prostate-tissue-mask-for-axial-dwi-prostate-mri",
            "prostate-tissue-mask-for-axial-t2-prostate-mri",
            "prostate-tissue-mask-for-transverse-dce-mri",
            "prostatectomy-tissue-mask",
            "prostatectomy-tissue-whole-slide-image",
            "prostatectomy-tissue-whole-slide-image-1",
            "prostatectomy-tissue-whole-slide-image-1-2",
            "prostatectomy-tissue-whole-slide-image-2",
            "prostatectomy-tissue-whole-slide-image-2-2",
            "transverse-dce-prostate-mri",
        ): interface_2_handler,
        (
            "axial-adc-prostate-mri",
            "axial-dwi-prostate-mri",
            "axial-t2-prostate-mri",
            "chimera-clinical-data-of-prostate-cancer-patients",
            "prostate-tissue-mask-for-axial-adc-prostate-mri",
            "prostate-tissue-mask-for-axial-dwi-prostate-mri",
            "prostate-tissue-mask-for-axial-t2-prostate-mri",
            "prostate-tissue-mask-for-transverse-dce-mri",
            "prostatectomy-tissue-mask",
            "prostatectomy-tissue-whole-slide-image",
            "prostatectomy-tissue-whole-slide-image-1",
            "prostatectomy-tissue-whole-slide-image-1-2",
            "prostatectomy-tissue-whole-slide-image-2",
            "prostatectomy-tissue-whole-slide-image-2-2",
            "prostatectomy-tissue-whole-slide-image-3",
            "prostatectomy-tissue-whole-slide-image-3-2",
            "transverse-dce-prostate-mri",
        ): interface_3_handler,
        (
            "axial-adc-prostate-mri",
            "axial-dwi-prostate-mri",
            "axial-t2-prostate-mri",
            "chimera-clinical-data-of-prostate-cancer-patients",
            "prostate-tissue-mask-for-axial-adc-prostate-mri",
            "prostate-tissue-mask-for-axial-dwi-prostate-mri",
            "prostate-tissue-mask-for-axial-t2-prostate-mri",
            "prostate-tissue-mask-for-transverse-dce-mri",
            "prostatectomy-tissue-mask",
            "prostatectomy-tissue-whole-slide-image",
            "prostatectomy-tissue-whole-slide-image-1",
            "prostatectomy-tissue-whole-slide-image-1-2",
            "prostatectomy-tissue-whole-slide-image-2",
            "prostatectomy-tissue-whole-slide-image-2-2",
            "prostatectomy-tissue-whole-slide-image-3",
            "prostatectomy-tissue-whole-slide-image-3-2",
            "prostatectomy-tissue-whole-slide-image-4",
            "prostatectomy-tissue-whole-slide-image-4-2",
            "transverse-dce-prostate-mri",
        ): interface_4_handler,
        (
            "axial-adc-prostate-mri",
            "axial-dwi-prostate-mri",
            "axial-t2-prostate-mri",
            "chimera-clinical-data-of-prostate-cancer-patients",
            "prostate-tissue-mask-for-axial-adc-prostate-mri",
            "prostate-tissue-mask-for-axial-dwi-prostate-mri",
            "prostate-tissue-mask-for-axial-t2-prostate-mri",
            "prostate-tissue-mask-for-transverse-dce-mri",
            "prostatectomy-tissue-mask",
            "prostatectomy-tissue-whole-slide-image",
            "prostatectomy-tissue-whole-slide-image-1",
            "prostatectomy-tissue-whole-slide-image-1-2",
            "prostatectomy-tissue-whole-slide-image-2",
            "prostatectomy-tissue-whole-slide-image-2-2",
            "prostatectomy-tissue-whole-slide-image-3",
            "prostatectomy-tissue-whole-slide-image-3-2",
            "prostatectomy-tissue-whole-slide-image-4",
            "prostatectomy-tissue-whole-slide-image-4-2",
            "prostatectomy-tissue-whole-slide-image-5",
            "prostatectomy-tissue-whole-slide-image-5-2",
            "transverse-dce-prostate-mri",
        ): interface_5_handler,
        (
            "axial-adc-prostate-mri",
            "axial-dwi-prostate-mri",
            "axial-t2-prostate-mri",
            "chimera-clinical-data-of-prostate-cancer-patients",
            "prostate-tissue-mask-for-axial-adc-prostate-mri",
            "prostate-tissue-mask-for-axial-dwi-prostate-mri",
            "prostate-tissue-mask-for-axial-t2-prostate-mri",
            "prostate-tissue-mask-for-transverse-dce-mri",
            "prostatectomy-tissue-mask",
            "prostatectomy-tissue-whole-slide-image",
            "prostatectomy-tissue-whole-slide-image-1",
            "prostatectomy-tissue-whole-slide-image-1-2",
            "prostatectomy-tissue-whole-slide-image-2",
            "prostatectomy-tissue-whole-slide-image-2-2",
            "prostatectomy-tissue-whole-slide-image-3",
            "prostatectomy-tissue-whole-slide-image-3-2",
            "prostatectomy-tissue-whole-slide-image-4",
            "prostatectomy-tissue-whole-slide-image-4-2",
            "prostatectomy-tissue-whole-slide-image-5",
            "prostatectomy-tissue-whole-slide-image-5-2",
            "prostatectomy-tissue-whole-slide-image-6",
            "prostatectomy-tissue-whole-slide-image-6-2",
            "transverse-dce-prostate-mri",
        ): interface_6_handler,
        (
            "axial-adc-prostate-mri",
            "axial-dwi-prostate-mri",
            "axial-t2-prostate-mri",
            "chimera-clinical-data-of-prostate-cancer-patients",
            "prostate-tissue-mask-for-axial-adc-prostate-mri",
            "prostate-tissue-mask-for-axial-dwi-prostate-mri",
            "prostate-tissue-mask-for-axial-t2-prostate-mri",
            "prostate-tissue-mask-for-transverse-dce-mri",
            "prostatectomy-tissue-mask",
            "prostatectomy-tissue-whole-slide-image",
            "prostatectomy-tissue-whole-slide-image-1",
            "prostatectomy-tissue-whole-slide-image-1-2",
            "prostatectomy-tissue-whole-slide-image-2",
            "prostatectomy-tissue-whole-slide-image-2-2",
            "prostatectomy-tissue-whole-slide-image-3",
            "prostatectomy-tissue-whole-slide-image-3-2",
            "prostatectomy-tissue-whole-slide-image-4",
            "prostatectomy-tissue-whole-slide-image-4-2",
            "prostatectomy-tissue-whole-slide-image-5",
            "prostatectomy-tissue-whole-slide-image-5-2",
            "prostatectomy-tissue-whole-slide-image-6",
            "prostatectomy-tissue-whole-slide-image-6-2",
            "prostatectomy-tissue-whole-slide-image-7",
            "prostatectomy-tissue-whole-slide-image-7-2",
            "transverse-dce-prostate-mri",
        ): interface_7_handler,
        (
            "axial-adc-prostate-mri",
            "axial-dwi-prostate-mri",
            "axial-t2-prostate-mri",
            "chimera-clinical-data-of-prostate-cancer-patients",
            "prostate-tissue-mask-for-axial-adc-prostate-mri",
            "prostate-tissue-mask-for-axial-dwi-prostate-mri",
            "prostate-tissue-mask-for-axial-t2-prostate-mri",
            "prostate-tissue-mask-for-transverse-dce-mri",
            "prostatectomy-tissue-mask",
            "prostatectomy-tissue-whole-slide-image",
            "prostatectomy-tissue-whole-slide-image-1",
            "prostatectomy-tissue-whole-slide-image-1-2",
            "prostatectomy-tissue-whole-slide-image-2",
            "prostatectomy-tissue-whole-slide-image-2-2",
            "prostatectomy-tissue-whole-slide-image-3",
            "prostatectomy-tissue-whole-slide-image-3-2",
            "prostatectomy-tissue-whole-slide-image-4",
            "prostatectomy-tissue-whole-slide-image-4-2",
            "prostatectomy-tissue-whole-slide-image-5",
            "prostatectomy-tissue-whole-slide-image-5-2",
            "prostatectomy-tissue-whole-slide-image-6",
            "prostatectomy-tissue-whole-slide-image-6-2",
            "prostatectomy-tissue-whole-slide-image-7",
            "prostatectomy-tissue-whole-slide-image-7-2",
            "prostatectomy-tissue-whole-slide-image-8",
            "prostatectomy-tissue-whole-slide-image-8-2",
            "transverse-dce-prostate-mri",
        ): interface_8_handler,
        (
            "axial-adc-prostate-mri",
            "axial-dwi-prostate-mri",
            "axial-t2-prostate-mri",
            "chimera-clinical-data-of-prostate-cancer-patients",
            "prostate-tissue-mask-for-axial-adc-prostate-mri",
            "prostate-tissue-mask-for-axial-dwi-prostate-mri",
            "prostate-tissue-mask-for-axial-t2-prostate-mri",
            "prostate-tissue-mask-for-transverse-dce-mri",
            "prostatectomy-tissue-mask",
            "prostatectomy-tissue-whole-slide-image",
            "prostatectomy-tissue-whole-slide-image-1",
            "prostatectomy-tissue-whole-slide-image-1-2",
            "prostatectomy-tissue-whole-slide-image-2",
            "prostatectomy-tissue-whole-slide-image-2-2",
            "prostatectomy-tissue-whole-slide-image-3",
            "prostatectomy-tissue-whole-slide-image-3-2",
            "prostatectomy-tissue-whole-slide-image-4",
            "prostatectomy-tissue-whole-slide-image-4-2",
            "prostatectomy-tissue-whole-slide-image-5",
            "prostatectomy-tissue-whole-slide-image-5-2",
            "prostatectomy-tissue-whole-slide-image-6",
            "prostatectomy-tissue-whole-slide-image-6-2",
            "prostatectomy-tissue-whole-slide-image-7",
            "prostatectomy-tissue-whole-slide-image-7-2",
            "prostatectomy-tissue-whole-slide-image-8",
            "prostatectomy-tissue-whole-slide-image-8-2",
            "prostatectomy-tissue-whole-slide-image-9",
            "prostatectomy-tissue-whole-slide-image-9-2",
            "transverse-dce-prostate-mri",
        ): interface_9_handler,
    }[interface_key]

    # Call the handler
    return handler()


def interface_0_handler():
    # Read the input
    input_transverse_dce_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/transverse-dce-prostate-mri",
    )
    input_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-t2-prostate-mri",
    )
    input_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-adc-prostate-mri",
    )
    input_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi",
    )
    input_prostatectomy_tissue_mask = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-mask",
    )
    input_chimera_clinical_data_of_prostate_cancer_patients = load_json_file(
        location=INPUT_PATH / "chimera-clinical-data-of-prostate-cancer-patients.json",
    )
    input_prostate_tissue_mask_for_transverse_dce_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-transverse-dce-mri",
    )
    input_prostate_tissue_mask_for_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-t2-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-adc-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-dwi-prostate-mri",
    )

    # Process the inputs: any way you'd like
    _show_torch_cuda_info()

    # Some additional resources might be required, include these in one of two ways.

    # Option 1: part of the Docker-container image: resources/
    resource_dir = Path("/opt/app/resources")
    with open(resource_dir / "some_resource.txt", "r") as f:
        print(f.read())

    # Option 2: upload them as a separate tarball to Grand Challenge (go to your Algorithm > Models). The resources in the tarball will be extracted to `model_dir` at runtime.
    model_dir = Path("/opt/ml/model")
    with open(
        model_dir / "a_tarball_subdirectory" / "some_tarball_resource.txt", "r"
    ) as f:
        print(f.read())

    # For now, let us make bogus predictions
    output_time_to_biochemical_recurrence_for_prostate_cancer = 42.0

    # Save your output
    write_json_file(
        location=OUTPUT_PATH
        / "time-to-biochemical-recurrence-for-prostate-cancer-months.json",
        content=output_time_to_biochemical_recurrence_for_prostate_cancer,
    )

    return 0


def interface_1_handler():
    # Read the input
    input_transverse_dce_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/transverse-dce-prostate-mri",
    )
    input_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-t2-prostate-mri",
    )
    input_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-adc-prostate-mri",
    )
    input_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi",
    )
    input_prostatectomy_tissue_mask = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-mask",
    )
    input_chimera_clinical_data_of_prostate_cancer_patients = load_json_file(
        location=INPUT_PATH / "chimera-clinical-data-of-prostate-cancer-patients.json",
    )
    input_prostatectomy_tissue_whole_slide_image_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-1",
    )
    input_prostate_tissue_mask_for_transverse_dce_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-transverse-dce-mri",
    )
    input_prostate_tissue_mask_for_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-t2-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-adc-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image_1_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-1",
    )

    # Process the inputs: any way you'd like
    _show_torch_cuda_info()

    # Some additional resources might be required, include these in one of two ways.

    # Option 1: part of the Docker-container image: resources/
    resource_dir = Path("/opt/app/resources")
    with open(resource_dir / "some_resource.txt", "r") as f:
        print(f.read())

    # Option 2: upload them as a separate tarball to Grand Challenge (go to your Algorithm > Models). The resources in the tarball will be extracted to `model_dir` at runtime.
    model_dir = Path("/opt/ml/model")
    with open(
        model_dir / "a_tarball_subdirectory" / "some_tarball_resource.txt", "r"
    ) as f:
        print(f.read())

    # For now, let us make bogus predictions
    output_time_to_biochemical_recurrence_for_prostate_cancer = 42.0

    # Save your output
    write_json_file(
        location=OUTPUT_PATH
        / "time-to-biochemical-recurrence-for-prostate-cancer-months.json",
        content=output_time_to_biochemical_recurrence_for_prostate_cancer,
    )

    return 0


def interface_2_handler():
    # Read the input
    input_transverse_dce_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/transverse-dce-prostate-mri",
    )
    input_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-t2-prostate-mri",
    )
    input_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-adc-prostate-mri",
    )
    input_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi",
    )
    input_prostatectomy_tissue_mask = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-mask",
    )
    input_chimera_clinical_data_of_prostate_cancer_patients = load_json_file(
        location=INPUT_PATH / "chimera-clinical-data-of-prostate-cancer-patients.json",
    )
    input_prostatectomy_tissue_whole_slide_image_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-2",
    )
    input_prostate_tissue_mask_for_transverse_dce_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-transverse-dce-mri",
    )
    input_prostate_tissue_mask_for_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-t2-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-adc-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image_1_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-2",
    )

    # Process the inputs: any way you'd like
    _show_torch_cuda_info()

    # Some additional resources might be required, include these in one of two ways.

    # Option 1: part of the Docker-container image: resources/
    resource_dir = Path("/opt/app/resources")
    with open(resource_dir / "some_resource.txt", "r") as f:
        print(f.read())

    # Option 2: upload them as a separate tarball to Grand Challenge (go to your Algorithm > Models). The resources in the tarball will be extracted to `model_dir` at runtime.
    model_dir = Path("/opt/ml/model")
    with open(
        model_dir / "a_tarball_subdirectory" / "some_tarball_resource.txt", "r"
    ) as f:
        print(f.read())

    # For now, let us make bogus predictions
    output_time_to_biochemical_recurrence_for_prostate_cancer = 42.0

    # Save your output
    write_json_file(
        location=OUTPUT_PATH
        / "time-to-biochemical-recurrence-for-prostate-cancer-months.json",
        content=output_time_to_biochemical_recurrence_for_prostate_cancer,
    )

    return 0


def interface_3_handler():
    # Read the input
    input_transverse_dce_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/transverse-dce-prostate-mri",
    )
    input_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-t2-prostate-mri",
    )
    input_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-adc-prostate-mri",
    )
    input_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi",
    )
    input_prostatectomy_tissue_mask = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-mask",
    )
    input_chimera_clinical_data_of_prostate_cancer_patients = load_json_file(
        location=INPUT_PATH / "chimera-clinical-data-of-prostate-cancer-patients.json",
    )
    input_prostatectomy_tissue_whole_slide_image_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-3",
    )
    input_prostate_tissue_mask_for_transverse_dce_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-transverse-dce-mri",
    )
    input_prostate_tissue_mask_for_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-t2-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-adc-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image_1_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-3",
    )

    # Process the inputs: any way you'd like
    _show_torch_cuda_info()

    # Some additional resources might be required, include these in one of two ways.

    # Option 1: part of the Docker-container image: resources/
    resource_dir = Path("/opt/app/resources")
    with open(resource_dir / "some_resource.txt", "r") as f:
        print(f.read())

    # Option 2: upload them as a separate tarball to Grand Challenge (go to your Algorithm > Models). The resources in the tarball will be extracted to `model_dir` at runtime.
    model_dir = Path("/opt/ml/model")
    with open(
        model_dir / "a_tarball_subdirectory" / "some_tarball_resource.txt", "r"
    ) as f:
        print(f.read())

    # For now, let us make bogus predictions
    output_time_to_biochemical_recurrence_for_prostate_cancer = 42.0

    # Save your output
    write_json_file(
        location=OUTPUT_PATH
        / "time-to-biochemical-recurrence-for-prostate-cancer-months.json",
        content=output_time_to_biochemical_recurrence_for_prostate_cancer,
    )

    return 0


def interface_4_handler():
    # Read the input
    input_transverse_dce_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/transverse-dce-prostate-mri",
    )
    input_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-t2-prostate-mri",
    )
    input_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-adc-prostate-mri",
    )
    input_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi",
    )
    input_prostatectomy_tissue_mask = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-mask",
    )
    input_chimera_clinical_data_of_prostate_cancer_patients = load_json_file(
        location=INPUT_PATH / "chimera-clinical-data-of-prostate-cancer-patients.json",
    )
    input_prostatectomy_tissue_whole_slide_image_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-4",
    )
    input_prostate_tissue_mask_for_transverse_dce_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-transverse-dce-mri",
    )
    input_prostate_tissue_mask_for_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-t2-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-adc-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image_1_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-4",
    )

    # Process the inputs: any way you'd like
    _show_torch_cuda_info()

    # Some additional resources might be required, include these in one of two ways.

    # Option 1: part of the Docker-container image: resources/
    resource_dir = Path("/opt/app/resources")
    with open(resource_dir / "some_resource.txt", "r") as f:
        print(f.read())

    # Option 2: upload them as a separate tarball to Grand Challenge (go to your Algorithm > Models). The resources in the tarball will be extracted to `model_dir` at runtime.
    model_dir = Path("/opt/ml/model")
    with open(
        model_dir / "a_tarball_subdirectory" / "some_tarball_resource.txt", "r"
    ) as f:
        print(f.read())

    # For now, let us make bogus predictions
    output_time_to_biochemical_recurrence_for_prostate_cancer = 42.0

    # Save your output
    write_json_file(
        location=OUTPUT_PATH
        / "time-to-biochemical-recurrence-for-prostate-cancer-months.json",
        content=output_time_to_biochemical_recurrence_for_prostate_cancer,
    )

    return 0


def interface_5_handler():
    # Read the input
    input_transverse_dce_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/transverse-dce-prostate-mri",
    )
    input_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-t2-prostate-mri",
    )
    input_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-adc-prostate-mri",
    )
    input_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi",
    )
    input_prostatectomy_tissue_mask = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-mask",
    )
    input_chimera_clinical_data_of_prostate_cancer_patients = load_json_file(
        location=INPUT_PATH / "chimera-clinical-data-of-prostate-cancer-patients.json",
    )
    input_prostatectomy_tissue_whole_slide_image_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-4",
    )
    input_prostatectomy_tissue_whole_slide_image_5 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-5",
    )
    input_prostate_tissue_mask_for_transverse_dce_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-transverse-dce-mri",
    )
    input_prostate_tissue_mask_for_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-t2-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-adc-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image_1_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-4",
    )
    input_prostatectomy_tissue_whole_slide_image_5_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-5",
    )

    # Process the inputs: any way you'd like
    _show_torch_cuda_info()

    # Some additional resources might be required, include these in one of two ways.

    # Option 1: part of the Docker-container image: resources/
    resource_dir = Path("/opt/app/resources")
    with open(resource_dir / "some_resource.txt", "r") as f:
        print(f.read())

    # Option 2: upload them as a separate tarball to Grand Challenge (go to your Algorithm > Models). The resources in the tarball will be extracted to `model_dir` at runtime.
    model_dir = Path("/opt/ml/model")
    with open(
        model_dir / "a_tarball_subdirectory" / "some_tarball_resource.txt", "r"
    ) as f:
        print(f.read())

    # For now, let us make bogus predictions
    output_time_to_biochemical_recurrence_for_prostate_cancer = 42.0

    # Save your output
    write_json_file(
        location=OUTPUT_PATH
        / "time-to-biochemical-recurrence-for-prostate-cancer-months.json",
        content=output_time_to_biochemical_recurrence_for_prostate_cancer,
    )

    return 0


def interface_6_handler():
    # Read the input
    input_transverse_dce_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/transverse-dce-prostate-mri",
    )
    input_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-t2-prostate-mri",
    )
    input_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-adc-prostate-mri",
    )
    input_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi",
    )
    input_prostatectomy_tissue_mask = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-mask",
    )
    input_chimera_clinical_data_of_prostate_cancer_patients = load_json_file(
        location=INPUT_PATH / "chimera-clinical-data-of-prostate-cancer-patients.json",
    )
    input_prostatectomy_tissue_whole_slide_image_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-4",
    )
    input_prostatectomy_tissue_whole_slide_image_5 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-5",
    )
    input_prostatectomy_tissue_whole_slide_image_6 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-6",
    )
    input_prostate_tissue_mask_for_transverse_dce_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-transverse-dce-mri",
    )
    input_prostate_tissue_mask_for_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-t2-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-adc-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image_1_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-4",
    )
    input_prostatectomy_tissue_whole_slide_image_5_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-5",
    )
    input_prostatectomy_tissue_whole_slide_image_6_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-6",
    )

    # Process the inputs: any way you'd like
    _show_torch_cuda_info()

    # Some additional resources might be required, include these in one of two ways.

    # Option 1: part of the Docker-container image: resources/
    resource_dir = Path("/opt/app/resources")
    with open(resource_dir / "some_resource.txt", "r") as f:
        print(f.read())

    # Option 2: upload them as a separate tarball to Grand Challenge (go to your Algorithm > Models). The resources in the tarball will be extracted to `model_dir` at runtime.
    model_dir = Path("/opt/ml/model")
    with open(
        model_dir / "a_tarball_subdirectory" / "some_tarball_resource.txt", "r"
    ) as f:
        print(f.read())

    # For now, let us make bogus predictions
    output_time_to_biochemical_recurrence_for_prostate_cancer = 42.0

    # Save your output
    write_json_file(
        location=OUTPUT_PATH
        / "time-to-biochemical-recurrence-for-prostate-cancer-months.json",
        content=output_time_to_biochemical_recurrence_for_prostate_cancer,
    )

    return 0


def interface_7_handler():
    # Read the input
    input_transverse_dce_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/transverse-dce-prostate-mri",
    )
    input_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-t2-prostate-mri",
    )
    input_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-adc-prostate-mri",
    )
    input_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi",
    )
    input_prostatectomy_tissue_mask = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-mask",
    )
    input_chimera_clinical_data_of_prostate_cancer_patients = load_json_file(
        location=INPUT_PATH / "chimera-clinical-data-of-prostate-cancer-patients.json",
    )
    input_prostatectomy_tissue_whole_slide_image_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-4",
    )
    input_prostatectomy_tissue_whole_slide_image_5 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-5",
    )
    input_prostatectomy_tissue_whole_slide_image_6 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-6",
    )
    input_prostatectomy_tissue_whole_slide_image_7 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-7",
    )
    input_prostate_tissue_mask_for_transverse_dce_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-transverse-dce-mri",
    )
    input_prostate_tissue_mask_for_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-t2-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-adc-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image_1_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-4",
    )
    input_prostatectomy_tissue_whole_slide_image_5_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-5",
    )
    input_prostatectomy_tissue_whole_slide_image_6_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-6",
    )
    input_prostatectomy_tissue_whole_slide_image_7_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-7",
    )

    # Process the inputs: any way you'd like
    _show_torch_cuda_info()

    # Some additional resources might be required, include these in one of two ways.

    # Option 1: part of the Docker-container image: resources/
    resource_dir = Path("/opt/app/resources")
    with open(resource_dir / "some_resource.txt", "r") as f:
        print(f.read())

    # Option 2: upload them as a separate tarball to Grand Challenge (go to your Algorithm > Models). The resources in the tarball will be extracted to `model_dir` at runtime.
    model_dir = Path("/opt/ml/model")
    with open(
        model_dir / "a_tarball_subdirectory" / "some_tarball_resource.txt", "r"
    ) as f:
        print(f.read())

    # For now, let us make bogus predictions
    output_time_to_biochemical_recurrence_for_prostate_cancer = 42.0

    # Save your output
    write_json_file(
        location=OUTPUT_PATH
        / "time-to-biochemical-recurrence-for-prostate-cancer-months.json",
        content=output_time_to_biochemical_recurrence_for_prostate_cancer,
    )

    return 0


def interface_8_handler():
    # Read the input
    input_transverse_dce_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/transverse-dce-prostate-mri",
    )
    input_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-t2-prostate-mri",
    )
    input_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-adc-prostate-mri",
    )
    input_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi",
    )
    input_prostatectomy_tissue_mask = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-mask",
    )
    input_chimera_clinical_data_of_prostate_cancer_patients = load_json_file(
        location=INPUT_PATH / "chimera-clinical-data-of-prostate-cancer-patients.json",
    )
    input_prostatectomy_tissue_whole_slide_image_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-4",
    )
    input_prostatectomy_tissue_whole_slide_image_5 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-5",
    )
    input_prostatectomy_tissue_whole_slide_image_6 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-6",
    )
    input_prostatectomy_tissue_whole_slide_image_7 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-7",
    )
    input_prostatectomy_tissue_whole_slide_image_8 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-8",
    )
    input_prostate_tissue_mask_for_transverse_dce_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-transverse-dce-mri",
    )
    input_prostate_tissue_mask_for_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-t2-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-adc-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image_1_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-4",
    )
    input_prostatectomy_tissue_whole_slide_image_5_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-5",
    )
    input_prostatectomy_tissue_whole_slide_image_6_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-6",
    )
    input_prostatectomy_tissue_whole_slide_image_7_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-7",
    )
    input_prostatectomy_tissue_whole_slide_image_8_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-8",
    )

    # Process the inputs: any way you'd like
    _show_torch_cuda_info()

    # Some additional resources might be required, include these in one of two ways.

    # Option 1: part of the Docker-container image: resources/
    resource_dir = Path("/opt/app/resources")
    with open(resource_dir / "some_resource.txt", "r") as f:
        print(f.read())

    # Option 2: upload them as a separate tarball to Grand Challenge (go to your Algorithm > Models). The resources in the tarball will be extracted to `model_dir` at runtime.
    model_dir = Path("/opt/ml/model")
    with open(
        model_dir / "a_tarball_subdirectory" / "some_tarball_resource.txt", "r"
    ) as f:
        print(f.read())

    # For now, let us make bogus predictions
    output_time_to_biochemical_recurrence_for_prostate_cancer = 42.0

    # Save your output
    write_json_file(
        location=OUTPUT_PATH
        / "time-to-biochemical-recurrence-for-prostate-cancer-months.json",
        content=output_time_to_biochemical_recurrence_for_prostate_cancer,
    )

    return 0


def interface_9_handler():
    # Read the input
    input_transverse_dce_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/transverse-dce-prostate-mri",
    )
    input_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-t2-prostate-mri",
    )
    input_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-adc-prostate-mri",
    )
    input_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi",
    )
    input_prostatectomy_tissue_mask = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-mask",
    )
    input_chimera_clinical_data_of_prostate_cancer_patients = load_json_file(
        location=INPUT_PATH / "chimera-clinical-data-of-prostate-cancer-patients.json",
    )
    input_prostatectomy_tissue_whole_slide_image_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-4",
    )
    input_prostatectomy_tissue_whole_slide_image_5 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-5",
    )
    input_prostatectomy_tissue_whole_slide_image_6 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-6",
    )
    input_prostatectomy_tissue_whole_slide_image_7 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-7",
    )
    input_prostatectomy_tissue_whole_slide_image_8 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-8",
    )
    input_prostatectomy_tissue_whole_slide_image_9 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-wsi-z-9",
    )
    input_prostate_tissue_mask_for_transverse_dce_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-transverse-dce-mri",
    )
    input_prostate_tissue_mask_for_axial_t2_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-t2-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_adc_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-adc-prostate-mri",
    )
    input_prostate_tissue_mask_for_axial_dwi_prostate_mri = load_image_file_as_array(
        location=INPUT_PATH / "images/prostate-tissue-mask-for-axial-dwi-prostate-mri",
    )
    input_prostatectomy_tissue_whole_slide_image_1_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-1",
    )
    input_prostatectomy_tissue_whole_slide_image_2_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-2",
    )
    input_prostatectomy_tissue_whole_slide_image_3_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-3",
    )
    input_prostatectomy_tissue_whole_slide_image_4_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-4",
    )
    input_prostatectomy_tissue_whole_slide_image_5_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-5",
    )
    input_prostatectomy_tissue_whole_slide_image_6_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-6",
    )
    input_prostatectomy_tissue_whole_slide_image_7_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-7",
    )
    input_prostatectomy_tissue_whole_slide_image_8_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-8",
    )
    input_prostatectomy_tissue_whole_slide_image_9_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/prostatectomy-tissue-wsi-9",
    )

    # Process the inputs: any way you'd like
    _show_torch_cuda_info()

    # Some additional resources might be required, include these in one of two ways.

    # Option 1: part of the Docker-container image: resources/
    resource_dir = Path("/opt/app/resources")
    with open(resource_dir / "some_resource.txt", "r") as f:
        print(f.read())

    # Option 2: upload them as a separate tarball to Grand Challenge (go to your Algorithm > Models). The resources in the tarball will be extracted to `model_dir` at runtime.
    model_dir = Path("/opt/ml/model")
    with open(
        model_dir / "a_tarball_subdirectory" / "some_tarball_resource.txt", "r"
    ) as f:
        print(f.read())

    # For now, let us make bogus predictions
    output_time_to_biochemical_recurrence_for_prostate_cancer = 42.0

    # Save your output
    write_json_file(
        location=OUTPUT_PATH
        / "time-to-biochemical-recurrence-for-prostate-cancer-months.json",
        content=output_time_to_biochemical_recurrence_for_prostate_cancer,
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
    # Use SimpleITK to read a file
    input_files = (
        glob(str(location / "*.tif"))
        + glob(str(location / "*.tiff"))
        + glob(str(location / "*.mha"))
    )
    result = SimpleITK.ReadImage(input_files[0])

    # Convert it to a Numpy array
    return SimpleITK.GetArrayFromImage(result)


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
