import os, sys
import subprocess


#variable storing each elapsed time per run
resp = []

#for this program to run, user has to write the following
#python3 runfiles.py -f <filename.extension> -n <number of times to run filename.extension>
#this is why we always expect to have 5 parameters, counted after the python3 keyword
if (len(sys.argv) == 5 ):

    #next we check that both -f and -n arguments are passed
    if (sys.argv.count("-f")>0 and sys.argv.count("-n")>0):
        try:
            
            #here, we try parsing the arguments, hence using the try catch block
            f = sys.argv[sys.argv.index("-f")+1]
            n = int(sys.argv[sys.argv.index("-n")+1])

            #if the params above are valid, we now begin to loop n times, running the file at each iteration
            for i in range(n):
                res = "python3 "+f
                res = subprocess.getoutput(res)
                    
                #parsing the elapsed time data
                res = res[res.index("Elapsed time:") : ]
                
                res = res.split(":")
                #parsing hours, minutes and seconds
                h = int(res[1])
                m = int(res[2])
                s = float( res[3][: res[3].index("\n")] )
                
                #converting the above time to seconds and storing it in resp array
                resp.append(float(h*60*60 + m*60 + s))
            
            avg = 0
            summ = 0

            #looping to sum the elapsed times
            for i in range(n):
                print("Elapsed time for run %d = %fs" % (i+1, resp[i]))
                summ += resp[i]

            #using calculated sum to get average elapsed time in seconds
            avg = summ/float(n)


            
            print("\n"*3)
            print("="*50)

            print("Average time taken = %f" % avg)

            print("Done")
        except Exception as e:
            print(e)
            print("invalid arguments. make sure that -f is a valid file and -n is an integer")
    
    else:
        print("make sure you pass the correct parameters")
else:
    print("invalid number of arguments")


exit(0)

