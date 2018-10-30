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


def generate_state_report(State_list, stateReport):
    """
    Generate top10 states output file
    :param State_list: state list of certified H1B
    :param stateReport: output file of top10 states
    :return: None
    """
    total_num_state = len(State_list)
    State_count = Counter(State_list)
    State_count = sorted(State_count.iteritems(), key=lambda (k, v): (-v, k))
    top10_states = State_count[0:10]
    top10_states = [list(state_count) for state_count in top10_states]
    for item in top10_states:
        percentage = round(float(item[1])/float(total_num_state)*100, 1)
        item.append(percentage)
    with open(stateReport, 'w+') as resultFile:
        resultFile.write("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE" + "\n")
        for sublist in top10_states:
            line = "{};{};{}%\n".format(sublist[0], sublist[1], sublist[2])
            resultFile.write(line)
    pass


def generate_job_report(SOC_list, occupationReport):
    """
    Generate top 10 occupation output file.
    :param SOC_list: Occupation list(SOC names)
    :param occupationReport: output file for top10 occupation
    :return: None
    """
    total_num_jobs = len(SOC_list)
    job_count = Counter(SOC_list)
    job_count = sorted(job_count.iteritems(), key=lambda (k, v): (-v, k))
    top10_jobs = job_count[0:10]
    top10_jobs = [list(job_count) for job_count in top10_jobs]
    for item in top10_jobs:
        percentage = round(float(item[1]) / float(total_num_jobs) * 100, 1)
        item.append(percentage)
    with open(occupationReport, 'w+') as resultFile:
        resultFile.write("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE" + "\n")
        for sublist in top10_jobs:
            line = "{};{};{}%\n".format(sublist[0], sublist[1], sublist[2])
            resultFile.write(line)
    pass


def main():
    if len(sys.argv) != 4:
        print 'You failed to provide input and output files!'
        sys.exit(1)   # abort because of error
    else:
        inputFile = sys.argv[1]
        occupation_out = sys.argv[2]
        top_state_out = sys.argv[3]
        SOC_name, States = readfile(inputFile)
        generate_job_report(SOC_name, occupation_out)
        generate_state_report(States, top_state_out)
    pass


if __name__ == "__main__":
    main()



#python ./src/h1b_counting.py ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt
#python ./src/h1b_counting.py ./input/sample_2k_2015.csv ./output/top_10_occupations.txt ./output/top_10_states.txt
#python ./src/h1b_counting.py ./input/sample_2014.csv ./output/top_10_occupations.txt ./output/top_10_states.txt
