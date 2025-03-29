#include <cstdio>
#include <cstring>
#include <vector>
#include <string>
#include <utility>
#include <map>

using namespace std;

const string ws = " \r\n\t";

enum types {
 err=-1,
 func=0,
 str=1,
 num=2,
 tbe=3,
};

int isin(char a,string b) {
 for (int i=0;i<strlen(b.c_str());i++)
  if (b[i]==a) return 1;
 return 0;
}

vector<pair<int,string>> split(const char* line) {
 vector<pair<int,string>> res;
 int paren=0;
 string sym="";
 for (int i=0;i<strlen(line);i++) {
  if (line[i]=='"') {
   i++;
   while (line[i]!='"' && i<strlen(line)) {
    if (line[i]=='\\') {
     i++;
     switch (line[i]) {
      case 'n':
       sym+=0x0a;
       break;
      case 'r':
       sym+=0x0d;
       break;
      case '"':
       sym+='"';
       break;
      case '\\':
       sym+='\\';
       break;
      default:
       break;
     }
    } else {
     sym+=line[i];
    }
    i++;
   }
   res.push_back({str,sym});
  } else if (isdigit(line[i])) {
   while (isdigit(line[i])) {
    sym+=line[i];
    i++;
   }
   res.push_back({num,sym});
  } else if (line[i]=='#') {
   break;
  } else if (line[i]=='(') {
   paren++;
   i++;
   while (1) {
    if (line[i]=='(') paren++;
    else if (line[i]==')') paren--;
    if (paren==0 || i>strlen(line)) break;
    sym+=line[i];
    i++;
   }
   res.push_back({tbe,sym});
  } else if (!isin(line[i],ws)) {
   while (!isin(line[i],ws)) {
    sym+=line[i];
    i++;
   }
   res.push_back({func,sym});
  }
  sym="";
 }
 return res;
}

pair<int,string> execute(vector<pair<int,string>> t) {
 static map<string,pair<int,string>> var;
 string fname="";
 int i=0;
 if (get<int>(t[i])==str || get<int>(t[i])==num) {
  return t[i];
 } else if (get<int>(t[i])==tbe) {
  return execute(split(get<string>(t[i]).c_str()));
 } else if (get<int>(t[i])==func) {
  if (get<string>(t[i])=="print") {
   i++;
   while (i<t.size()) {
    if (get<int>(t[i])==str)
     printf("%s",get<string>(t[i]).c_str());
    else if (get<int>(t[i])==num)
     printf("%s",get<string>(t[i]).c_str());
    else if (get<int>(t[i])==func) {
     printf("%s",get<string>(execute(split(get<string>(var.at(get<string>(t[i]))).c_str()))).c_str());
    } else if (get<int>(t[i])==tbe)
     printf("%s",get<string>(execute(split(get<string>(t[i]).c_str()))).c_str());
    i++;
   }
  } else if (get<string>(t[i])=="let") {
   i++;
   if (get<int>(t[i])==func) {
    try {
     var.at(get<string>(t[i]));
    } catch (...) {
     fname=get<string>(t[i]);
     i++;
     var[fname]=t[i];
    }
   } else {
    return {err,"Cannot assign"};
   }
  } else if (get<string>(t[i])=="+") {
   try {
    return {num,to_string(stoi(get<string>(execute(split(get<string>(t[i+1]).c_str())))) + stoi(get<string>(execute(split(get<string>(t[i+2]).c_str())))))};
   } catch (...) {
    return {err,"Cannot evaluate expression: '+'"};
   }
  } else if (get<string>(t[i])=="-") {
   try {
    return {num,to_string(stoi(get<string>(execute(split(get<string>(t[i+1]).c_str())))) - stoi(get<string>(execute(split(get<string>(t[i+2]).c_str())))))};
   } catch (...) {
    return {err,"Cannot evaluate expression: '-'"};
   }
  } else if (get<string>(t[i])=="*") {
   try {
    return {num,to_string(stoi(get<string>(execute(split(get<string>(t[i+1]).c_str())))) * stoi(get<string>(execute(split(get<string>(t[i+2]).c_str())))))};
   } catch (...) {
    return {err,"Cannot evaluate expression: '*'"};
   }
  } else if (get<string>(t[i])=="/") {
   try {
    return {num,to_string(stoi(get<string>(execute(split(get<string>(t[i+1]).c_str())))) / stoi(get<string>(execute(split(get<string>(t[i+2]).c_str())))))};
   } catch (...) {
    return {err,"Cannot evaluate expression: '/'"};
   }
  } else {
   try {
    return execute(split(get<string>(var.at(get<string>(t[i]))).c_str()));
   } catch (...) {
    return {err,"Cannot evaluate function: '"+get<string>(t[i])+"'"};
   }
  }
 }
 return {num,"0"};
}

int main(int argc,char* argv[]) {
 if (argc==1) {
  printf("Not enough arguments\n");
  return 1;
 }
 FILE* fin=fopen(argv[1],"r");
 if (!fin) {
  printf("Cannot open file\n");
  return 1;
 }
 char line[128];
 while (fgets(line,128,fin)) {
  pair<int,string> t = execute(split(line));
  if (get<int>(t)==err) {
   printf("%s\n",get<string>(t).c_str());
   return 1;
  }
 }
 return 0;
}
