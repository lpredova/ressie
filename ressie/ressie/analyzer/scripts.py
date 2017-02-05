import os
import subprocess


class Scripts(object):
    scripts_folder = os.getcwd() + "/data/custom/scripts/"

    def run_defined_scripts(self):

        for f in os.listdir(self.scripts_folder):
            try:
                subprocess.call(self.scripts_folder + f)
            except Exception as e:
                print(e.message)
