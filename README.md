# MLF-TD-Boilerplate

This project provides a tutorial on integrating with the TimeDetect API.
The documentation for the TimeDetect API can be found [here](https://docs.resolve.visma.com/time-detect/).

## Prerequisites

Before you begin, ensure you have Python installed on your system. Then, install the requirements and run the notebook `TD_Integration_Guide.ipynb`.

## Install the required packages:

```
pip install -r requirements.txt
```

## Launching the TD Demo

To correctly operate the TD Demo, please follow these guidelines:

**1. Generate Data and Train Models**

Before running the demo, you need to either create new data or upload existing data, and train your models.

This can be done by following the steps in the `TD_Integration_Guide.ipynb`. Remember to place your data in a 'data' folder that in the root directory of this project.

**2. Configure the Necessary Variables**

Head to `src/constants.py` and adjust the `TENANT_ID` and `DATASET_ID` to correlate with the identifiers you used in the Tutorial during the data upload and model training phases.

Next, proceed to `src/api/constants.py` and replace `VISMA_CONNECT_CLIENT_ID` with your specific client-ID. Also, ensure you define `VISMA_CONNECT_KEY_STAGE` as an environment variable in your system.

**3. Launch the Application**

With the environment variable correctly set, you can now initiate the application using Streamlit. To achieve this, execute the following command in your terminal:

```bash
streamlit run TD_demo.py
```

## Contact

If you have any questions related to this repository, please contact one of the following:

- [Camilla Dybdal](mailto:camilla.dybdal@visma.com)
- [Henrik Hesle](mailto:henrik.hesle@visma.com)
