from datasuscommons.ftpinfo import *
import operator

def get_sus_ftp_info(sus_target_path, sus_system, file_pattern = '',
                    base = '', uf = '', year_month_range = '',
                    ftp_host = 'ftp.datasus.gov.br'):
    print(f"Get info from SUS system {sus_system} at path: {ftp_host}{sus_target_path}")
    from ftplib import FTP
    ftp = FTP(ftp_host)
    ftp.login()
    ftp.cwd(sus_target_path)

    if not file_pattern:
        file_pattern = base + uf + year_month_range + "*"
    print(f"File pattern: {file_pattern}")
    components_info = ftpsus_entry_info_list(ftp, file_pattern)
    return components_info

def ftpsus_group_entries_by(entries_with_components: list, field_index, index_items= 'items', sorted_reverse = False):
    grouped_entries = {}
    for entry in entries_with_components:
        group_key = entry[field_index]
        if grouped_entries.get(group_key) is not None:
           grouped_entries[group_key].append(entry)
        else:
           grouped_entries[group_key] = [entry]
    list_grouped_entries = [ {field_index: group, index_items: items} for group, items in grouped_entries.items() ]
    return sorted(list_grouped_entries, key = lambda entry: entry[field_index], reverse = sorted_reverse)


def ftpsus_filter_entries(entries_with_components: list, function_filter, index, ref_value):
    return list(filter(lambda entry: function_filter(entry, index, ref_value), entries_with_components))


def ftpsus_filter_entries_by_field(entries_with_components: list, field_index: str, field_ref_value, op: operator):
    return list(filter(lambda entry: op(entry[field_index], field_ref_value) , entries_with_components))

def ftpsus_get_equal_entries(entries_with_components: list, field_index, ref_value):
    return ftpsus_filter_entries_by_field(entries_with_components, field_index, ref_value, operator.eq)

def ftpsus_get_entries_contains(entries_with_components: list, field_index, ref_values):
    return ftpsus_filter_entries(entries_with_components, lambda entry, index, values: operator.contains(values, entry[index]) ,field_index, ref_values)

def ftpsus_get_after_entries(entries_with_components: list, field_index, ref_value):
    return ftpsus_filter_entries_by_field(entries_with_components, field_index, ref_value, operator.gt)

def ftpsus_get_previous_entries(entries_with_components: list, field_index, ref_value):
    return ftpsus_filter_entries_by_field(entries_with_components, field_index, ref_value, operator.lt)

def ftpsus_get_entries_between(entries_with_components: list, field_index, ref_value_from, ref_value_to, closed_interval = True):
    if closed_interval:
        return ftpsus_filter_entries(entries_with_components, lambda entry, index, values: values[0] <= entry[index] <= values[1] , field_index, [ref_value_from, ref_value_to] )
    else:
        return ftpsus_filter_entries(entries_with_components, lambda entry, index, values: values[0] < entry[index] < values[1] , field_index, [ref_value_from, ref_value_to] )
