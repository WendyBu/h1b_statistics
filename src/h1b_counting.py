# data source: H-1B data from United State Department of Labor
# calculate two metrics: Top 10 Occupations and Top 10 States for certified H-1B visa applications.
# Usage: python ./src/h1b_counting.py ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt


import sys, csv
from collections import Counter


def readfile(inputFile):
    """
    Read input file
    :param inputFile: argv[1], input file
    :return: the occupation list, state list of certified H1B
    """
    Certified = []
    SOC_Name = []
    State = []
    try:
        with open(inputFile, "r") as f:
            reader = csv.DictReader(f, delimiter=';')  # read rows into a dictionary format
            i = reader.fieldnames                                  # read csv header
            s = [colname for colname in i if 'STATUS' in colname]  # field name of status: STATUS; CASE_STATUS
            for row in reader:
                if row[s[0]] == "CERTIFIED":
                    Certified.append(row)  # store the certified record in Certified list
            for record in Certified:
                if "SOC_NAME" in record:
                    SOC_Name.append(record["SOC_NAME"])      # Occupations: SOC_NAME; LCA_CASE_SOC_NAME
                elif "LCA_CASE_SOC_NAME" in record:
                    SOC_Name.append(record["LCA_CASE_SOC_NAME"])

                if "WORKSITE_STATE" in record:
                    State.append(record["WORKSITE_STATE"])   # State: WORKSITE_STATE; LCA_CASE_WORKLOC1_STATE
                elif "LCA_CASE_WORKLOC1_STATE" in record:
                    State.append(record["LCA_CASE_WORKLOC1_STATE"])
    except:
        print "Reading file failed!"
    return SOC_Name, State


def get_top10(inputList):
    """
    get top 10 most common element in a list
    :param inputList: a list
    :return: top 10 element with counts and percentage
    """
    total_num_element = len(inputList)
    key_count = Counter(inputList)
    key_count = sorted(key_count.iteritems(), key=lambda (k, v): (-v, k))  # sort by value first, then sort key by alphabeta
    top10_element = key_count[0:10]
    top10_element = [list(key_count) for key_count in top10_element]
    for item in top10_element:
        percentage = round(float(item[1]) / float(total_num_element) * 100, 1)
        item.append(percentage)
    return top10_element


def generate_state_report(top10_State, stateReport):
    """
    Generate top10 states output file
    :param State_list: top10 states, with case num and percentage
    :param stateReport: output file of top10 states
    :return: None
    """
    with open(stateReport, 'w+') as resultFile:
        resultFile.write("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE" + "\n")
        for sublist in top10_State:
            line = "{};{};{}%\n".format(sublist[0], sublist[1], sublist[2])
            resultFile.write(line)
    pass


def generate_job_report(top10_SOC, occupationReport):
    """
    Generate top 10 occupation output file.
    :param SOC_list: top 10 Occupation, with case num and percentage
    :param occupationReport: output file for top10 occupation
    :return: None
    """
    with open(occupationReport, 'w+') as resultFile:
        resultFile.write("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE" + "\n")
        for sublist in top10_SOC:
            line = "{};{};{}%\n".format(sublist[0], sublist[1], sublist[2])
            resultFile.write(line)
    pass


def main():
    if len(sys.argv) != 4:
        print 'You failed to provide input and output files!'
        sys.exit(1)   # abort because of error
    else:
        inputFile = sys.argv[1]
        occupation_output = sys.argv[2]
        top_state_output = sys.argv[3]
        SOC_name, States = readfile(inputFile)  #read input file, get SOC_name list and State list.
        top10_SOC = get_top10(SOC_name)
        top10_State = get_top10(States)
        generate_job_report(top10_SOC, occupation_output)
        generate_state_report(top10_State, top_state_output)
    pass


if __name__ == "__main__":
    main()
