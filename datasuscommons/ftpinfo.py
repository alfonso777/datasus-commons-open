from datetime import datetime

def ftpsus_get_components_from_line(ftp_line):
    import re
    try:
        entities = ftp_line.split()
        file_name = entities[3]
        date_hour = datetime.strptime(entities[0]+' '+ entities[1], "%m-%d-%y %I:%M%p")
        size = round( int(entities[2])/(1024*1024) , 4)
        #return (entities[3], fn_get_file_refdate(), date_hour.strftime("%Y-%m-%d"), date_hour.strftime("%H:%M"), size)
        name, extension = file_name.split('.')
        #print(f"name: {name}")
        #base, uf, ref_date, year, month = name[0:2], name[2:4], ('20' + name[-4:]), name[-4:-2], name[-2:]
        components = re.findall(r'(\w{2,3})(\w{2})(\d{4})(.?)', name)
        base, uf, ref_date, seq = components[0]
        return {
            'file_name': file_name,
            'name': name,
            'extension': extension,
            'sequence':  seq,
            'modification_datetime': date_hour.strftime("%Y-%m-%d %H:%M"), 
            'modification_date': date_hour.strftime("%Y-%m-%d"),
            'modification_hour': date_hour.strftime("%H:%M"),
            'size_mb': size,
            'base': base,
            'uf':   uf,
            'ref_date': '20' + ref_date,
            'ref_year': '20' + ref_date[0:2],
            'ref_month': ref_date[2:4]
        }
    except Exception as e:
        print(f"Exception at line => {ftp_line}")
        #raise ValueError()
        return None

def ftpsus_entry_info_list(ftp, file_pattern,  fn_line_handler = ftpsus_get_components_from_line ):
    lines = []
    ftp.retrlines(f'LIST {file_pattern}', lines.append)
    #print("lines: " + str(lines))
    return list(filter( None, [ fn_line_handler(line) for line in lines]))
