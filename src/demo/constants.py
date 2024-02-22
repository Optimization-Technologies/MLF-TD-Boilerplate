TENANT_ID = "your-tenant-id" #TODO: replace with your tenant id
DATASET_ID = "your-dataset-id" #TODO: replace with your dataset id

# Path to the data files
DATA_FILE_PATH = f"data/"

#Width of the data tables
TABLE_WIDTH_FRACTION = 0.5

#Column names
REG_ID_COL = "registrationId"
DATE_COL = "date"
EMPLOYEE_ID_COL = "employeeId"
PROJECT_ID_COL = "projectId"
DEPARTMENT_ID_COL = "departmentId"
WORK_CATEGORY_COL = "workCategory"
START_TIME_COL = "startTime"
END_TIME_COL = "endTime"
WORK_DURATION_COL = "workDuration"
BREAK_DURATION_COL = "breakDuration"
PUBLIC_HOLIDAY_COL = "publicHoliday"
NUMERICALS_COL = "numericals"
ANOMALY_SCORE_COL = "anomalyScore"
SUBMODEL_ID_COL = "subModelId"
MISSING_COL = "missing"
AGGREGATED_COL = "aggregated"
SIGNIFICANT_FIELDS_COL = "significantFields"
REL_REG_IDS_COL = "relatedRegistrationIds"

#Data types
DATA_TYPES = {
    REG_ID_COL: "string",
    DATE_COL: "string",
    EMPLOYEE_ID_COL: "string",
    PROJECT_ID_COL: "string",
    DEPARTMENT_ID_COL: "string",
    WORK_CATEGORY_COL: "string",
    START_TIME_COL: "float64",
    END_TIME_COL: "float64",
    WORK_DURATION_COL: "float64",
    BREAK_DURATION_COL: "float64",
    PUBLIC_HOLIDAY_COL: "bool",
    NUMERICALS_COL: [],
}

#Info text
TRAIN_TAB_INFO_TEXT = "**On this tab you can explore and visualize the training data \
    that is used to train the anomaly  detection model**"

TEST_TAB_INFO_TEXT = [
    ("**Here you can try out the TimeDetect API**"),
    ("Edit the data by double clicking on the cells."),
    (
        "When you are happy with the data, click the red button below \
    to send the data to the model. Scroll down to see the results."
    ),
]
