#Set by you
VISMA_CONNECT_CLIENT_ID = "your-client-id" #TODO: replace with your client id
VISMA_CONNECT_KEY_STAGE = "VISMA_CONNECT_KEY_STAGE" #Set by you as an environment variable
 
#API constants
BASE_URL = "https://api.machine-learning-factory.stage.visma.com/td"
VISMA_CONNECT_TOKEN_URL = "https://connect.identity.stagaws.visma.com/connect/token"
VISMA_CONNECT_API_SCOPE = "machine-learning-factory-api-stage:td"
REG_FIELDS = [
    "registrationId",
    "date",
    "employeeId",
    "projectId",
    "departmentId",
    "workCategory",
    "startTime",
    "endTime",
    "workDuration",
    "breakDuration",
    "publicHoliday",
    "numericals",
]
MODEL_BUCKET = "mlf-td-trainer-model-bucket-stage"

