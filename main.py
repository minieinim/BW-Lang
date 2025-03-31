from sys import argv
from enum import Enum

ws = " \r\n\t"

class types(Enum):
 eror=-1
 func=0
 stri=1
 flot=2
 boln=3
 tbev=4

def split(line:str) -> list[tuple[types,any]]:
 res: list[tuple[types,any]] = []
 sym:str = ""
 i:int = 0
 paren:int = 0
 dot:int = 0
 while i<len(line):
  if line[i]=='"':
   i+=1
   while line[i]!='"' and i<len(line):
    if line[i]=="\\":
     i+=1
     if line[i]=="n":
      sym+="\n"
     elif line[i]=="r":
      sym+="\r"
     elif line[i]=='"':
      sym+='"'
     elif line[i]=="\\":
      sym+="\\"
    else:
     sym+=line[i]
    i+=1
   res.append((types.stri,sym))
  elif line[i].isdigit():
   while i<len(line) and line[i].isdigit():
    sym+=line[i]
    i+=1
    if i<len(line) and line[i]=="." and dot==0:
     sym+="."
     i+=1
     dot+=1
    elif i<len(line) and line[i]=="." and dot>0: break
   res.append((types.flot,float(sym)))
  elif line[i]=="#": break
  elif line[i]=="(":
   paren+=1
   i+=1
   while True:
    if line[i]=="(": paren+=1
    elif line[i]==")": paren-=1
    if paren==0 or i>=len(line): break
    sym+=line[i]
    i+=1
   res.append((types.tbev,sym))
  elif not line[i] in ws:
   while i<len(line) and not line[i] in ws:
    sym+=line[i]
    i+=1
   res.append((types.func,sym) if not sym in ["True","False"] else (types.boln,True if sym=="True" else False))
  sym=""
  i+=1
 return res

var:dict[tuple[str,tuple[types,any]]]={"pi":(types.flot,"3.14159265")}
def execute(args:list[tuple[types,any]]) -> tuple[types,any]:
 global var
 command:tuple[types,any] = args.pop(0)
 print(command)
 print(args)
 if command[0] in [types.stri,types.flot,types.boln]:
  return command
 elif command[0] == types.tbev:
  return execute(split(command[1]))
 elif command[0] == types.func:
  if command[1]=="print":
   for i in args:
    if i[0] == types.func:
     print(execute([var[i[1]]])[1],end="")
    elif i[0] == types.tbev:
     print(execute(split(i[1]))[1],end="")
    else:
     print(i[1],end="")
  elif command[1]=="let":
   if args[0][0] == types.func:
    try:
     var[args[0][1]]
     return (types.eror,"Function already defined")
    except KeyError:
     var[args[0][1]]=args[1]
   else:
    return (types.eror,"Cannot assign function")
  elif command[1]=="del":
   if args[0][0] != types.func:
    return (types.eror,"Cannot delete function")
   try:
    del var[args[0][1]]
   except KeyError:
    return (types.eror,"Function not defined")
  elif command[1]=="if":
   try:
    if execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1]:
     return execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))
    return execute([args[2]] if args[2][0]!=types.tbev else split(args[2][1]))
   except IndexError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="and":
   try:
    return (types.boln,bool(execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1] and execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))[1]))
   except ValueError or TypeError or IndexError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="or":
   try:
    return (types.boln,bool(execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1] or execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))[1]))
   except ValueError or TypeError or IndexError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="not":
   try:
    return (types.boln,not bool(execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1]))
   except ValueError or TypeError or IndexError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="+":
   try:
    return (types.flot,float(execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1] + execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))[1]))
   except IndexError or TypeError or ValueError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="-":
   try:
    return (types.flot,float(execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1] - execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))[1]))
   except IndexError or TypeError or ValueError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="*":
   try:
    return (types.flot,float(execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1] * execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))[1]))
   except IndexError or TypeError or ValueError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="/":
   try:
    return (types.flot,float(execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1] / execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))[1]))
   except IndexError or TypeError or ValueError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="<":
   try:
    return (types.boln,execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1] < execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))[1])
   except IndexError or TypeError or ValueError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="<=":
   try:
    return (types.boln,execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1] <= execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))[1])
   except IndexError or TypeError or ValueError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]==">":
   try:
    return (types.boln,execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1] > execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))[1])
   except IndexError or TypeError or ValueError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]==">=":
   try:
    return (types.boln,execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1] >= execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))[1])
   except IndexError or TypeError or ValueError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="=":
   try:
    return (types.boln,execute([args[0]] if args[0][0]!=types.tbev else split(args[0][1]))[1] == execute([args[1]] if args[1][0]!=types.tbev else split(args[1][1]))[1])
   except IndexError or TypeError or ValueError:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  else:
   try:
    if var[command[1]][0]==types.tbev:
     body=list(var[command[1]])
     if len(args)>0:
      for i in range(len(args)):
       if args[i][0] == types.flot:
        body[1]=body[1].replace(f"${i+1}",str(args[i][1]))
       elif args[i][0] == types.stri:
        body[1]=body[1].replace(f"${i+1}",'"'+args[i][1]+'"')
       elif args[i][0] == types.tbev:
        body[1]=body[1].replace(f"${i+1}",'('+args[i][1]+')')
     return execute([tuple(body)])
    else:
     return execute([var[command[1]]])
   except:
    return (types.eror,"Cannot execute: %s" % command[1])
 return (types.flot,0)

def main(file) -> int:
 if not file.endswith(".bw"):
  print("File should end with extension '.bw'")
  return 1
 fin: FileIO = open(file,"r")
 if not fin:
  print("File not found: '%s'" % file)
  return 1
 t:list[tuple[types,str]]
 r:tuple[types,str]
 for line in fin.readlines():
  t=split(line)
  r=execute(t)
  if r[0]==types.eror:
   print(r[1])
 fin.close()
 return 0

if __name__=="__main__":
 if len(argv)<2:
  print("Not enough arguments")
  exit(1)
 r=main(argv[1])
 exit(r)
