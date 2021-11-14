## CLIENT COMMANDS
MESSAGE = "message"
LOGOUT = "logout"
WHOELSE = "whoelse"
BLOCK = "block"
UNBLOCK = "unblock"

## SERVER CONSTANTS
NEW_USER = "NewUser"
LIST_OF_OTHER_USERS = "ListOfOtherUsers"
FOUND_USER = "ExistingUser"
SUCCESS = "Success"
AUTHENTICATED = "AuthenticationSuccessful"

INVALID_CREDENTIALS = "InvalidCredentials"
INACTIVITY = "Inactive"
ALREADY_ACTIVE = "AlreadyActive"
USER_NOT_FOUND = "UserNotFound"
INVALID_INPUT = "InvalidInput"
OPERATION_NOT_ALLOWED_ON_SELF = "OperationNotAllowedOnSelf"
ALREADY_BLOCKED = "AlreadyBlocked"
USER_IS_BLOCKED = "UserIsBlocked"
ALREADY_UNBLOCKED = "AlreadyUnblocked"
REQUIRES_PRINT = [SUCCESS,USER_NOT_FOUND,INVALID_INPUT,OPERATION_NOT_ALLOWED_ON_SELF,ALREADY_BLOCKED,USER_IS_BLOCKED, ALREADY_UNBLOCKED]

COMMON_EXIT_EXCEPTIONS = [LOGOUT,ALREADY_ACTIVE, INACTIVITY,LOGOUT]

MESSAGES = {
    NEW_USER:"New User",
    FOUND_USER:"Existing User",
    AUTHENTICATED:"Authentication Successful",
    INVALID_CREDENTIALS : "Invalid Credentials",
    INACTIVITY : "Inactive for too long",
    ALREADY_ACTIVE : "The user is already online",
    USER_NOT_FOUND : "User not found",
    LOGOUT:"Logging out",
    INVALID_INPUT:"Invalid Input",
    OPERATION_NOT_ALLOWED_ON_SELF:"You can not run this operation on your own username",
    ALREADY_BLOCKED:"User is already blocked",
    SUCCESS:"Operation is successfully executed",
    USER_IS_BLOCKED:"You are blocked by the user",
    ALREADY_UNBLOCKED:"The user is already unblocked"

}

CREDENTIALS_FILE = 'credentials.txt' 
BUFFER_SIZE = 1024

class CustomExceptions(Exception):
    pass

