
from os import listdir
from os.path import isfile, join

# PATH = "C:/Users/astroboi/Downloads/fa_AAA"
# PATH = "C:/Users/terry/Downloads/hg38.chromFa/chroms"
PATH = "C:/Users/terry/Downloads/hg38.chromFa/chr_short"
NCT_LEN = 3
BASE = ["A","C","G","T"]

def getPrefix(base):
    list = []
    for i in range(0,len(base)):
        list.append(base[i])
    return list

def getNucleotide(base,results,nct):
    if nct == 1:
        return results
    else:
        process = []
        for i in range(0,len(base)):
            st1 = base[i]
            for j in range(0,len(results)):
                st2 = results[j]
                process.append(st1+st2)
        return getNucleotide(base,process,nct-1)

def getFilesFromDir(dir_path):
    return [f for f in listdir(dir_path) if isfile(join(dir_path,f)) and f.find("_") == -1 and f.find("fa") > 0]


def match(j, k, dnaStr, base):
    # print("dnaStr : %s , base :%s" %(dnaStr, base))
    # print("dnaStr[%s] : %s , base[%s] :%s" %(j,dnaStr[j],k, base[k]))
    if dnaStr[j] == base[k]:
        if k == (len(base)-1):
            return True
        else:
            return match(j+1,k+1,dnaStr,base)
    return False

# def match2(dnaStr,base):
#     # TODO



def getData(files,ar,base,nct_len):

    results = {}

    for i in range(0,len(files)) :
        file = open(PATH+"/"+files[i],"r")
        header = ""
        dnaStr = ""

        iv = ""
        for i in range(0,nct_len-1):
            iv = iv +"X"
        dnaStr = dnaStr +iv
        try:
            flag = True
            while True:
                #line = file.read().splitlines()
                line = file.readline().rstrip('\n').rstrip('\r')
                if not line: break
                if flag:
                    header = header+line
                    flag= False
                else:
                    dnaStr = dnaStr[len(dnaStr)-nct_len+1:]
                    dnaStr = dnaStr + line.upper()
                    for j in range(0,len(ar)):
                        count = 0
                        for k in range(0,len(dnaStr)-len(ar[j])+1):
                            if(match(k,0,dnaStr,ar[j])):
                                count += 1

                        if ar[j] in results.keys():
                            results[ar[j]] += count
                        else:
                            results[ar[j]] = count
                        # print(ar[j] +"::::: %d" %(results[ar[j]]))


                #print(line)
        except FileNotFoundError as e:
            print(e)
        except IOError as e:
            print(e)
        finally:
            file.close()
    return results







def main():
    preFix = getPrefix(BASE)
    ar = getNucleotide(BASE,preFix,NCT_LEN)

    print(getData(getFilesFromDir(PATH), ar, BASE,NCT_LEN))

main()
#print(getFilesFromDir(PATH))



