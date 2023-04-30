import sys, re
from truckfactor.compute import main
import truckfactor.evo_log_to_csv as eltcsv
# library used to calculate bus size is https://github.com/HelgeCPH/truckfactor

'''
This method is mostly the same from truckfactor.evo_log_to_csv.
The original did not account for the posibility that some lines wouldn't have a match, so
the method had to be patched.
'''
def parse_numstat_block_fixed(commit_line, block):
    if block:
        for line in block:
            m = re.match(eltcsv.LINE_RE, line)
            if m is None:
                csv_line = ",".join((commit_line, "0", "0", ""))
                yield csv_line
            else:
                added, removed, file_name = m.groups()
                if added == "-":
                    added = f'"{added}"'
                if removed == "-":
                    removed = f'"{removed}"'
                csv_line = ",".join((commit_line, added, removed, f'"{file_name}"'))
                yield csv_line
    else:
        csv_line = ",".join((commit_line, "", "", ""))
        yield csv_line

eltcsv.parse_numstat_block = parse_numstat_block_fixed

if __name__ == '__main__':
    try:
        result = main(sys.argv[1].strip('"'), ouputkind=None)[0]
    except:
        result = 0
    print(result)


