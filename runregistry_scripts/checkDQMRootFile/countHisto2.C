#include <iostream>
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <string>

using namespace std;

void countHisto2(string infname, int run)
{
   TFile *inf = new TFile(infname.data());
   TDirectory *f2 = (TDirectory*)inf->Get("DQMData");
   f2->cd();
   TDirectory *f3 = (TDirectory*)f2->Get(Form("Run %d",run));
   f3->cd();	
   TDirectory *f4 = (TDirectory*)f3->Get("Egamma");	
   f4->cd();
   TDirectory *f5 = (TDirectory*)f4->Get("Run summary");	
   f5->cd();
   TDirectory *f6 = (TDirectory*)f5->Get("Electrons");	
   f6->cd();
   TDirectory *f7 = (TDirectory*)f6->Get("Ele4_Et10TkIso1");	
   f7->cd();
 	

   TH1F *h = (TH1F*)f7->FindObjectAny("ele0_vertexPt_barrel");
   cout << "The number of entries = " << h->GetEntries() << endl;
}
