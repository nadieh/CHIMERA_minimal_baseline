# CHIMERA Baseline Template

This repository provides a **minimal working template** for participating in the [CHIMERA Challenge](https://chimera.grand-challenge.org/).  
It serves as a **starting point** for your own submission and implements the required boilerplate to run across all tasks in the challenge.

---

## 📁 Structure

Each task follows this structure:

- `inference.py`: Main entry point for processing inputs and generating outputs.
- `model/`: Placeholder for model-related resources.
  - `README.md`: Instructions for uploading or including models.
  - `a_tarball_subdirectory/`: Example subdirectory for tarball-based resources.
- `resources/`: Placeholder for any additional resources.
- `requirements.in` and `requirements.txt`: Define the Python dependencies for the project.
- `Dockerfile`: Specifies the container environment for running the algorithm.
- `do_build.sh`: Script to build the Docker container.
- `do_test_run.sh`: Script to test the container locally.
- `do_save.sh`: Script to save the container image and optional tarball for upload.

---

## 🚀 Getting Started

**System requirements:**  
- Linux-based OS (e.g., Ubuntu 22.04)  
- Python 3.10+  
- Docker installed

Depending on your preferred development setup, you can follow one of our tutorials:

- **Local development with Docker**
- **Local development with Python virtual environment** *(experimental)*

> **Note:** We're working on adding instructions for providing the script with the necessary inputs — stay tuned!

⚠️ The local Python virtual environment workflow does **not** support creating a Docker container suitable for submission to Grand Challenge. For that, please follow the Docker-based workflow.

---

## 🛠️ Customization

- Modify `inference.py` to implement your own feature extraction or prediction logic.
- Add your model weights to the `model/` directory or upload them as a tarball to Grand Challenge.
- Update `requirements.in` to include any additional Python dependencies.
- Regenerate `requirements.txt` using:

  ```bash
  pip-compile requirements.in
