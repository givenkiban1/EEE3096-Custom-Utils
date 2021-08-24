import os, sys

resp = []

if (len(sys.argv) == 5 ):
    if (sys.argv.count("-f")>0 and sys.argv.count("-n")>0):
        try:
            f = sys.argv[sys.argv.index("-f")+1]
            n = int(sys.argv[sys.argv.index("-n")+1])

            #print("f is %s" % f)
            #print("n is %s" % n)

            for i in range(n):
                res = os.system("python3 "+f)

                res = res[res.index("Elapsed time:") : ]

                res = res.split(":")
                h = int(res[1])
                m = int(res[2])
                s = double(res[3])

                resp.append(h*60*60 + m*60 + s)
            
            avg = 0
            summ = 0
            for i in range(n):
                print("Elapsed time for run %d = %ds" % (i+1, resp[i]))
                summ += resp[i]

            avg = summ/n

            print("Average time taken = %d" % avg)

            print("Done")
        except:
            print("invalid arguments. make sure that -f is a valid file and -n is an integer")
    
    else:
        print("make sure you pass the correct parameters")
else:
    print("invalid number of arguments")


exit(0)

