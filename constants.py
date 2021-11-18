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
UNBLOCKED = "Unblocked"
FOUND_USER = "ExistingUser"
SUCCESS = "Success"
BLOCKED = "Blocked"
PRIVATE_REQUEST_ACCEPTED = "PrivateRequestAccepted"
AUTHENTICATED = "AuthenticationSuccessful"


TOO_MANY_ATTEMPTS = "TooManyAttempts"
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
ALREADY_CONNECTED = "AlreadyConnected"
OFFLINE = "Offline"
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
    ALREADY_CONNECTED,
    INACTIVITY,
    BLOCKED,
    UNBLOCKED,
    OFFLINE,
    STOP_PRIVATE,
]

COMMON_EXIT_EXCEPTIONS = [
    LOGOUT,
    ALREADY_ACTIVE,
    INACTIVITY,
    TOO_MANY_ATTEMPTS,
    STOP_PRIVATE,
]

MESSAGES = {
    AUTHENTICATED: "Authentication Successful",
    INVALID_CREDENTIALS: "Invalid Credentials",
    INVALID_COMMAND: "Do not understand this command",
    INACTIVITY: "Inactive for too long. Exiting",
    ALREADY_ACTIVE: "User is already online on another device",
    USER_NOT_FOUND: "User not found",
    LOGOUT: "Logging out",
    BLOCKED: "User is successfully blocked",
    UNBLOCKED: "User is successfully unblocked",
    INVALID_INPUT: "Invalid Input",
    USER_NOT_ONLINE: "User is currently offline",
    OPERATION_NOT_ALLOWED_ON_SELF: "You can not run this operation on your own username",
    ALREADY_BLOCKED: "User is already blocked",
    SUCCESS: "Operation is successfully executed",
    USER_IS_BLOCKED: "You are blocked by the User",
    ALREADY_UNBLOCKED: "User is already unblocked",
    PRIVATE_REQUEST_DENIED: "User has denied your request",
    OFFLINE_MESSAGE_DELIVERED: "User is offline. He will see the message when he/she comes online",
    ALREADY_CONNECTED: "Cannot connect! Already paired with User",
    TOO_MANY_ATTEMPTS: "MAX attempts exceeded. You are blocked Try again in a while",
    OFFLINE: "While you were online, your friends you sent you these",
}

CREDENTIALS_FILE = "credentials.txt"
BUFFER_SIZE = 1024


class CustomExceptions(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def displayMessage(response):

    msg = MESSAGES[response[0]]
    if len(response) == 2:
        msg = lifePotion(msg, response[1])
    print(msg)


def lifePotion(placeholder, user=None):
    string = placeholder
    if user:
        string = string.replace("User", user)

    return string
