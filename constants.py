## CLIENT COMMANDS
MESSAGE = "message"
LOGOUT = "logout"
WHOELSE = "whoelse"
WHOELSESINCE = "whoelsesince"
BLOCK = "block"
UNBLOCK = "unblock"
START_PRIVATE = "startprivate"
PRIVATE = "private"
STOP_PRIVATE = "stopprivate"
BROADCAST = "broadcast"

## SERVER CONSTANTS
NOTIFICATION = "Notification"
NEW_USER = "NewUser"
PRIVATE_REQUEST = "PrivateRequest"
# INITIATE_PRIVATE = "InitiatePrivate"
LIST_OF_OTHER_USERS = "ListOfOtherUsers"
LIST_OF_OTHER_USERS_SINCE = "ListOfOtherUsersSince"
FOUND_USER = "ExistingUser"
SUCCESS = "Success"
PRIVATE_REQUEST_ACCEPTED = "PrivateRequestAccepted"
AUTHENTICATED = "AuthenticationSuccessful"


INVALID_CREDENTIALS = "InvalidCredentials"
INACTIVITY = "Inactive"
PRIVATE_REQUEST_DENIED = "PrivateRequestDenied"
ALREADY_ACTIVE = "AlreadyActive"
USER_NOT_FOUND = "UserNotFound"
USER_NOT_ONLINE = "UserNotOnline"
INVALID_INPUT = "InvalidInput"
OPERATION_NOT_ALLOWED_ON_SELF = "OperationNotAllowedOnSelf"
ALREADY_BLOCKED = "AlreadyBlocked"
USER_IS_BLOCKED = "UserIsBlocked"
ALREADY_UNBLOCKED = "AlreadyUnblocked"
INVALID_COMMAND = "INVALID COMMAND"
OFFLINE_MESSAGE_DELIVERED = "OfflineMessageDelivered"

REQUIRES_PRINT = [
    SUCCESS,
    USER_NOT_FOUND,
    INVALID_INPUT,
    OPERATION_NOT_ALLOWED_ON_SELF,
    ALREADY_BLOCKED,
    USER_IS_BLOCKED,
    ALREADY_UNBLOCKED,
    PRIVATE_REQUEST_DENIED,
    USER_NOT_ONLINE,
    OFFLINE_MESSAGE_DELIVERED,
    INVALID_COMMAND,
]

COMMON_EXIT_EXCEPTIONS = [
    LOGOUT,
    ALREADY_ACTIVE,
    INACTIVITY,
]

MESSAGES = {
    NEW_USER: "New User",
    FOUND_USER: "Existing User",
    AUTHENTICATED: "Authentication Successful",
    INVALID_CREDENTIALS: "Invalid Credentials",
    INVALID_COMMAND: "Do not understand this command",
    INACTIVITY: "Inactive for too long",
    ALREADY_ACTIVE: "The user is already online",
    USER_NOT_FOUND: "User not found",
    LOGOUT: "Logging out",
    INVALID_INPUT: "Invalid Input",
    USER_NOT_ONLINE: "The selected user is currently offline",
    OPERATION_NOT_ALLOWED_ON_SELF: "You can not run this operation on your own username",
    ALREADY_BLOCKED: "User is already blocked",
    SUCCESS: "Operation is successfully executed",
    USER_IS_BLOCKED: "You are blocked by the user",
    ALREADY_UNBLOCKED: "The user is already unblocked",
    PRIVATE_REQUEST_DENIED: "The user has denied your request",
    OFFLINE_MESSAGE_DELIVERED: "The user is offline. He will see the message when he/she comes online",
}

CREDENTIALS_FILE = "credentials.txt"
BUFFER_SIZE = 1024


class CustomExceptions(Exception):
    pass


def lifePotion(placeholder, user=None):
    string = placeholder
    if user:
        string = string.replace("User", user)

    return string
