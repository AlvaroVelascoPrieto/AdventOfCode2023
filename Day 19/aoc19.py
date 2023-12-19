import time
def importInput():    
    workflows = {}
    parts = []
    rules = {}
    with open('input.txt') as input:
        for line in input:
            if line[0]=="{":
                line = line.strip('{').strip('\n').strip('}').split(',')
                part={}
                for elem in line:
                    elem = elem.split('=')
                    part[elem[0]]=elem[1]
                part['wf']='in'
                parts.append(part)
            elif line=='\n':
                continue
            else:
                a =line.strip('\n').split('{')  
                rulesPre = a[1].strip('}').split(',')
                rules={}
                for rule in rulesPre:
                    r = rule.split(':')
                    if len(r)==1:
                        rules['else']=r[0]
                    else:
                        rules[r[0]]=r[1]
                workflows[a[0]]=rules
                
    print(workflows)
    print(parts)
    return workflows, parts

wfs, parts = importInput()

for part in parts:
    currwf = part['wf']
    print('WFINI:'  + currwf)
    print("part: " + str(part))
    while currwf not in ('A', 'R'):
        print(currwf)
        rules = wfs[currwf]
        
        for rule in rules:
            caracteristica = rule[0]
            print(rule)
            if caracteristica == 'e':
                currwf = rules.get('else')
                
            else:
                valor = part[rule[0]] 
                operador = rule[1]
                
                print(operador)
                
                if operador == '<':
                    
                    if int(valor) < int(rule[2:]):
                        print('Entro2')
                        currwf = rules.get(rule)
                        print(currwf)
                        break
                elif operador == '>':
                    if int(valor) > int(rule[2:]):
                        currwf = rules.get(rule)
                        break
    part['wf']=currwf

print('END STATES: ')
sumAcum=0
for part in parts:
    sum=0
    print("part: " + str(part))
    if part['wf'] == 'A':
        for caracteristica in part:
            if caracteristica!='wf':
                sum += int(part[caracteristica])
    sumAcum+=sum
    print(sum)
print(sumAcum)
