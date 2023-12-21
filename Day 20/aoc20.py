def importInput():    
    broadcast = {}
    modules = {}
    module = {}
    with open('input.txt') as input:
        for line in input:  
            module = {}       
            if line[0]=='%':
                module['type'] = '%'
                module['outputs'] = line.split('->')[1].strip('\n').strip().split(',')
                module['state'] = 'off'
                modules[line.split('->')[0].strip('%').strip()] = module
            elif line[0]=='&':
                module['type'] = '&'
                module['outputs'] = line.split('->')[1].strip('\n').strip().split(',')
                module['inputs']=[]
                modules[line.split('->')[0].strip('&').strip()] = module
            else:
                broadcast['outputs'] = line.split('->')[1].strip('\n').strip().split(',')
    return modules, broadcast

modules, broadcast = importInput()

lowPulses = 0
highPulses = 0
signals = []
for module in modules:
    for output in modules[module]['outputs']:
        if output=='rx':
            continue
        if modules[output.strip()]['type']=='&':
            
            input = {'name' : module, 'lastPulse' : 'low'}
            modules[output.strip()]['inputs'].append(input)



for i in range(1000):
    lowPulses+=1
    for output in broadcast['outputs']:
        signal = {'origin': 'broadcast', 'dest' : output, 'pulseType': 'low'}
        signals.append(signal)
    while len(signals)!=0:
        signal = signals.pop(0)
        module = modules[signal['dest'].strip()]
        type = module['type']
        pulse = signal['pulseType']
        if type =='%':
            if pulse == 'low':
                lowPulses+=1
                if module['state'] == 'off':
                    module['state'] = 'on'
                else:
                    module['state'] = 'off'
                for output in module['outputs']:
                    newSignal = {'origin': signal['dest'],'dest' : output, 'pulseType': 'high' if module['state']=='on' else 'low'}
                    signals.append(newSignal)
            else:
                highPulses+=1
                #NADA
        else:
            if pulse == 'low':
                lowPulses+=1
                inputs = module['inputs']
                for input in inputs:
                    if input['name']==signal['origin']:
                        input['lastPulse'] = "low"
                for output in module['outputs']:
                        if output=='rx':
                            highPulses+=1
                            continue    
                        newSignal = {'origin': signal['dest'],'dest' : output, 'pulseType' : 'high'}
                        signals.append(newSignal)
            else:
                highPulses+=1
                inputs = module['inputs']
                for input in inputs:
                    if input['name']==signal['origin'].strip():
                        input['lastPulse'] = "high"
                allHigh = True
                for input in inputs:
                    if input['lastPulse']=="low":
                        allHigh=False
                        break
                
                if allHigh:
                    for output in module['outputs']:
                        if output=='rx':
                            lowPulses+=1
                            continue    
                        newSignal = {'origin': signal['dest'],'dest' : output, 'pulseType' : 'low'}
                        signals.append(newSignal)
                else:
                    
                    for output in module['outputs']:
                        if output=='rx':
                            highPulses+=1
                            continue    
                        newSignal = {'origin': signal['dest'],'dest' : output, 'pulseType' : 'high'}
                        signals.append(newSignal)

print("LOW PULSES: " + str(lowPulses))
print("HIGH PULSES: " + str(highPulses))
print(lowPulses*highPulses)