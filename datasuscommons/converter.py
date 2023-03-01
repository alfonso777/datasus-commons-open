import subprocess
import os
from abc import ABC, abstractmethod
from simpledbf import Dbf5
import dbfread
import pandas as pd
import re


class DBCFileConverter():
    @classmethod
    def convert_dbc_to_dbf(cls, source_file_name: str, source_folder: str, target_folder:str, extension_sensitive: bool = False) -> bool:
        if source_file_name.split('.')[1].lower() != "dbc":
            raise ValueError(f"File type not supported: {source_file_name}")
        source_file = os.path.join(source_folder, source_file_name)
        target_file = os.path.join(target_folder,  re.sub('.dbc', '.dbf', source_file_name , flags = re.S if extension_sensitive else re.I) )
        if os.path.exists(target_file):
            return True
        cmd_conversion = f"{os.path.join('.','tmpinstalls','blast-dbf','blast-dbf')} {source_file} {target_file}"
        
        result = subprocess.check_output(cmd_conversion, shell=True)
        #print(f"Result: {result}")
        return os.path.exists(target_file)
    
    @classmethod
    def convert_dbc_files_to_dbf(cls, source_file_names: list, source_folder: str, target_folder:str ) -> list:
        processed_files_failed = []
        for source_file_name in source_file_names:
            if not cls.convert_dbc_to_dbf(source_file_name, source_folder, target_folder):
                processed_files_failed.append(source_file_name)
        return processed_files_failed

class AbstractDBFReader(ABC):
    @abstractmethod
    def load_dbf(self, dbf_file_path: str, encoding = 'ISO-8859-1'):
        pass

    @abstractmethod
    def convert_dbf_to_dataframe(self, source_file_name: str, source_folder: str, encoding = 'ISO-8859-1'):
        pass

#Based on simpledbf package
class SimpleDBFReader(AbstractDBFReader):
    def load_dbf(self, dbf_file_path: str, encoding='ISO-8859-1'):
        if dbf_file_path.split('.')[1].lower() != "dbf":
            raise ValueError(f"File type not supported: {dbf_file_path}")
        dbf_object = Dbf5(dbf_file_path, codec=encoding)
        return dbf_object

    def convert_dbf_to_dataframe(self, source_file_name: str, source_folder: str, encoding = 'ISO-8859-1'):
        if source_file_name.split('.')[1].lower() != "dbf":
            raise ValueError(f"File type not supported: {source_file_name}")
        source_file = os.path.join(source_folder, source_file_name)
        dbf_object = self.load_dbf(source_file, encoding)
        df = dbf_object.to_dataframe()
        return df

#base on dbfread package
class DBFReader(AbstractDBFReader):
    def load_dbf(self, dbf_file_path: str, encoding='ISO-8859-1'):
        if dbf_file_path.split('.')[1].lower() != "dbf":
            raise ValueError(f"File type not supported: {dbf_file_path}")
        table = dbfread.DBF(dbf_file_path, encoding=encoding)
        return table

    def convert_dbf_to_dataframe(self, source_file_name: str, source_folder: str, encoding = 'ISO-8859-1'):
        if source_file_name.split('.')[1].lower() != "dbf":
            raise ValueError(f"File type not supported: {source_file_name}")
        source_file = os.path.join(source_folder, source_file_name)
        table = self.load_dbf(source_file, encoding)
        df = pd.DataFrame(table)
        return df


class DBFFileConverter():
    dbf_reader: AbstractDBFReader
    def __init__(self, dbf_reader: AbstractDBFReader) -> None:
        self.set_dbf_reader(dbf_reader)
    
    def set_dbf_reader(self, dbf_reader: AbstractDBFReader):
        self.dbf_reader = dbf_reader

    def convert_dbf_to_csv(self, source_file_name: str, source_folder: str, target_folder:str, sep = '\t', encoding = 'ISO-8859-1') -> bool:
        df = self.dbf_reader.convert_dbf_to_dataframe(source_file_name, source_folder, encoding)
        #dbf_object.to_csv(target_file)
        target_file = os.path.join(target_folder, source_file_name.replace(".dbf", ".csv"))
        df.to_csv(target_file, sep=sep)
        return os.path.exists(target_file)

    def convert_dbf_to_parquet(self, source_file_name: str, source_folder: str, target_folder:str, encoding = 'ISO-8859-1' ) -> bool:
        target_file = os.path.join(target_folder, source_file_name.replace(".dbf", ".parquet"))
        if os.path.exists(target_file):
            return True
        df = self.dbf_reader.convert_dbf_to_dataframe(source_file_name, source_folder, encoding = encoding)
        df.to_parquet(target_file)
        return os.path.exists(target_file)
