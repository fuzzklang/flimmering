def run_sc_script(script):
    """
    Running predefined sc-script from python with bash command.
    The default script (in the flimmering project) fetches csv data (++)
    exported from python, and creates an audio file in Non-real time with it.
    Returns returncode from sh process (subprocess.run)
    """
    import subprocess
    import shutil
    from sys import platform

    sclang = shutil.which('sclang')

    result = subprocess.run([sclang, script])

    return result
