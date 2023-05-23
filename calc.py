import math
possibleconfig = [0,0.5,-0.5]
from random import randint
from random import sample
import time

def is_close(a, b):
    return math.isclose(a, b, rel_tol=1e-09, abs_tol=0.0)

def calcPossibleConfig(m,vElectron, limit):
    nbConfiguration = (math.factorial(m*2))/(math.factorial(vElectron)*math.factorial(m*2-vElectron))
    print(nbConfiguration)
    totalMicroStates = [[]] * int(nbConfiguration)
    print(totalMicroStates)

    def mixAroundOrbitals(i):
        #empty_start_index = next((index for index, config in enumerate(totalMicroStates) if config == []), None)
        randomMicroState = randint(0,i)
        reOrderedMicroState = sample( totalMicroStates[randomMicroState], len(totalMicroStates[randomMicroState]) )
        return reOrderedMicroState

    i=0 
    previousi = 0
    iCounter = 0
    while i < nbConfiguration:
        def createMicroStates():
            specificMicroState = [[[],[]] for _ in range(m)]
            pluggedInElectrons = 0
            for j in range(0,m):
                k = 0
                
                while k < 2: # Only 2 avialable spots every orbital in microstate
                    inputInteger = randint(0,2)
                    inputElectron = possibleconfig[inputInteger]
                    if pluggedInElectrons == vElectron: # Check if the maximum amount of vElectrons in put in
                        specificMicroState[j][k] = 0
                        k+=1
                        continue
                    if k==1:
                        while specificMicroState[j][0] == inputElectron: # pauli exclusion
                            inputInteger = randint(0,2)
                            inputElectron = possibleconfig[inputInteger]
                        if inputElectron == specificMicroState[j][0]*-1:
                            pluggedInElectrons+=1
                            specificMicroState[j][0] = 0.5
                            specificMicroState[j][1] = -0.5
                            k+=1
                            continue
                        if specificMicroState[j][0] == 0 and inputElectron != 0:
                            pluggedInElectrons+=1
                            specificMicroState[j][0] = inputElectron
                            specificMicroState[j][1] = 0
                            k+=1
                            continue
                        else:
                            if inputElectron != 0:
                                pluggedInElectrons+=1
                            specificMicroState[j][1] = inputElectron

                    else:
                        if inputElectron != 0:
                            pluggedInElectrons+=1
                        specificMicroState[j][k] = inputElectron
                        k+=1
                        continue
            return specificMicroState, pluggedInElectrons
            
        datCreatedMicroState = createMicroStates()
        while datCreatedMicroState[1] != vElectron: # ensuring all electrons are in the orbitals
            datCreatedMicroState = createMicroStates()

        #timesLooped += 1
        result = any(all(all(is_close(a, b) for a, b in zip(subarray_2d, input_array_2d)) for subarray_2d, input_array_2d in zip(subarray, datCreatedMicroState[0])) for subarray in totalMicroStates if subarray) and datCreatedMicroState[0] in totalMicroStates
        if previousi == i:
            iCounter += 1
        else:
            iCounter = 0
        previousi = i # instead of the 1000 check if a i number is returned a consequntive amount of time
        #if timesLooped >= limit: # start mixing  up
        if iCounter >= limit: # start mixing  up 
            p = i
            while p < nbConfiguration:
                print(f"mixing state: {i}")
                returnedMicroStateMixed = mixAroundOrbitals(i)
                result = any(all(all(is_close(a, b) for a, b in zip(subarray_2d, input_array_2d)) for subarray_2d, input_array_2d in zip(subarray, returnedMicroStateMixed)) for subarray in totalMicroStates if subarray) and returnedMicroStateMixed in totalMicroStates
                while result:
                    returnedMicroStateMixed = mixAroundOrbitals(i)
                    result = any(all(all(is_close(a, b) for a, b in zip(subarray_2d, input_array_2d)) for subarray_2d, input_array_2d in zip(subarray, returnedMicroStateMixed)) for subarray in totalMicroStates if subarray) and returnedMicroStateMixed in totalMicroStates
                totalMicroStates[i] = returnedMicroStateMixed
                i += 1
                p +=1
                continue
            continue
        if result:
            continue

        else:
            if i < len(totalMicroStates):
                print(f"generating: {i}")
                totalMicroStates[i] = datCreatedMicroState[0]
            else:
                print(f"generating: {i}")
                totalMicroStates.append(datCreatedMicroState[0])  # Append specificMicroState if i is beyond the current length
            i += 1
            continue
    print(totalMicroStates)
    return totalMicroStates

def calculateMsMl(m,totalMicrostate):
    
    MicroStateConfigurationList = [[[],[]] for _ in range(len(totalMicrostate))]

    convertedMList = list(range(-(m//2), m//2 + 1))
    print(convertedMList)
    for i in range(0,len(totalMicrostate)):
        Ms = 0
        Ml = 0
        
        #jCounter = 0
        for jCounter, j in enumerate(totalMicrostate[i]):
            for k in j:
                
                Ms += k
                if k != 0:
                    Ml += convertedMList[jCounter] # there are multiple in convertedMList that have the same index j
            #jCounter +=1
        MicroStateConfigurationList[i][0] = Ms
        MicroStateConfigurationList[i][1] = float(Ml)
    return MicroStateConfigurationList

def TermTable(data):
    table = {}
    for microStateConfig in data:
        column = microStateConfig[1]
        value = microStateConfig[0]

        if column not in table:
            table[column] = []
        table[column].append(value)
    return table

if __name__ == "__main__":
    insertedM = 5
    start = time.time()
    totalMicroStateReturned = calcPossibleConfig(insertedM,5,5000) # do systematic amount of mixing go over every microstate do x times mixing for all configurations decrease the amount of random
    end = time.time()
    print(end-start)

    with open("output.txt", "w") as f:
        f.write("\n".join(str(item) for item in totalMicroStateReturned))

    calcMsMl = calculateMsMl(insertedM,totalMicroStateReturned)
    print(TermTable(calcMsMl))

    # can solve americum in 131.06236481666565 s (7,7,20000)