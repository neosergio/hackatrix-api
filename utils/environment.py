from os import environ


# Function to get environment variables value if they exist.
def env(e, d):
    if e in environ:
        return environ[e]
    else:
        return d
