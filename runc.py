import os, sys
import subprocess


#variable storing each elapsed time per run
resp = []


def updateDataType(old, new, threaded=False):

    if (threaded==False):

        content = ""

        with open("makefile", "r") as f:
            content = f.readlines()
            f.close()

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

        





#for this program to run, user has to write the following
#python3 runfiles.py -n <no. of times to run these files> -c [-t] 
#this is why we always expect to have 5 parameters, counted after the python3 keyword
if (len(sys.argv) in [4,5]):

    #next we check that both -f and -n arguments are passed
    if (sys.argv.count("-c")>0 and sys.argv.count("-n")>0):

        try:
            
            #here, we try parsing the arguments, hence using the try catch block
            n = int(sys.argv[sys.argv.index("-n")+1])

            #check if t is a parameter

            command = "make"

            additional = "run"

            if (sys.argv.count("-t")>0):
                additional = "threaded"

            #if the params above are valid, we now begin to loop n times, running the file at each iteration
            
            data_types = ["double", "__fp16", "float"]

            past = "float"

            count = 0

            for i in range(3):

                updateDataType(past, data_types[i])

                for o in range(n):

                    count+=1
                    
                    # make file
                    res = command
                    res = subprocess.getoutput(res)

                    #run the compiled file

                    res = command + " " + additional
                    res = subprocess.getoutput(res)

                    #parsing the elapsed time data
                    res = res[res.index("Time: ") : ]
                    
                    # Time: 211.642441 ms
                    res = res.split(" ")
                    
                    # [Time:, 211.642441, ms]
                    #parsing hours, minutes and seconds
                    s = float( res[1] )
                    
                    #converting the above time to seconds and storing it in resp array
                    resp.append(s)

                
                past = data_types[i]

            
            avg = 0
            summ = 0

            #looping to sum the elapsed times
            for i in range(count):
                print("Elapsed time for run %d = %fms" % (i+1, resp[i]))
                summ += resp[i]

            #using calculated sum to get average elapsed time in seconds
            avg = summ/float(n)

            print("\n"*3)
            print("="*50)

            print("Average time taken = %f ms" % avg)

            print("Done")
        except Exception as e:
            print(e)
            print("invalid arguments. make sure that -f is a valid file and -n is an integer")
    
    else:
        print("make sure you pass the correct parameters")
else:
    print("invalid number of arguments")


exit(0)

