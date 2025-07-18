#!/usr/bin/env bash
# Stop at first error
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Set default container name
DOCKER_IMAGE_TAG="example-algorithm-brs-prediction-final-test"

echo "=+= (Re)build the container"
source "${SCRIPT_DIR}/do_build.sh"

# Check if the image was built successfully
if ! docker image inspect "$DOCKER_IMAGE_TAG" > /dev/null 2>&1; then
    echo "Error: Docker image $DOCKER_IMAGE_TAG was not built successfully."
    exit 1
fi

# Get the build information from the Docker image tag
build_timestamp=$( docker inspect --format='{{ .Created }}' "$DOCKER_IMAGE_TAG")

if [ -z "$build_timestamp" ]; then
    echo "Error: Failed to retrieve build information for container $DOCKER_IMAGE_TAG"
    exit 1
fi

# Format the build information to remove special characters
formatted_build_info=$(echo "$build_timestamp" | sed -E 's/(.*)T(.*)\..*Z/\1_\2/' | sed 's/[-,:]/-/g')

# Set the output filename with timestamp and build information
output_filename="${SCRIPT_DIR}/${DOCKER_IMAGE_TAG}_${formatted_build_info}.tar.gz"

# Save the Docker-container image and gzip it
echo "==+=="
echo "Saving the container image as ${output_filename}. This can take a while."
echo ""

docker save "$DOCKER_IMAGE_TAG" | gzip -c > "$output_filename"
chmod 644 "$output_filename"
echo "Container image saved as ${output_filename}"
echo "==+=="

# Create the tarball of the model directory if it exists
echo "==+=="
output_tarball_name="${SCRIPT_DIR}/nmodel.tar.gz"

if [ -d "${SCRIPT_DIR}/model" ]; then
    echo "Creating the optional tarball as ${output_tarball_name}. This can take a while."
    echo ""
    tar -czf "$output_tarball_name" -C "${SCRIPT_DIR}/model" .
    chmod 644 "$output_tarball_name"
    echo "(Optional) Uploadable tarball was created as ${output_tarball_name}"
else
    echo "Warning: model directory not found at ${SCRIPT_DIR}/model"
    echo "Skipping model tarball creation"
fi
echo "==+=="
