#       Status Codes

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#          Error
# ''''''''''''''''''''''''''
# 1 -- Error

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#           CMP
# ''''''''''''''''''''''''''
# 10 -- Local and remote synced
# 11 -- Local ahead of remote
# 12 -- Remote ahead of local
# 13 -- Remote and local diverged
# 14 -- Remote and local unrelated

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#          PUSH
# ''''''''''''''''''''''''''
# 20 -- Push successful

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#         DELETE
# ''''''''''''''''''''''''''
# 30 -- Delete successful

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#          GET
# ''''''''''''''''''''''''''
# 40 -- Get successful 

class Status:
    def __init__(self):
        self.message = {
                "message": "Invalid status"
            }
        self.code = 1

class StatusSynced(Status):
    def __init__(self):
        self.message = {
                "message": "Local and remote synced"
            }
        self.code = 10

class StatusLocalAhead(Status):
    def __init__(self):
        self.message = {
                "message": "Local ahead of remote"
            }
        self.code = 11

class StatusRemoteAhead(Status):
    def __init__(self):
        self.message = {
                "message": "Remote ahead of local"
            }
        self.code = 12

class StatusDivergent(Status):
    def __init__(self):
        self.message = {
                "message": "remote and local diverged"
            }
        self.code = 13

class StatusUnrelated(Status):
    def __init__(self):
        self.message = {
                "message": "remote and local unrelated"
            }
        self.code = 14

class StatusPushSuccessful(Status):
    def __init__(self):
        self.message = {
                "message": "Push successful"
            }
        self.code = 20

class StatusDeleteSuccessful(Status):
    def __init__(self):
        self.message = {
                "message": "Delete successful"
            }
        self.code = 30
