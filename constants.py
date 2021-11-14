## CLIENT COMMANDS
MESSAGE = "message"
LOGOUT = "logout"
WHOELSE = "whoelse"

## SERVER CONSTANTS
NEW_USER = "NewUser"
LIST_OF_OTHER_USERS = "ListOfOtherUsers"
FOUND_USER = "ExistingUser"
AUTHENTICATED = "AuthenticationSuccessful"

INVALID_CREDENTIALS = "InvalidCredentials"
INACTIVITY = "Inactive"
ALREADY_ACTIVE = "AlreadyActive"
USER_NOT_FOUND = "UserNotFound"

COMMON_EXCEPTIONS = [USER_NOT_FOUND]
COMMON_EXIT_EXCEPTIONS = [LOGOUT,ALREADY_ACTIVE, INACTIVITY,LOGOUT]

MESSAGES = {
    NEW_USER:"New User",
    FOUND_USER:"Existing User",
    AUTHENTICATED:"Authentication Successful",
    INVALID_CREDENTIALS : "Invalid Credentials",
    INACTIVITY : "Inactive for too long",
    ALREADY_ACTIVE : "The user is already online",
    USER_NOT_FOUND : "User not found",
    LOGOUT:"Logging out"
}

CREDENTIALS_FILE = 'credentials.txt' 
BUFFER_SIZE = 1024

class CustomExceptions(Exception):
    pass