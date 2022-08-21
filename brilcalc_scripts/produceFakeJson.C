#include <fstream>
#include <iostream>
using namespace std;

void produceFakeJson(std::string outputFileName)
{
  ofstream fout;
 fout.open(outputFileName.data());
 fout << "{" << endl;
 int run=1;
 int lumi1=1;
 int lumi2=1;
 cout << "Input run number" << endl; 
 cout << "If you don't want to continue, input -1" << endl;
 cin >> run;
 while(run >0)
   {
     fout << " \"" << run << "\": [";
     cout << "Start enter lumi sections" << endl;
     cout << "For example, 4 4 or 4 39 " << endl;
     cout << "If you don't want to continue, input -1 -1" << endl;
     cin >> lumi1 >> lumi2;
     while(lumi1 >0 && lumi2>0)
     {
      fout << "[" << lumi1 << ", " << lumi2 << "]"; 
      cin >> lumi1 >> lumi2;
      if(lumi1>0 && lumi2>0)
	fout << ", ";
      }
     cout << "Input run number" << endl;
     cin >> run;
     if(run>0)
       fout << "]," << endl;
     else
       {
	 fout << "]" << endl;
	 fout << "}" << endl;
       }
   }
fout.close();
}
