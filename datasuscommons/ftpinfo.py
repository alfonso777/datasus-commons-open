from .commons import UF_MAP,DATASUS_SUBSYSTEM, DATASUS_SYSTEM, DATASUS_REGEX_SYSTEM
from datetime import datetime
import re

def ftpsus_get_components_from_line(ftp_line, system: DATASUS_SYSTEM = None, subsystem: DATASUS_SUBSYSTEM = None):
    try:
        entities = ftp_line.split()
        file_name = entities[3]
        date_hour = datetime.strptime(entities[0]+' '+ entities[1], "%m-%d-%y %I:%M%p")
        size_bytes = int(entities[2])
        size_mb = round( size_bytes/(1024*1024) , 7)
        splitted_name = file_name.split('.')
        if len(splitted_name) > 1:
            name, extension = ( '.'.join(splitted_name[0:-1]), splitted_name[-1])
        else:
            name, extension = ( file_name, '' )

        regex_by_system = DATASUS_REGEX_SYSTEM.get_name_regex_by_system(system, subsystem)
        match = re.findall(regex_by_system, name) if regex_by_system else None
        core_name, ref_date, sufix = match[0] if match else (name,'','')

        return {
            'file_name': file_name,
            'name': name,
            'modification_datetime': date_hour.strftime("%Y-%m-%d %H:%M"), 
            'modification_date': date_hour.strftime("%Y-%m-%d"),
            'modification_hour': date_hour.strftime("%H:%M"),
            'size_mb': size_mb,
            'size': size_bytes,
            'core_name': core_name[0:-1] if core_name.endswith('_') else core_name,
            'ref_date':  f"20{ref_date}" if len(ref_date) == 4 else ref_date,
            'ref_year':  f"20{ref_date[0:2]}" if len(ref_date) == 4 else ( ref_date[0:4] if len(ref_date) == 6 else ''),
            'ref_month': ref_date[-2:] if len(ref_date) == 4 or len(ref_date) == 6 else '',
            'sufix':  sufix,
            'extension': extension
        }
    except Exception as e:
        print(f"Exception at line => {ftp_line}")
        #raise ValueError()
        return None


def ftpsus_get_full_components_from_line(ftp_line, system: DATASUS_SYSTEM = None, subsystem: DATASUS_SUBSYSTEM = None):
    try:
        components_entry = ftpsus_get_components_from_line(ftp_line, system, subsystem)
        if not components_entry:
            return None 
        regex_subsystem_uf = DATASUS_REGEX_SYSTEM.get_subsystem_uf_regex_by_system(system, subsystem)
        match = re.findall(regex_subsystem_uf, components_entry['core_name']) if regex_subsystem_uf else None
        found_subsystem, found_uf = match[0] if match else ('','')

        components_entry['subsystem']   = found_subsystem[0:-1] if found_subsystem.endswith('_') or found_subsystem.endswith('-') else found_subsystem
        components_entry['uf']          = found_uf
        return components_entry
    except Exception as e:
        print(f"Exception at line => {ftp_line}")
        #raise ValueError()
        raise e
        return None

def ftpsus_entry_info_list(ftp, file_pattern,  fn_line_handler = ftpsus_get_full_components_from_line, system: DATASUS_SYSTEM = None, subsystem: DATASUS_SUBSYSTEM = None ):
    lines = []
    ftp.retrlines(f'LIST {file_pattern}', lines.append)
    #print("lines: " + str(lines))
    return list(filter( None, [ fn_line_handler(line, system, subsystem) for line in lines]))
