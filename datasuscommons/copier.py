
class Copier():
#	def __init__(self, *args):
	def copy_file(self, file_name: str, from_folder: str, to_folder: str, *extra_args) -> bool:
		pass

		
	def copy_files(self, file_names: list, from_folder: str, to_folder: str, *extra_args) -> bool:
		pass
	
	def copy_folder(self, from_folder: str, to_folder: str, *extra_args) -> bool:
		pass

import shutil
import os

class LocalCopier(Copier):
    def copy_file(self, file_name: str, from_folder: str, to_folder: str, copy_stats = False ) -> bool:
        file_full = os.path.join(from_folder, file_name)
        result = shutil.copy(file_full, to_folder)
        if copy_stats:
            shutil.copystat(file_name, os.path.join(to_folder, file_name) )
        #print("\nLocal Copier" + str(copy_stats) )
        return str(result).endswith(file_name)
