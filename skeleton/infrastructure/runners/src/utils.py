import shutil

def resolve_cmd(cmd):
    # npm is npm.cmd on windows!
    # use which to check if npm.cmd
    return shutil.which(cmd) or cmd
