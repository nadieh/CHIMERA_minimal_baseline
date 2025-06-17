"""
The following is a simple example evaluation method.

It is meant to run within a container. Its steps are as follows:

  1. Read the algorithm output
  2. Associate original algorithm inputs with a ground truths via predictions.json
  3. Calculate metrics by comparing the algorithm output to the ground truth
  4. Repeat for all algorithm jobs that ran for this submission
  5. Aggregate the calculated metrics
  6. Save the metrics to metrics.json

To run it locally, you can call the following bash script:

  ./do_test_run.sh

This will start the evaluation and reads from ./test/input and writes to ./test/output

To save the container and prep it for upload to Grand-Challenge.org you can call:

  ./do_save.sh

Any container that shows the same behaviour will do, this is purely an example of how one COULD do it.

Reference the documentation to get details on the runtime environment on the platform:
https://grand-challenge.org/documentation/runtime-environment/

Happy programming!
"""

import json


import random
from statistics import mean
from pathlib import Path
from pprint import pformat, pprint
from helpers import run_prediction_processing, tree
from sksurv.metrics import concordance_index_censored
import numpy as np
import pandas as pd
INPUT_DIRECTORY = Path("/input")
OUTPUT_DIRECTORY = Path("/output")
GROUND_TRUTH_DIRECTORY = Path("/opt/ml/input/data/ground_truth/a_tarball_subdirectory/ground_truth.csv")



def main():
    print_inputs()

    metrics = {}
    predictions = read_predictions()

    # We now process each algorithm job for this submission
    # Note that the jobs are not in any specific order!
    # We work that out from predictions.json

    metrics["results"] = run_prediction_processing(fn=process, predictions=predictions)

    result_df = pd.DataFrame(metrics["results"])

   
    print("result_df", result_df)

    survival_times = np.array(result_df["case_id_gt_time"])
    events = np.array(result_df["case_id_gt_event"], dtype=bool)
    predicted_times = np.array(result_df["case_id_prediction_years_to_recurrence"])
    print("events, survival_times, predicted_times",events, survival_times, predicted_times)
  
    # Negating the predicted times to convert them into risk scores before calculating the concordance index. 
    # This ensures the concordance index correctly interprets higher scores as lower risk.
    c_index = concordance_index_censored(events, survival_times, -predicted_times)

    print("c_index",c_index)
    

    metrics["aggregates"] = {
        "c_index": c_index[0]
    }
    
    # Make sure to save the metrics
    write_metrics(metrics=metrics)

    return 0


def process(job):
    # The key is a tuple of the slugs of the input sockets
    interface_key = get_interface_key(job)

    # Lookup the handler for this particular set of sockets (i.e. the interface)
    handler = {
        (
            "bladder-cancer-tissue-biopsy-whole-slide-image",
            "bulk-rna-seq-bladder-cancer",
            "chimera-clinical-data-of-bladder-cancer-recurrence",
            "tissue-mask",
        ): process_interf0,
    }[interface_key]

    # Call the handler
    return handler(job)


def process_interf0(
    job,
):
    """Processes a single algorithm job, looking at the outputs"""
    report = "Processing:\n"
    report += pformat(job)
    report += "\n"

    # Firstly, find the location of the results
    location_likelihood_of_bladder_cancer_recurrence = get_file_location(
        job_pk=job["pk"],
        values=job["outputs"],
        slug="likelihood-of-bladder-cancer-recurrence",
    )

    # Secondly, read the results
    result_likelihood_of_bladder_cancer_recurrence = load_json_file(
        location=location_likelihood_of_bladder_cancer_recurrence,
    )

    # Thirdly, retrieve the input file name to match it with your ground truth
    image_name_tissue_mask = get_image_name(
        values=job["inputs"],
        slug="tissue-mask",
    )
    image_name_bladder_cancer_tissue_biopsy_whole_slide_image = get_image_name(
        values=job["inputs"],
        slug="bladder-cancer-tissue-biopsy-whole-slide-image",
    )

    # Fourthly, load your ground truth
    ground_truth_df =  pd.read_csv(GROUND_TRUTH_DIRECTORY, dtype={'case_id': str})


    gt_image_name_df = ground_truth_df[ground_truth_df["case_id"]==image_name_bladder_cancer_tissue_biopsy_whole_slide_image[:-4]]

    print('gt_image_name_df',gt_image_name_df)

 
    gt_image_name_time = gt_image_name_df["time_to_HG_recur_or_FUend"].item()

    print('gt_image_name_time',gt_image_name_time)

    gt_image_name_event = gt_image_name_df["progression"].item()

    print('gt_image_name_event',gt_image_name_event)




    # Finally, calculate by comparing the ground truth to the actual results
    return {
        "case_id": image_name_bladder_cancer_tissue_biopsy_whole_slide_image[:-4],
        "case_id_gt_time": gt_image_name_time, 
        "case_id_gt_event": gt_image_name_event,
        "case_id_prediction_years_to_recurrence": result_likelihood_of_bladder_cancer_recurrence
    }


def print_inputs():
    # Just for convenience, in the logs you can then see what files you have to work with
    print("Input Files:")
    for line in tree(INPUT_DIRECTORY):
        print(line)
    print("")


def read_predictions():
    # The prediction file tells us the location of the users' predictions
    return load_json_file(location=INPUT_DIRECTORY / "predictions.json")


def get_interface_key(job):
    # Each interface has a unique key that is the set of socket slugs given as input
    socket_slugs = [sv["interface"]["slug"] for sv in job["inputs"]]
    return tuple(sorted(socket_slugs))


def get_image_name(*, values, slug):
    # This tells us the user-provided name of the input or output image
    for value in values:
        if value["interface"]["slug"] == slug:
            return value["image"]["name"]

    raise RuntimeError(f"Image with interface {slug} not found!")


def get_interface_relative_path(*, values, slug):
    # Gets the location of the interface relative to the input or output
    for value in values:
        if value["interface"]["slug"] == slug:
            return value["interface"]["relative_path"]

    raise RuntimeError(f"Value with interface {slug} not found!")


def get_file_location(*, job_pk, values, slug):
    # Where a job's output file will be located in the evaluation container
    relative_path = get_interface_relative_path(values=values, slug=slug)
    return INPUT_DIRECTORY / job_pk / "output" / relative_path


def load_json_file(*, location):
    # Reads a json file
    with open(location) as f:
        return json.loads(f.read())


def write_metrics(*, metrics):
    # Write a json document used for ranking results on the leaderboard
    write_json_file(location=OUTPUT_DIRECTORY / "metrics.json", content=metrics)


def write_json_file(*, location, content):
    # Writes a json file
    with open(location, "w") as f:
        f.write(json.dumps(content, indent=4))


if __name__ == "__main__":
    raise SystemExit(main())
