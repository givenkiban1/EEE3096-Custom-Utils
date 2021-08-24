import os, sys
import subprocess



resp = []

if (len(sys.argv) == 5 ):
    if (sys.argv.count("-f")>0 and sys.argv.count("-n")>0):
        try:
            f = sys.argv[sys.argv.index("-f")+1]
            #print(f)
            n = int(sys.argv[sys.argv.index("-n")+1])
            #print(n)
            #print("f is %s" % f)
            #print("n is %s" % n)

            for i in range(n):
                res = "python3 "+f
                res = subprocess.getoutput(res)
                #print("result is ")
                #print(res)
                #if (type(res)==int):
                #print("output is an int")
                #continue
                    
                res = res[res.index("Elapsed time:") : ]
                #print("res :\n")
                #print(res)
                
                res = res.split(":")

                h = int(res[1])
                m = int(res[2])
                s = float( res[3][: res[3].index("\n")] )
                
                #print(h)
                #print(m)
                #print(s)

                resp.append(float(h*60*60 + m*60 + s))
            
            avg = 0
            summ = 0
            for i in range(n):
                print("Elapsed time for run %d = %fs" % (i+1, resp[i]))
                summ += resp[i]

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

