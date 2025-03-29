from sys import argv
from enum import Enum

ws = " \r\n\t"

class types(Enum):
 eror=-1
 func=0
 stri=1
 numb=2
 flot=3
 tbev=4

def split(line:str) -> list[tuple[types,str]]:
 res: list[tuple[types,str]] = []
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
    if line[i]=="." and dot==0:
     sym+="."
     i+=1
     dot+=1
    elif line[i]=="." and dot>0: break
   res.append((types.numb,sym) if dot==0 else (types.flot,sym))
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
   res.append((types.func,sym))
  sym=""
  i+=1
 return res

var:dict[tuple[str,tuple[types,str]]]={"pi":(types.flot,"3.14159265")}
def execute(args:list[tuple[int,str]]) -> tuple[int,str]:
 global var
 command:tuple[int,str] = args.pop(0)
 if command[0] == types.stri or command[0] == types.numb or command[0] == types.flot:
  return command
 elif command[0] == types.tbev:
  return execute(split(command[1]))
 elif command[0] == types.func:
  if command[1]=="print":
   for i in args:
    if i[0] == types.func:
     print(execute([var[i[1]]])[1],end="")
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
    return var[args[0][1]]
    del var[args[0][1]]
   except KeyError:
    return (types.eror,"Function not defined")
  elif command[1]=="+":
   try:
    return (types.flot,str(float(execute(split(args[0][1]))[1]) + float(execute(split(args[1][1]))[1])))
   except:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="-":
   try:
    return (types.flot,str(float(execute(split(args[0][1]))[1]) - int(execute(split(args[1][1]))[1])))
   except:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="*":
   try:
    return (types.flot,str(float(execute(split(args[0][1]))[1]) * int(execute(split(args[1][1]))[1])))
   except:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  elif command[1]=="/":
   try:
    return (types.flot,str(float(execute(split(args[0][1]))[1]) / int(execute(split(args[1][1]))[1])))
   except:
    return (types.eror,"Cannot execute: '%s'" % command[1])
  else:
   return execute([var[command[1]]])
 return (types.numb,"0")

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
# print(var)
# print(t)
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
