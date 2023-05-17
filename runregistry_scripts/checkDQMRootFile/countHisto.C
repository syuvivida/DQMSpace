#include <iostream>
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <string>

using namespace std;

void countHisto(string infname, int nLS=1500)
{
   TFile *inf = new TFile(infname.data());
   TH1F *h = (TH1F*)inf->FindObjectAny("lumisec");
   unsigned int nLSWithEvents=0;
   unsigned int lastLSwithEvents=0;
   for(int i=1; i<= nLS; i++)
     {
       int currentLS=h->GetBinLowEdge(i);
       int currentNeve=h->GetBinContent(i); 
       cout << currentLS <<" : "<< currentNeve <<endl;
       if( currentNeve>0){
	 nLSWithEvents++;
	 lastLSwithEvents= currentLS;
       }
     }
   cout << "Total number of LSs with non-zero events= " << nLSWithEvents << endl;
   cout << "The last LS with no-zero events = " << lastLSwithEvents << endl;
}
