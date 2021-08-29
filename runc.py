#!/usr/bin/python3
"""
Automation code
Given Kibanza
Date: 24 August 2021

Automation code that edits and compiles c files for Lab 2, recording time taken.
Each compilation either implements changing bit widths, multi-threading or the use of compiler flags.
After each run, results such as time taken and average time taken to run are displayed. this is used in our report.
"""


import os, sys
import subprocess


#variable storing each elapsed time per run
resp = []


def updateDataType(old="", new="", threaded=False, compilerFlags=False, cflag=""):

    print("Running updateDataType")

    flags = ["lm", "lrt"]
    if compilerFlags:
        flags.append(cflag)

    c = " -".join(flags)
    c = "CFLAGS = -"+ c
    

    # simply changing bit widths
    if (threaded==False):

        content = ""

        with open("makefile", "r") as f:
            content = f.readlines()
            f.close()

        content[2] = c

        #if it's a __fp16
        if (old =="__fp16"):
            #remove -mfp16-format=-eee

            content[11] = content[11].replace("$(CFLAGS) -mfp16-format=ieee", "$(CFLAGS)")
            content[12] = content[12].replace("$(CFLAGS) -mfp16-format=ieee", "$(CFLAGS)")

        elif (new == "__fp16"):
            # add -mfp16-format=ieee to $(CFLAGS)
            
            content[11] = content[11].replace("$(CFLAGS)", "$(CFLAGS) -mfp16-format=ieee")
            content[12] = content[12].replace("$(CFLAGS)", "$(CFLAGS) -mfp16-format=ieee")

        with open("makefile", "w") as f:
            f.writelines(content)
            f.close()
            


        #CHeterodyning file
        content = ""
        with open("src/CHeterodyning.c", "r") as f:
            content = f.read()
            f.close()

        content = content.replace(old, new)

        with open("src/CHeterodyning.c", "w") as f:
            f.write(content)
            f.close()

        #globals.h file
        content = ""
        with open("src/globals.h", "r") as f:
            content = f.read()
            f.close()

        content = content.replace(old, new)

        with open("src/globals.h", "w") as f:
            f.write(content)
            f.close()

    elif (threaded):
        content = ""

        with open("src/CHeterodyning_threaded.h", "r") as f:
            content = f.readlines()
            f.close()

        content[2] = c

        content[14] = "#define Thread_Count " + new

        with open("src/CHeterodyning_threaded.h", "w") as f:
            f.writelines(content)
            f.close()






#for this program to run, user has to write the following
#python3 runc.py -n <no. of times to run these files> [-c] [-t] 
# -c means implement compiler flags
# -t means implement threading
# -n means no of times to iterate a certain variable

# -h command is for help
if (sys.argv.count("-h")):
    o = "Welcome to Given & Bertha's Automation Code"
    print(o)
    print("="*len(o))
    print("Some useful information you should know:\n")
    print("python3 runc.py -n <no. of times to run these files> [-c] [-t]")
    print("-c means implement compiler flags. c can be used in combination with '-t'")
    print("-t means implement threading")
    print("-n means no of times to iterate a certain variable. this is always required")
    print("\nEnjoy your day.")

#this is why we always expect to have 5 parameters, counted after the python3 keyword
elif (len(sys.argv) in [3,4,5]):

    #next we check that both -f and -n arguments are passed
    if (sys.argv.count("-n")>0):

        try:
            
            #here, we try parsing the arguments, hence using the try catch block
            n = int(sys.argv[sys.argv.index("-n")+1])

            #check if t is a parameter

            command = "make"

            additional = "make run"

            compiler_flags = False

            if (sys.argv.count("-t")>0):
                command = "make threaded"
                additional = "make run_threaded"

            if (sys.argv.count("-c")>0):
                compiler_flags = True
                print("compiler flags in the building!")                

            #if the params above are valid, we now begin to loop n times, running the file at each iteration
            
            data_types = []
            if additional=="make run_threaded":
                print("Running threaded version")
                data_types = ["2", "4", "8", "16", "32", "1"]
                past = "1"
            else:
                print("Running Non-threaded")
                data_types = ["double", "__fp16", "float"]
                past = "float"

            c_flags = ["O0", "O1","O2", "O3", "Ofast", "Os", "Og", "funroll-loops"]

            count = 0
            c_times = []

            if compiler_flags==True:
                for c in range(len(c_flags)):
                    for i in range(len(data_types)):
                        tr = additional=="make run_threaded"
                        updateDataType(past, data_types[i], threaded=tr, compilerFlags=True, cflag=c_flags[c] )

                        for o in range(n):

                            count+=1
                            print(count)
                            
                            # make file
                            res = command
                            res = subprocess.getoutput(res)

                            # clear console
                            subprocess.getoutput("clear")

                            #run the compiled file

                            res = additional
                            res = subprocess.getoutput(res)

                            # clear console
                            subprocess.getoutput("clear")


                            #parsing the elapsed time data
                            res = res[res.index("Time") : ]

                            # Time: 211.642441 ms
                            res = res.split(" ")

                            # if not threaded
                            # [Time:, 211.642441, ms]
                            #parsing hours, minutes and seconds

                            if additional=="make run":
                                s = float( res[1] )
                            
                            #if threaded
                            # Time taken for threads to run = 16.2098 ms
                            elif additional=="make run_threaded":
                                s = float( res[7] )

                            #converting the above time to seconds and storing it in resp array
                            resp.append(s)

                            print("done ...")


                        
                        past = data_types[i]
                    c_times.append({
                        "resp": resp,
                        "c_flag": c_flags[c]
                    })
            else:
                for i in range(len(data_types)):
                    tr = additional=="make run_threaded"
                    updateDataType(past, data_types[i], threaded=tr)

                    for o in range(n):

                        count+=1
                        print(count)
                        
                        # make file
                        res = command
                        res = subprocess.getoutput(res)

                        # clear console
                        subprocess.getoutput("clear")

                        #run the compiled file

                        res = additional
                        res = subprocess.getoutput(res)

                        # clear console
                        subprocess.getoutput("clear")


                        #parsing the elapsed time data
                        res = res[res.index("Time") : ]

                        # Time: 211.642441 ms
                        res = res.split(" ")

                        # if not threaded
                        # [Time:, 211.642441, ms]
                        #parsing hours, minutes and seconds

                        if additional=="make run":
                            s = float( res[1] )
                        
                        #if threaded
                        # Time taken for threads to run = 16.2098 ms
                        elif additional=="make run_threaded":
                            s = float( res[7] )

                        #converting the above time to seconds and storing it in resp array
                        resp.append(s)

                        print("done ...")

                
                    
                    past = data_types[i]

            
            if compiler_flags:
                for cf in c_times:
                    printContent(cf["resp"], cf["c_flag"])
            else:
                printContent(resp)

            print("Done")
        except Exception as e:
            print(e)
            print("invalid arguments. make sure that -f is a valid file and -n is an integer")
    
    else:
        print("make sure you pass the correct parameters")
else:
    print("invalid number of arguments")


def printContent(nResp, flags=""):
    avg = 0
    summ = 0
    
    miniSum = 0
    t_ype = -1

    if (flags!=""):
        print("The following flag was used in this run: "+ flags)

    count = len(nResp)

    #looping to sum the elapsed times
    for i in range(count):
        print("Elapsed time for run %d = %fms" % (i+1, nResp[i]))
        if ((i+1) % n)==0:
            miniSum += nResp[i]
            t_ype+=1
            print("\n---------- Average Time for the Above (%s) ----------\n" %(data_types[t_ype]))
            print("=%fms\n\n" % (miniSum/n))
            miniSum = 0
        else:
            miniSum+= nResp[i]
        summ += resp[i]

    #using calculated sum to get average elapsed time in seconds
    avg = summ/float(count)

    print("\n"*3)
    print("="*50)

    print("Average time taken = %f ms" % avg)

exit(0)

