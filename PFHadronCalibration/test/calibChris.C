#include <vector>
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TF1.h>
#include <TF2.h>
#include "TH2F.h"
#include "TLegend.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "Math/SMatrix.h"
#include "Math/SVector.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TLine.h"
#include <string>
#include <iostream>
#include <math.h>

//#include "CrystalBall.C"

using namespace std;

double sigC_ = 5.;

//unsigned sampleRangeHigh = 1000;
unsigned sampleRangeHigh = 500;
bool freezeparameters = true;
bool useMean = false;
bool changeRange =false;
bool old_logic = false;
bool drawpT = false;
bool drawResoFit = true;
bool saveCanvas = true;
//char* _region_ = (char*)"EC_within_tracker";
//char* _region_ = (char*)"EC_outside_tracker";
//char* _region_ = (char*)"barrel";
char* _region_ = (char*)"Full";

float _etaMin_ = 0.0;
float _etaMax_ = 0.0;


//threshold
/////////////MM
double aEH = 3.5;
double aE = 3.5;
// double aEH = 4.5;
// double aE = 4.5;
double aH = 2.5;//3.0;

double aEHe = 3.5;
double aEe = 3.5;
// double aEHe = 4.5;
// double aEe = 4.5;
double aHe = 2.5;
/////////////MM


/*
//threshold
/////////////SP
double aEH = 3.675;
double aE = 3.675;
double aH = 2.625;//3.0;

double aEHe = 3.675;
double aEe = 3.675;
double aHe = 2.625;
/////////////SP
*/


//double lBs = 0.25; //0.25 B //0.5 E
double lBs = 0.50; //0.25 B //0.5 E
//double mBs=1.; //1 B
double mBs=2.; //1 B
double hBs=5.0; //10 40 B 50 E

double RBE = 2; //rebinning for alpha-beta curves

//Eta factor : ecal*factor + hcal
double factorB = 1.3;//Optimal //A factor put in by hand to make the eta dependence agree
double factorE = 1.3; //better. Should fit for the value later. 
//double factorE = 1.7; //better. Should fit for the value later.  //shubham

vector<double> sigmas;

void LoadOldThresholds() {
	aEH = 3.5; aE = 3.5; aH = 2.5; //3.5 2.5
	aEHe = 3.5; aEe = 3.5; aHe = 2.5;
}

//spandey
void LoadNewThresholds() {
	aEH = 3.8; aE = 3.8; aH = 3.0; //3.5 2.5
	aEHe = 3.8; aEe = 3.8; aHe = 3.0;
}


TF1* faBarrel;
TF1* fbBarrel;
TF1* fcBarrel;
TF1* faEtaBarrel;
TF1* fbEtaBarrel;


TF1* faBarrel52x;
TF1* fbBarrel52x;
TF1* fcBarrel52x;
TF1* faEtaBarrel52x;
TF1* fbEtaBarrel52x;

// Double_t median1(TH1 *h1) {
//    //compute the median for 1-d histogram h1
//    Int_t nbins = h1->GetXaxis()->GetNbins();
//    Double_t *x = new Double_t[nbins];
//    Double_t *y = new Double_t[nbins];
//    for (Int_t i=0;i<nbins;i++) {
//       x[i] = h1->GetXaxis()->GetBinCenter(i+1);
//       y[i] = h1->GetBinContent(i+1);
//    }
//    Double_t median = TMath::Median(nbins,x,y);
//    delete [] x;
//    delete [] y;
//    return median;
// } 

void InitBarrelAlpha() {

	// faBarrel = new TF1("faBarrel","[0]+((([1]+([2]/(x^[8])))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]*(x/[5])))))",1.,1000.);
	// fbBarrel = new TF1("fbBarrel","[0]+([1]+[2]/x^1.1)*exp(-x/[3])-[4]*exp(-x^[5]*x/2000.)",1.,1000.);
	// fcBarrel = new TF1("fcBarrel","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])",1.,1000.);
	// faEtaBarrel = new TF1("faEtaBarrel","[0]+[1]*exp(-x^[3]/[2])+([4]/x^[5])*exp([6]*x)",1.,1000.);
	// fbEtaBarrel = new TF1("fbEtaBarrel","[0]+([1]*x+[2])*exp(-(x+[4])/[3])",1.,1000.);
	// faBarrel->SetParameter(0,1.04193);
	// fbBarrel->SetParameter(0,0.992287);
	// fcBarrel->SetParameter(0,0.978144);
	// faEtaBarrel->SetParameter(0,-0.00327152);
	// fbEtaBarrel->SetParameter(0,-6.58476);
	// faBarrel->SetParameter(1,16.2881);
	// fbBarrel->SetParameter(1,0.216829);
	// fcBarrel->SetParameter(1,0.0451738);
	// faEtaBarrel->SetParameter(1,-0.00327152);
	// fbEtaBarrel->SetParameter(1,0.0273361);
	// faBarrel->SetParameter(2,-14.9307);
	// fbBarrel->SetParameter(2,-5.0668);
	// fcBarrel->SetParameter(2,-0.49014);
	// fbEtaBarrel->SetParameter(2,12.4812);
	// faBarrel->SetParameter(3,0.80573);
	// fbBarrel->SetParameter(3,42.8035);
	// fcBarrel->SetParameter(3,8.84333);
	// fbEtaBarrel->SetParameter(3,505.069);
	// faBarrel->SetParameter(4,3.06364);
	// fbBarrel->SetParameter(4,0.0832237);
	// fcBarrel->SetParameter(4,1.18357);
	// faEtaBarrel->SetParameter(4,-0.00327152);
	// fbEtaBarrel->SetParameter(4,318.064);
	// faBarrel->SetParameter(5,9.23088);
	// fbBarrel->SetParameter(5,0.921352);
	// fcBarrel->SetParameter(5,12.6626);
	// faBarrel->SetParameter(6,0.174875);
	// faBarrel->SetParameter(7,0.522519);
	// faBarrel->SetParameter(8,0.0568171);

	// Barrel (fit made with |eta| < 1.2)
	faBarrel = new TF1("faBarrel","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])",1.,1000.);
	fbBarrel = new TF1("fbBarrel","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])",1.,1000.);
	fcBarrel = new TF1("fcBarrel","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])",1.,1000.);
	faEtaBarrel = new TF1("faEtaBarrel","[0]+[1]*exp(-x/[2])",1.,1000.);
	fbEtaBarrel = new TF1("fbEtaBarrel","[0]+[1]*exp(-x/[2])+[3]*[3]*exp(-x*x/([4]*[4]))",1.,1000.);
	faBarrel->SetParameter(0,1.15665);
	fbBarrel->SetParameter(0,0.994603);
	fcBarrel->SetParameter(0,0.956544);
	faEtaBarrel->SetParameter(0,0.014664);
	fbEtaBarrel->SetParameter(0,0.00975451);
	faBarrel->SetParameter(1,0.165627);
	fbBarrel->SetParameter(1,0.13632);
	fcBarrel->SetParameter(1,0.0857207);
	faEtaBarrel->SetParameter(1,-0.0426776);
	fbEtaBarrel->SetParameter(1,0.102247);
	faBarrel->SetParameter(2,0.827718);
	fbBarrel->SetParameter(2,-0.758013);
	fcBarrel->SetParameter(2,-0.44347);
	faEtaBarrel->SetParameter(2,431.054);
	fbEtaBarrel->SetParameter(2,436.21);
	faBarrel->SetParameter(3,231.339);
	fbBarrel->SetParameter(3,183.627);
	fcBarrel->SetParameter(3,63.3479);
	faBarrel->SetParameter(4,2.45332);
	fbBarrel->SetParameter(4,1);
	fcBarrel->SetParameter(4,1.24174);
	faBarrel->SetParameter(5,29.6603);
	fbBarrel->SetParameter(5,39.6784);
	fcBarrel->SetParameter(5,12.322);





	faBarrel->SetLineColor(kBlue+1);
	faBarrel->SetLineStyle(2);
	faBarrel->SetLineWidth(2);
	fbBarrel->SetLineColor(kBlue+1);
	fbBarrel->SetLineStyle(2);
	fbBarrel->SetLineWidth(2);
	fcBarrel->SetLineColor(kBlue+1);
	fcBarrel->SetLineStyle(2);
	fcBarrel->SetLineWidth(2);
	faEtaBarrel->SetLineColor(kBlue+1);
	faEtaBarrel->SetLineStyle(2);
	faEtaBarrel->SetLineWidth(2);
	fbEtaBarrel->SetLineColor(kBlue+1);
	fbEtaBarrel->SetLineStyle(2);
	fbEtaBarrel->SetLineWidth(2);

	faBarrel->SetTitle("Ecal coef 4XY");
	fbBarrel->SetTitle("Hcal coef 4XY");
	faEtaBarrel->SetTitle("#alpha coef 4XY");
	fbEtaBarrel->SetTitle("#beta coef 4XY");



	// faBarrel52x = new TF1("faBarrel52X","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])",1.,1000.);
	//  fbBarrel52x = new TF1("fbBarrel52X","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])",1.,1000.);
	//  fcBarrel52x = new TF1("fcBarrel52X","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])",1.,1000.);
	//  faEtaBarrel52x = new TF1("faEtaBarrel52X","[0]+[1]*exp(-x/[2])",1.,1000.);
	//  fbEtaBarrel52x = new TF1("fbEtaBarrel52X","[0]+[1]*exp(-x/[2])",1.,1000.);
	//  faBarrel52x->SetParameter(0,1.30727);
	//  fbBarrel52x->SetParameter(0,0.998609);
	//  fcBarrel52x->SetParameter(0,0.961909);
	//  faEtaBarrel52x->SetParameter(0,256.375);
	//  fbEtaBarrel52x->SetParameter(0,0.0236908);
	//  faBarrel52x->SetParameter(1,0.297017);
	//  fbBarrel52x->SetParameter(1,0.185606);
	//  fcBarrel52x->SetParameter(1,2.48019);
	//  faEtaBarrel52x->SetParameter(1,-256.412);
	//  fbEtaBarrel52x->SetParameter(1,0.144532);
	//  faBarrel52x->SetParameter(2,0.176997);
	//  fbBarrel52x->SetParameter(2,-2.4317);
	//  fcBarrel52x->SetParameter(2,-6.18656);
	//  faEtaBarrel52x->SetParameter(2,1.02648e+06);
	//  fbEtaBarrel52x->SetParameter(2,122.074);
	//  faBarrel52x->SetParameter(3,71.526);
	//  fbBarrel52x->SetParameter(3,11.5238);
	//  fcBarrel52x->SetParameter(3,7.32584);
	//  faBarrel52x->SetParameter(4,2.16376);
	//  fbBarrel52x->SetParameter(4,1);
	//  fcBarrel52x->SetParameter(4,0.263953);
	//  faBarrel52x->SetParameter(5,31.9415);
	//  fbBarrel52x->SetParameter(5,9.98657);
	//  fcBarrel52x->SetParameter(5,387.311);

	faBarrel52x = new TF1("faBarrel52x","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])",1.,1000.);
	fbBarrel52x = new TF1("fbBarrel52x","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])",1.,1000.);
	fcBarrel52x = new TF1("fcBarrel52x","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])",1.,1000.);
	faEtaBarrel52x = new TF1("faEtaBarrel52x","[0]+[1]*exp(-x/[2])",1.,1000.);
	fbEtaBarrel52x = new TF1("fbEtaBarrel52x","[0]+[1]*exp(-x/[2])",1.,1000.);
	faBarrel52x->SetParameter(0,1.36776);
	fbBarrel52x->SetParameter(0,1.00174);
	fcBarrel52x->SetParameter(0,0.958822);
	faEtaBarrel52x->SetParameter(0,-0.0235949);
	fbEtaBarrel52x->SetParameter(0,-20.0611);
	faBarrel52x->SetParameter(1,0.401817);
	fbBarrel52x->SetParameter(1,-0.575566);
	fcBarrel52x->SetParameter(1,-20.7743);
	faEtaBarrel52x->SetParameter(1,0.145271);
	fbEtaBarrel52x->SetParameter(1,20.1811);
	faBarrel52x->SetParameter(2,-0.272423);
	fbBarrel52x->SetParameter(2,0.511645);
	fcBarrel52x->SetParameter(2,22.8622);
	faEtaBarrel52x->SetParameter(2,3.76578);
	fbEtaBarrel52x->SetParameter(2,733806);
	faBarrel52x->SetParameter(3,39.0306);
	fbBarrel52x->SetParameter(3,11.098);
	fcBarrel52x->SetParameter(3,1.29814);
	faBarrel52x->SetParameter(4,2.30666);
	fbBarrel52x->SetParameter(4,1);
	fcBarrel52x->SetParameter(4,0.223834);
	faBarrel52x->SetParameter(5,27.6117);
	fbBarrel52x->SetParameter(5,34.2481);
	fcBarrel52x->SetParameter(5,84.6003);


	faBarrel52x->SetLineColor(kOrange-3);
	faBarrel52x->SetLineStyle(7);
	faBarrel52x->SetLineWidth(2);
	fbBarrel52x->SetLineColor(kOrange-3);
	fbBarrel52x->SetLineStyle(7);
	fbBarrel52x->SetLineWidth(2);
	fcBarrel52x->SetLineColor(kOrange-3);
	fcBarrel52x->SetLineStyle(7);
	fcBarrel52x->SetLineWidth(2);
	faEtaBarrel52x->SetLineColor(kOrange-3);
	faEtaBarrel52x->SetLineStyle(7);
	faEtaBarrel52x->SetLineWidth(2);
	fbEtaBarrel52x->SetLineColor(kOrange-3);
	fbEtaBarrel52x->SetLineStyle(7);
	fbEtaBarrel52x->SetLineWidth(2);

	faBarrel52x->SetTitle("Ecal coef 52X");
	fbBarrel52x->SetTitle("Hcal coef 52X");
	faEtaBarrel52x->SetTitle("#alpha coef 52X");
	fbEtaBarrel52x->SetTitle("#beta coef 52X");




}


///////////////////////////////////////////////////////////////////////////////
//Container class that holds all the coefficients for a particular Etrue bin
///////////////////////////////////////////////////////////////////////////////

class ABC
{
	private:

		vector<double> ETrueEnergies_; //Variables that fall in this ETrue bin, 
		vector<double> ecalEnergies_;  //which is defined by binLowEdge and 
		vector<double> hcalEnergies_;  //binHighEdge. sigmaEcalHcal is simply the
		vector<double> etas_;          //uncertainty from the ecal and hcal(not
		vector<double> sigmaEcalHcal_; //uncertainty in the calibration consts)
		double binLowEdge_;
		double binHighEdge_;
		double etaMinFit_;     //From what etas to fit the B and C constants.
		double etaMaxFit_;     
		double etaMinEtaFit_;  //From what etas to fit the Alpha and Beta 
		double etaMaxEtaFit_;  //constants.
		bool isBarrel_;


		double ETrueAverage_; //Average and RMS of the ETrue values in the bin.
		double ETrueRMS_;
		double a_;  //Constant values.
		double b_;
		double c_;

		double sigmaB_;  //Uncertainty in the constants
		double sigmaC_;

	public:
		ABC(double binLowEdge, double binHighEdge, bool isBarrel); 

		bool addEntry(double ETrueEnergy, double ecalEnergy, double hcalEnergy,
				double eta);  //Adds an event to the ETrue bin
		double getBinLowEdge();
		double getBinHighEdge();
		bool isBarrel();  //Checks if it is a barrel-type constant storage
		bool isEmpty();   //Checks if its empty
		bool isEmptyInFitRange();   //Checks if its empty in eta fit range
		unsigned getSize();        //Returns the various stored variables in the
		double getETrueAverage();  //ABC object
		double getETrueRMS();
		double getA();
		double getB();
		double getC();
		double getSigmaB();
		double getSigmaC();

		double getETrue(unsigned i);
		double getEcal(unsigned i); //Returns b*ecal for entry i
		double getHcal(unsigned i); //Returns c*hcal for entry i
		double getEta(unsigned i);
		double getNEntries();

		void computeETrueAverage();  //Computes the various calibration constants
		void computeETrueRMS();      //and other stored elements in the object.
		void computeA(double a);     //Right now the constant "a" is not computed
		void computeB();             //but rather just set.
		void computeC();
		bool computeBC();
		void clear();
};

ABC::ABC(double binLowEdge, double binHighEdge, 
		bool _isBarrel) 

{
	binLowEdge_ = binLowEdge;
	binHighEdge_ = binHighEdge;
	isBarrel_ = _isBarrel;

	if(isBarrel_)
	{
		etaMinFit_ = 0.0;
		etaMaxFit_ = 1.0;
		etaMinEtaFit_ = 0.0;
		etaMaxEtaFit_ = 1.3;
	}
	else
	{
		etaMinFit_ = 1.6;
		etaMaxFit_ = 2.2; //FIXME 2.2
		etaMinEtaFit_ = 1.6;
		etaMaxEtaFit_ = 2.8; //FIXME 2.8
	}

	a_ = 0;
	b_ = 0;
	c_ = 0;
	ETrueAverage_ = 0;
	ETrueRMS_ = 0;
	sigmaB_ = 0;
	sigmaC_ = 0;
}
bool ABC::addEntry(double ETrue, double ecalEnergy, double hcalEnergy, double eta)
{


	double sigmaEcalHcal;

	if(isBarrel_) 
		sigmaEcalHcal = sqrt(0.08*0.08 + 1.04*1.04*(std::max(ecalEnergy + 
						hcalEnergy, 1.0)));
	else
		sigmaEcalHcal = sqrt(0.04*0.04 + 1.80*1.80*(std::max(ecalEnergy + 
						hcalEnergy, 1.0)));

	if( fabs(ecalEnergy + hcalEnergy + a_ - ETrue) > sigC_*sigmaEcalHcal || 
			(ecalEnergy + hcalEnergy) < 0.5 || ETrue < 1.0 || ETrue < binLowEdge_ || 
			ETrue> binHighEdge_ || fabs(eta) > etaMaxFit_ || fabs(eta) < etaMinFit_ )
		return false;


	ETrueEnergies_.push_back(ETrue);
	ecalEnergies_.push_back(ecalEnergy);
	hcalEnergies_.push_back(hcalEnergy);
	etas_.push_back(eta);
	sigmaEcalHcal_.push_back(sigmaEcalHcal);

	// if(ecalEnergy==0 && isBarrel_)
	//   cout<<hcalEnergy<<"  "<<fabs(ecalEnergy + hcalEnergy + a_ - ETrue)<<"   "<<sigmaEcalHcal<<endl;

	return true;
}

double ABC::getBinLowEdge() {return binLowEdge_;}
double ABC::getBinHighEdge() {return binHighEdge_;}
double ABC::getETrueAverage() {return ETrueAverage_;}
double ABC::getETrueRMS() {return ETrueRMS_;}
double ABC::getA() {return a_;}
double ABC::getB() {return b_;}
double ABC::getC() {return c_;}
double ABC::getSigmaB() {return sigmaB_;}
double ABC::getSigmaC() {return sigmaC_;}

double ABC::getETrue(unsigned i) {return ETrueEnergies_[i];}
double ABC::getEcal(unsigned i) {return ecalEnergies_[i];}
double ABC::getHcal(unsigned i) {return hcalEnergies_[i];}
double ABC::getEta(unsigned i) {return etas_[i];}
double ABC::getNEntries(){return ETrueEnergies_.size();}
bool ABC::isBarrel() {return isBarrel_;}
bool ABC::isEmpty() 
{
	if(ETrueEnergies_.size() == 0) return true;
	else return false;
}
bool ABC::isEmptyInFitRange() 
{
	//  cout<<"etas_.size():"<<etas_.size()<<endl;
	for(unsigned i = 0; i < etas_.size(); i++)
	{
		if(fabs(etas_[i]) < etaMaxFit_ && fabs(etas_[i]) > etaMinFit_)
			return false;
	}
	return true;
}
unsigned ABC::getSize()
{
	return ETrueEnergies_.size();
}
void ABC::computeETrueAverage()
{
	double totalETrue = 0;
	int numberSkipped = 0;

	for(unsigned i = 0; i < ETrueEnergies_.size(); i++)
	{
		if(fabs(etas_[i]) > etaMaxFit_ || fabs(etas_[i]) < etaMinFit_ ) 
		{
			numberSkipped++;
			continue;
		}   

		totalETrue += ETrueEnergies_[i];
	}

	ETrueAverage_ = totalETrue/(ETrueEnergies_.size() - numberSkipped);
} 
void ABC::computeETrueRMS()
{
	double totalETrueSquared = 0;
	int numberSkipped = 0;

	for(unsigned i = 0; i<ETrueEnergies_.size(); i++)
	{
		if(fabs(etas_[i]) > etaMaxFit_ || fabs(etas_[i]) < etaMinFit_ ) 
		{
			numberSkipped++;
			continue;
		}

		totalETrueSquared += ETrueEnergies_[i]*ETrueEnergies_[i];
	}

	ETrueRMS_ = sqrt(
			(totalETrueSquared/(ETrueEnergies_.size() - numberSkipped) -
			 ETrueAverage_*ETrueAverage_)/(ETrueEnergies_.size() - numberSkipped)); 
} 
void ABC::computeA(double a) 
{
	a_ = a; 
}
void ABC::computeB() 
{
	double totalEcalSquared = 0;
	double totalEMinusATimesEcal = 0;

	for (unsigned i = 0; i < ETrueEnergies_.size(); i++)
	{
		if(fabs(etas_[i]) > etaMaxFit_ || fabs(etas_[i]) < etaMinFit_ ) continue;

		totalEcalSquared += 2* ecalEnergies_[i]*ecalEnergies_[i]/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);
		totalEMinusATimesEcal += 2*(ETrueEnergies_[i] - a_)*ecalEnergies_[i]/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);
	}

	b_ = totalEMinusATimesEcal/totalEcalSquared;
	sigmaB_ = sqrt(1/totalEcalSquared);
}
void ABC::computeC() 
{
	double totalHcalSquared = 0;
	double totalEMinusATimesHcal = 0;

	//cout<<" size C : "<<ETrueEnergies_.size()<<endl;

	for (unsigned i = 0; i < ETrueEnergies_.size(); i++)
	{
		totalHcalSquared += 2*hcalEnergies_[i]*hcalEnergies_[i]/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);
		totalEMinusATimesHcal += 2*(ETrueEnergies_[i] - a_)*hcalEnergies_[i]/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);
	}

	c_ = totalEMinusATimesHcal/totalHcalSquared;
	//cout<<totalEMinusATimesHcal<<"   "<<totalHcalSquared<<"   "<<c_<<endl;
	//cout<<"totalEMinusATimesHcal: "<<totalEMinusATimesHcal<<",   totalHcalSquared: "<<totalHcalSquared<<",   c_: "<<c_<<endl;

	// //FIXME MM
	// TH1F* cplot=new TH1F("cplot","",3000,-1, 5); 
	// float median=c_;
	// for (unsigned i = 0; i < ETrueEnergies_.size(); i++)
	//   {
	//     cplot->Fill( (ETrueEnergies_[i] - a_)/hcalEnergies_[i] );
	//   }

	// //  cout<<ETrueEnergies_[0]<<"  "<<" c_ "<<c_<<"   "<<(c_ + median1(cplot))/2.<<"   "<<median1(cplot)<<endl;
	// // if(ETrueEnergies_[0]>20)
	// //   c_ = (c_ + median1(cplot))/2.;
	// if(ETrueEnergies_[0]<=20)
	//   c_ = median1(cplot);

	// delete cplot;

	//================================


	sigmaC_ = sqrt(1/totalHcalSquared);
}
bool ABC::computeBC()
{
	ROOT::Math::SMatrix<double,2, 2, ROOT::Math::MatRepStd<double,2> > coeffs;
	ROOT::Math::SVector<double, 2> consts;
	ROOT::Math::SVector<double, 2> values;
	bool isInverted;

	coeffs(0, 0) = 0;
	coeffs(0, 1) = 0;
	coeffs(1, 0) = 0;
	coeffs(1, 1) = 0;
	consts(0) = 0;
	consts(1) = 0;
	//Create the matrix that will be inverted and the vector which will multiply
	//that matrix to find the b and c calibration constants.

	//cout<<" size AB : "<<ETrueEnergies_.size()<<endl;

	for(unsigned i = 0; i < ETrueEnergies_.size(); ++i)
	{
		if(fabs(etas_[i]) > etaMaxFit_ || fabs(etas_[i]) < etaMinFit_ ) continue;

		// if(i<10)
		// 	cout<<ETrueEnergies_[i]<<"   "<<ecalEnergies_[i]<<"   "<<hcalEnergies_[i]<<"   "<<etas_[i]<<"  "<<sigmaEcalHcal_[i]<<"   "<<a_;


		coeffs(0, 0) += 2*ecalEnergies_[i]*ecalEnergies_[i]/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		coeffs(0, 1) += 2*ecalEnergies_[i]*hcalEnergies_[i]/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		coeffs(1, 0) += 2*ecalEnergies_[i]*hcalEnergies_[i]/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		coeffs(1, 1) += 2*hcalEnergies_[i]*hcalEnergies_[i]/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		consts(0) += 2*(ETrueEnergies_[i] - a_)*ecalEnergies_[i] /
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		consts(1) += 2*(ETrueEnergies_[i] - a_)*hcalEnergies_[i]/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		// if(i<10)
		// 	cout<<" ---> "<<coeffs(0, 0)<<"  "<<coeffs(0, 0)
		// 	    <<"  "<<coeffs(0, 0)<<"  "<<coeffs(0, 0)
		// 	    <<"  "<<consts(0)<<"  "<<consts(1)<<endl;

	}
	isInverted = coeffs.Invert();
	// coeffs.Print(cout); cout<<endl;
	// consts.Print(cout);


	if(isInverted && sqrt(coeffs(0,0)) <  100000) //Make sure it inverted successfully (i.e. det != 0)
	{

		values = coeffs*consts;

		b_ = values(0);
		c_ = values(1);
		sigmaB_ = sqrt(coeffs(0,0));
		sigmaC_ = sqrt(coeffs(1,1));

		//cout<<" b: "<<b_<<"  c: "<<c_<<endl;

		// //FIXME MM
		// TH1F* cplot=new TH1F("cplot","",3000,-1, 5); 
		//   for(unsigned i = 0; i < ETrueEnergies_.size(); ++i)
		// 	  {
		// 	    if(fabs(etas_[i]) > etaMaxFit_ || fabs(etas_[i]) < etaMinFit_ ) continue;

		// 	    cplot->Fill( (ETrueEnergies_[i] - a_ - b_*ecalEnergies_[i])/hcalEnergies_[i] ); 
		// 	  }

		// 	//	cout<<ETrueEnergies_[0]<<"  "<<" c_ "<<c_<<"   "<<(c_ + median1(cplot))/2.<<"   "<<median1(cplot)<<endl;

		// 	c_ = (c_ + median1(cplot))/2.;
		// 	//	c_ = median1(cplot);

		// 	delete cplot;
		//================================

		return true;


	}
	else return false;
}

void ABC::clear()
{
	ETrueEnergies_.clear();
	ecalEnergies_.clear();
	hcalEnergies_.clear();
	etas_.clear();

	delete &binLowEdge_;
	delete &binHighEdge_;
	delete &isBarrel_;
	delete &ETrueAverage_;
	delete &ETrueRMS_;
	delete &a_;
	delete &b_;
	delete &c_;
	delete &sigmaB_;
	delete &sigmaC_;
}

class AlphaBeta
{
	private:
		vector<double> ETrueEnergies_;
		vector<double> ecalEnergies_;
		vector<double> hcalEnergies_;
		vector<double> etas_;
		vector<double> sigmaEcalHcal_;
		vector<double> a_;


		double binLowEdge_;
		double binHighEdge_;
		double etaMinFit_;
		double etaMaxFit_;
		bool isBarrel_;

		double ETrueAverage_;
		double ETrueRMS_;
		double alpha_;
		double gamma_;
		double beta_;
		double sigmaAlpha_;
		double sigmaGamma_;
		double sigmaBeta_;

	public:
		AlphaBeta(double binLowEdge, double binHighEdge, bool isBarrel);
		bool addEntry(double ETrueEnergy, double ecalEnergies, double correctedHcal, double eta);  //Adds an event to the ETrue bin
		double getBinLowEdge();
		double getBinHighEdge();
		bool isBarrel();  //Checks if it is a barrel-type constant storage
		bool isEmpty();   //Checks if its empty
		bool isEmptyInFitRange();   //Checks if its empty in eta fit range
		unsigned getSize();        //Returns the various stored variables in the
		double getETrue(unsigned i);
		double getEcal(unsigned i);
		double getHcal(unsigned i);

		double getETrueAverage();  //AlphaBeta object
		double getETrueRMS();
		double getAlpha();
		double getBeta();
		double getGamma();
		double getSigmaAlpha();
		double getSigmaBeta();
		double getSigmaGamma();

		void correctEcal(unsigned i, double b);
		void correctHcal(unsigned i, double c);
		void computeSigmaEcalHcal();
		void computeETrueAverage();  //Computes the various calibration constants
		void computeETrueRMS();      //and other stored elements in the object.
		bool computeAlphaBeta();
		bool computeAlphaBetaGamma();
		void clear();

};

AlphaBeta::AlphaBeta(double binLowEdge, double binHighEdge, bool _isBarrel) 

{
	binLowEdge_ = binLowEdge;
	binHighEdge_ = binHighEdge;
	isBarrel_ = _isBarrel;

	if(isBarrel_)
	{
		etaMinFit_ = 0.0;
		etaMaxFit_ = 1.2;
	}
	else
	{
		etaMinFit_ = 1.6; //FIXME 1.6
		etaMaxFit_ = 2.8; //FIXME 2.8
	}

	alpha_ = 0;
	beta_ = 0;
	ETrueAverage_ = 0;
	ETrueRMS_ = 0;
	sigmaAlpha_ = 0;
	sigmaBeta_ = 0;
}
bool AlphaBeta::addEntry(double ETrue, double ecal, 
		double hcal, double eta)
{
	double a = 0;

	if(isBarrel_) 
	{

		if(ecal > 0)
			a = aEH;
		else
			a = aH;
	}
	else
	{
		if(ecal > 0)
			a = aEHe;
		else
			a = aHe;
	}
	if((ecal + hcal) < 0.5 || ETrue < 1.0 || 
			ETrue < binLowEdge_ || ETrue > binHighEdge_ || fabs(eta) > etaMaxFit_ || 
			fabs(eta) < etaMinFit_) return false;

	a_.push_back(a);
	ETrueEnergies_.push_back(ETrue);
	ecalEnergies_.push_back(ecal);
	hcalEnergies_.push_back(hcal);
	etas_.push_back(eta);

	return true;
}

double AlphaBeta::getBinLowEdge() {return binLowEdge_;}
double AlphaBeta::getBinHighEdge() {return binHighEdge_;}
double AlphaBeta::getETrueAverage() {return ETrueAverage_;}
double AlphaBeta::getETrueRMS() {return ETrueRMS_;}
double AlphaBeta::getAlpha() {return alpha_;}
double AlphaBeta::getBeta() {return beta_;}
double AlphaBeta::getGamma() {return gamma_;}
double AlphaBeta::getSigmaAlpha() {return sigmaAlpha_;}
double AlphaBeta::getSigmaBeta() {return sigmaBeta_;}
double AlphaBeta::getSigmaGamma() {return sigmaGamma_;}
bool AlphaBeta::isBarrel() {return isBarrel_;}
bool AlphaBeta::isEmpty() 
{
	if(ETrueEnergies_.size() == 0) return true;
	else return false;
}
bool AlphaBeta::isEmptyInFitRange() 
{
	for(unsigned i = 0; i < etas_.size(); i++)
	{
		if(fabs(etas_[i]) < etaMaxFit_ && fabs(etas_[i]) > etaMinFit_)
		{
			return false;
		}
	}
	return true;
}
unsigned AlphaBeta::getSize()
{
	return ETrueEnergies_.size();
}
double AlphaBeta::getETrue(unsigned i){return ETrueEnergies_[i];}
double AlphaBeta::getEcal(unsigned i){return ecalEnergies_[i];}
double AlphaBeta::getHcal(unsigned i){return hcalEnergies_[i];}
void AlphaBeta::correctEcal(unsigned i, double b)
{
	ecalEnergies_[i] = b* ecalEnergies_[i];
}
void AlphaBeta::correctHcal(unsigned i, double c)
{
	hcalEnergies_[i] = c* hcalEnergies_[i];
}
void AlphaBeta::computeSigmaEcalHcal()
{
	double sigmaEcalHcal;
	double ecal;
	double hcal;
	//double a;
	vector<bool> erase;


	for(unsigned entry = 0; entry < ETrueEnergies_.size(); entry++)
	{
		ecal = ecalEnergies_[entry];
		hcal = hcalEnergies_[entry];
		//a = a_[entry];
		erase.push_back(false);

		if(isBarrel_)
			sigmaEcalHcal = sqrt(0.08*0.08 + 1.04*1.04*
					(std::max(ecal + hcal, 1.0)));
		else
			sigmaEcalHcal = sqrt(0.04*0.04 + 1.80*1.80*
					(std::max(ecal + hcal, 1.0)));

		sigmaEcalHcal_.push_back(sigmaEcalHcal);

	}


}
void AlphaBeta::computeETrueAverage()
{
	double totalETrue = 0;
	int numberSkipped = 0;

	for(unsigned i = 0; i < ETrueEnergies_.size(); i++)
	{
		if(fabs(etas_[i]) > etaMaxFit_ || fabs(etas_[i]) < etaMinFit_ ) 
		{
			numberSkipped++;
			continue;
		}   

		totalETrue += ETrueEnergies_[i];
	}

	ETrueAverage_ = totalETrue/(ETrueEnergies_.size() - numberSkipped);
} 
void AlphaBeta::computeETrueRMS()
{
	double totalETrueSquared = 0;
	int numberSkipped = 0;

	for(unsigned i = 0; i<ETrueEnergies_.size(); i++)
	{
		if(fabs(etas_[i]) > etaMaxFit_ || fabs(etas_[i]) < etaMinFit_ ) 
		{
			numberSkipped++;
			continue;
		}

		totalETrueSquared += ETrueEnergies_[i]*ETrueEnergies_[i];
	}

	ETrueRMS_ = sqrt(
			(totalETrueSquared/(ETrueEnergies_.size() - numberSkipped) -
			 ETrueAverage_*ETrueAverage_)/(ETrueEnergies_.size() - numberSkipped)); 
} 



bool AlphaBeta::computeAlphaBeta()
{
	ROOT::Math::SMatrix<double,2, 2, ROOT::Math::MatRepStd<double,2> > coeffs;
	ROOT::Math::SVector<double, 2> consts;
	ROOT::Math::SVector<double, 2> values;
	bool isInverted;
	vector<double> etaPow;


	coeffs(0, 0) = 0;
	coeffs(0, 1) = 0;
	coeffs(1, 0) = 0;
	coeffs(1, 1) = 0;
	consts(0) = 0;
	consts(1) = 0;
	int N=0;

	if(isBarrel_) 
	{
		for(unsigned i = 0; i < etas_.size(); i++) 
			etaPow.push_back(etas_[i]*etas_[i]);


		for(unsigned i = 0; i < etas_.size(); ++i)
		{ 
			if( fabs(ecalEnergies_[i] + hcalEnergies_[i] - ETrueEnergies_[i] + a_[i]) 
					> sigC_*sigmaEcalHcal_[i]) continue;   
			if(hcalEnergies_[i] == 0)continue;

			if(ecalEnergies_[i]>0 ) {
				coeffs(0, 0) += 2.0*
					ecalEnergies_[i]*ecalEnergies_[i]/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

				coeffs(0, 1) += 2.0*etaPow[i]*
					ecalEnergies_[i]*ecalEnergies_[i]/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

				coeffs(1, 0) += 2.0*etaPow[i]*
					ecalEnergies_[i]*ecalEnergies_[i]/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

				coeffs(1, 1) += 2.0*etaPow[i]*etaPow[i]*
					ecalEnergies_[i]*ecalEnergies_[i]/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

				consts(0) += 2.0*(ETrueEnergies_[i] -
						a_[i] - ecalEnergies_[i] - 
						hcalEnergies_[i])*ecalEnergies_[i]/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);  

				consts(1) += 2.0*etaPow[i]*
					(ETrueEnergies_[i] - a_[i] - ecalEnergies_[i] - 
					 hcalEnergies_[i])*ecalEnergies_[i]/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);
			}
			else {
				coeffs(0, 0) += 2.0*
					(factorB*ecalEnergies_[i] + hcalEnergies_[i])*
					(factorB*ecalEnergies_[i] + hcalEnergies_[i])/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

				coeffs(0, 1) += 2.0*etaPow[i]*
					(factorB*ecalEnergies_[i] + hcalEnergies_[i])*
					(factorB*ecalEnergies_[i] + hcalEnergies_[i])/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

				coeffs(1, 0) += 2.0*etaPow[i]*
					(factorB*ecalEnergies_[i] + hcalEnergies_[i])*
					(factorB*ecalEnergies_[i] + hcalEnergies_[i])/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

				coeffs(1, 1) += 2.0*etaPow[i]*etaPow[i]*
					(factorB*ecalEnergies_[i] + hcalEnergies_[i])*
					(factorB*ecalEnergies_[i] + hcalEnergies_[i])/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

				consts(0) += 2.0*
					(ETrueEnergies_[i] - a_[i] - ecalEnergies_[i] - 
					 hcalEnergies_[i])*
					(factorB*ecalEnergies_[i] + hcalEnergies_[i])/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);  

				consts(1) += 2.0*etaPow[i]*
					(ETrueEnergies_[i] - a_[i] - ecalEnergies_[i] - 
					 hcalEnergies_[i])*
					(factorB*ecalEnergies_[i] + hcalEnergies_[i])/
					(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);
			}

		}
	}
	else
	{

		for(unsigned i = 0; i < etas_.size(); i++) 
			//etaPow.push_back((fabs(etas_[i]))*(fabs(etas_[i]) ) *  (fabs(etas_[i]))*(fabs(etas_[i]) ) );
			etaPow.push_back((fabs(etas_[i]) - 1.5)*(fabs(etas_[i]) - 1.5)  
					*(fabs(etas_[i]) - 1.5)*(fabs(etas_[i]) - 1.5));

		for(unsigned i = 0; i < etas_.size(); ++i)
		{  
			if ( fabs(ecalEnergies_[i] + hcalEnergies_[i] - ETrueEnergies_[i] + a_[i]) > sigC_*sigmaEcalHcal_[i]) continue;             
			if(hcalEnergies_[i] == 0)continue;

			N++;

			coeffs(0, 0) += 2.0*
				(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
				(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
				(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

			coeffs(0, 1) += 2.0*etaPow[i]*
				(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
				(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
				(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

			coeffs(1, 0) += 2.0*etaPow[i]*
				(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
				(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
				(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

			coeffs(1, 1) += 2.0*etaPow[i]*etaPow[i]*
				(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
				(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
				(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

			consts(0) += 2.0*
				(ETrueEnergies_[i] - a_[i] - ecalEnergies_[i] - 
				 hcalEnergies_[i])*
				(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
				(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);  

			consts(1) += 2.0*etaPow[i]*
				(ETrueEnergies_[i] - a_[i] - ecalEnergies_[i] - 
				 hcalEnergies_[i])*
				(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
				(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);
		}
		// coeffs.Print(cout);
		// cout<<"N = "<<N<<endl;
	}

	//Create the matrix that will be inverted and the vector which will multiply
	//that matrix to find the alpha and beta calibration constants.


	isInverted = coeffs.Invert();

	if(isInverted && sqrt(coeffs(0,0)) < 100000)
	{
		values = coeffs*consts;

		alpha_ = values(0);
		beta_ = values(1);
		sigmaAlpha_ = sqrt(coeffs(0,0));
		sigmaBeta_ = sqrt(coeffs(1,1));

		return true;
	}
	else
	{
		return false;
	}
} 


bool AlphaBeta::computeAlphaBetaGamma()
{
	ROOT::Math::SMatrix<double,3, 3, ROOT::Math::MatRepStd<double,3> > coeffs;
	ROOT::Math::SVector<double, 3> consts;
	ROOT::Math::SVector<double, 3> values;
	bool isInverted;
	vector<double> etaPow2;
	vector<double> etaPow;

	coeffs(0, 0) = 0;
	coeffs(0, 1) = 0;
	coeffs(0, 2) = 0;
	coeffs(1, 0) = 0;
	coeffs(1, 1) = 0;
	coeffs(1, 2) = 0;
	coeffs(2, 0) = 0;
	coeffs(2, 1) = 0;
	coeffs(2, 2) = 0;
	consts(0) = 0;
	consts(1) = 0;
	consts(2) = 0;

	int N=0;

	for(unsigned i = 0; i < etas_.size(); i++)  {
		// etaPow.push_back(etas_[i]*etas_[i]);
		etaPow.push_back(fabs(etas_[i]));
		etaPow2.push_back(fabs(etas_[i])*fabs(etas_[i]) );

	}

	for(unsigned i = 0; i < etas_.size(); ++i)
	{  
		if ( fabs(ecalEnergies_[i] + hcalEnergies_[i] - ETrueEnergies_[i] + a_[i]) > sigC_*sigmaEcalHcal_[i]) continue;             
		if(hcalEnergies_[i] == 0)continue;

		N++;

		coeffs(0, 0) += 2.0*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		coeffs(0, 1) += 2.0*etaPow[i]*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		coeffs(0, 2) += 2.0*etaPow2[i]*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		coeffs(1, 0) += 2.0*etaPow[i]*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		coeffs(1, 1) += 2.0*etaPow2[i]*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		coeffs(1, 2) += 2.0*etaPow2[i]*etaPow[i]*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		coeffs(2, 0) += 2.0*etaPow2[i]*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		coeffs(2, 1) += 2.0*etaPow2[i]*etaPow[i]*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		coeffs(2, 2) += 2.0*etaPow2[i]*etaPow2[i]*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);


		consts(0) += 2.0*
			(ETrueEnergies_[i] - a_[i] - ecalEnergies_[i] - 
			 hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);  

		consts(1) += 2.0*etaPow[i]*
			(ETrueEnergies_[i] - a_[i] - ecalEnergies_[i] - 
			 hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);

		consts(2) += 2.0*etaPow2[i]*
			(ETrueEnergies_[i] - a_[i] - ecalEnergies_[i] - 
			 hcalEnergies_[i])*
			(factorE*ecalEnergies_[i] + hcalEnergies_[i])/
			(sigmaEcalHcal_[i]*sigmaEcalHcal_[i]);
	}


	//Create the matrix that will be inverted and the vector which will multiply
	//that matrix to find the alpha and beta calibration constants.
	//    cout<<" N= "<<N<<endl;
	// coeffs.Print(cout);
	if(N==0) return false;
	isInverted = coeffs.Invert();
	// coeffs.Print(cout); cout<<endl;
	// consts.Print(cout);

	if(isInverted && sqrt(coeffs(0,0)) < 100000)
	{
		values = coeffs*consts;

		alpha_ = values(0);
		gamma_ = values(1);
		beta_ = values(2);

		//      cout<<endl<<alpha_<<"   "<<gamma_<<"   "<<beta_<<endl;

		sigmaAlpha_ = sqrt(coeffs(0,0));
		sigmaGamma_ = sqrt(coeffs(1,1));
		sigmaBeta_ = sqrt(coeffs(2,2));


		return true;
	}
	else
	{
		return false;
	}
} 





void AlphaBeta::clear()
{
	ETrueEnergies_.clear();
	ecalEnergies_.clear();
	hcalEnergies_.clear();
	etas_.clear();

	delete &binLowEdge_;
	delete &binHighEdge_;
	delete &isBarrel_;
	delete &ETrueAverage_;
	delete &ETrueRMS_;
	delete &a_;
	delete &alpha_;
	delete &beta_;
	delete &sigmaAlpha_;
	delete &sigmaBeta_;
}








///////////////////////////////////////////////////////////////////////////////
//The class that holds the calibration information over all values of ETrue. 
//It takes in a collection of ABC objects and fits each calibration 
//constant to a function. These functions are then used to find the calibrated
//energy.
///////////////////////////////////////////////////////////////////////////////
class Calibration
{
	private:
		double ETrueMax_;
		bool isBarrel_;

		vector<double> ETrueMeansABC_;
		vector<double> ETrueRMSsABC_;
		vector<double> ETrueMeansAlphaBeta_;
		vector<double> ETrueRMSsAlphaBeta_;

		vector<double> as_;
		vector<double> bs_;
		vector<double> cs_;
		vector<double> alphas_;
		vector<double> betas_;
		vector<double> gammas_;

		vector<double> sigmaBs_;
		vector<double> sigmaCs_;
		vector<double> sigmaAlphas_;
		vector<double> sigmaBetas_;
		vector<double> sigmaGammas_;

		TGraph *graphA_ ;
		TGraphErrors *graphB_;
		TGraphErrors *graphC_;
		TGraphErrors *graphAlpha_;
		TGraphErrors *graphBeta_ ;
		TGraphErrors *graphGamma_ ;

		TGraph *graphBError_;
		TGraph *graphCError_;
		TGraph *graphAlphaError_;
		TGraph *graphBetaError_ ;
		TF1* functionA_;
		TF1* functionB_;
		TF1* functionC_;
		TF1* functionAlpha_;
		TF1* functionBeta_;
		TF1* functionGamma_;

	public:
		Calibration();
		Calibration(double ETrueMax, bool isBarrel);
		//Adds a graph point by hand, i.e. putting in the individual values.
		void addGraphPoints(double ETrueAverage, double ETrueRMS,
				double a, double b, double sigmaB, double C,
				double sigmaC, double alpha, double sigmaAlpha,
				double beta, double sigmaBeta,
				double gamma, double sigmaGamma ); 
		//Adds a graph point by taking apart an ABC object.
		void addGraphPoints(ABC* abc);
		void addGraphPoints( AlphaBeta* alphabeta);
		//Creates the graphs after the points have been added.
		void initializeGraphs(string option);  
		double getETrueMax();      //Returns the various objects  that the 
		TGraphErrors* getGraph();  //calibration class holds.
		TF1* getFunctionA();
		TF1* getFunctionB();
		TF1* getFunctionC();
		TF1* getFunctionAlpha();
		TF1* getFunctionBeta();   
		TF1* getFunctionGamma();   
		//Returns calibrated energy without any eta dependence.
		double getCalibratedEnergy(double ETrue, double ecalEnergy, 
				double hcalEnergy); 
		//Returns calibrated energy with eta dependence.
		double getCalibratedEnergy(double ETrue, double ecalEnergy, 
				double hcalEnergy, double eta);
		//and with advanced pol dependency
		double getCalibratedEnergyWithGamma(double ETrue, double ecalEnergy, 
				double hcalEnergy, double eta);

		void setETrueMax(double ETrueMax);
		bool fitAsToFunction(TF1 *functionA);  //Fits the functions to their 
		bool fitAsToFunction();                //graph points. One that takes in
		bool fitBsToFunction(TF1 *functionB);  //a function which then fits it to
		bool fitBsToFunction();                //that function, and one that is
		bool fitCsToFunction(TF1 *functionC);  //used to simply improve the fit.
		bool fitCsToFunction();
		bool fitAlphasToFunction(TF1 *functionAlpha);
		bool fitAlphasToFunction();
		bool fitBetasToFunction(TF1 *functionBetas);
		bool fitBetasToFunction();
		bool fitGammasToFunction(TF1 *functionGammas);
		bool fitGammasToFunction();

		bool setAlphasToFunction(TF1 *functionAlpha);
		bool setBetasToFunction(TF1 *functionBeta);

		void drawCoeffGraph(string graph, string tag, string outFileName);  //Makes and draws a graph of a 
		void drawSigmaGraph(string graph);  //coefficient. Takes in as an 
		//argument a, b, c, alpha, or beta.
		void printBs();
		void printCs();
		void printBetas();
		void printAlphas();
		void printGammas();
};

Calibration::Calibration()
{
	ETrueMax_ = 1000;
	isBarrel_ = true;
}
Calibration::Calibration(double ETrueMax, bool isBarrel) 

{
	ETrueMax_ = ETrueMax;
	isBarrel_ = isBarrel;
}
void Calibration::addGraphPoints(double ETrueAverage, double ETrueRMS,
		double a, double b, double sigmaB, double c,
		double sigmaC, double alpha, 
		double sigmaAlpha, double beta,
		double sigmaBeta, double gamma,
		double sigmaGamma)
{
	ETrueMeansABC_.push_back(ETrueAverage);
	ETrueRMSsABC_.push_back(ETrueRMS);
	as_.push_back(a);
	bs_.push_back(b);
	cs_.push_back(c);
	alphas_.push_back(alpha);
	betas_.push_back(beta);
	gammas_.push_back(gamma);


	sigmaBs_.push_back(sigmaB);
	sigmaCs_.push_back(sigmaC);
	sigmaAlphas_.push_back(sigmaAlpha);
	sigmaBetas_.push_back(sigmaBeta);
	sigmaGammas_.push_back(sigmaGamma);

}
void Calibration::addGraphPoints(ABC* abc)
{
	if(abc->isEmpty() || (abc->getSigmaC() == 0 && abc->getC() == 0)) return;

	ETrueMeansABC_.push_back(abc->getETrueAverage());
	ETrueRMSsABC_.push_back(abc->getETrueRMS());
	as_.push_back(abc->getA());
	bs_.push_back(abc->getB());
	cs_.push_back(abc->getC());


	sigmaBs_.push_back(abc->getSigmaB());
	sigmaCs_.push_back(abc->getSigmaC());
}

void Calibration::addGraphPoints(AlphaBeta* alphabeta)
{
	if(alphabeta->isEmpty()|| 
			(alphabeta->getSigmaBeta() == 0 && alphabeta->getBeta() == 0)) return;


	ETrueMeansAlphaBeta_.push_back(alphabeta->getETrueAverage());
	ETrueRMSsAlphaBeta_.push_back(alphabeta->getETrueRMS());
	alphas_.push_back(alphabeta->getAlpha());
	betas_.push_back(alphabeta->getBeta());
	gammas_.push_back(alphabeta->getGamma());
	sigmaAlphas_.push_back(alphabeta->getSigmaAlpha());
	sigmaBetas_.push_back(alphabeta->getSigmaBeta());
	sigmaGammas_.push_back(alphabeta->getSigmaGamma());

}
void Calibration::initializeGraphs(string option)
{
	vector<double> x;
	vector<double> sigmaX;
	vector<double> y;
	vector<double> sigmaY;

	if(option == "abc" || option == "ABC" || option == "all")
	{
		for(unsigned i = 0; i < ETrueMeansABC_.size(); i++)
		{
			if( bs_[i] == 0 && sigmaBs_[i] == 0.0) continue;

			x.push_back(ETrueMeansABC_[i]);
			sigmaX.push_back(ETrueRMSsABC_[i]);
			y.push_back(bs_[i]);
			sigmaY.push_back(sigmaBs_[i]);

		}

		graphB_ = new TGraphErrors(x.size(), &x[0], &y[0], &sigmaX[0], 
				&sigmaY[0]);

		x.clear();
		sigmaX.clear();
		y.clear();
		sigmaY.clear();

		for(unsigned i = 0; i < ETrueMeansABC_.size(); i++)
		{
			if( cs_[i] == 0 && sigmaCs_[i] == 0.0) continue;

			x.push_back(ETrueMeansABC_[i]);
			sigmaX.push_back(ETrueRMSsABC_[i]);
			y.push_back(cs_[i]);
			sigmaY.push_back(sigmaCs_[i]);

		}

		graphC_ = new TGraphErrors(x.size(), &x[0], &y[0], &sigmaX[0], 
				&sigmaY[0]);

		x.clear();
		sigmaX.clear();
		y.clear();
		sigmaY.clear();
	}
	if(option == "AlphaBeta" || option == "alphabeta" || 
			option == "alphaBeta" || option == "ALPHABETA" || option == "all")
	{      
		for(unsigned i = 0; i < ETrueMeansAlphaBeta_.size(); i++)
		{
			if( alphas_[i] == 0 && sigmaAlphas_[i] == 0.0) continue;

			x.push_back(ETrueMeansAlphaBeta_[i]);
			sigmaX.push_back(ETrueRMSsAlphaBeta_[i]);
			y.push_back(alphas_[i]);
			sigmaY.push_back(sigmaAlphas_[i]);

		}

		graphAlpha_ = new TGraphErrors(x.size(), &x[0], &y[0], &sigmaX[0], 
				&sigmaY[0]);
		x.clear();
		sigmaX.clear();
		y.clear();
		sigmaY.clear();

		for(unsigned i = 0; i < ETrueMeansAlphaBeta_.size(); i++)
		{
			if( betas_[i] == 0 && sigmaBetas_[i] == 0.0) continue;

			x.push_back(ETrueMeansAlphaBeta_[i]);
			sigmaX.push_back(ETrueRMSsAlphaBeta_[i]);
			y.push_back(betas_[i]);
			sigmaY.push_back(sigmaBetas_[i]);

		}

		graphBeta_ = new TGraphErrors(x.size(), &x[0], &y[0], &sigmaX[0], 
				&sigmaY[0]);

		x.clear();
		sigmaX.clear();
		y.clear();
		sigmaY.clear();

		for(unsigned i = 0; i < ETrueMeansAlphaBeta_.size(); i++)
		{
			if( betas_[i] == 0 && sigmaGammas_[i] == 0.0) continue;

			x.push_back(ETrueMeansAlphaBeta_[i]);
			sigmaX.push_back(ETrueRMSsAlphaBeta_[i]);
			y.push_back(gammas_[i]);
			sigmaY.push_back(sigmaGammas_[i]);

		}

		graphGamma_ = new TGraphErrors(x.size(), &x[0], &y[0], &sigmaX[0], 
				&sigmaY[0]);

		x.clear();
		sigmaX.clear();
		y.clear();
		sigmaY.clear();



	}

}
double Calibration::getETrueMax() {return ETrueMax_;}
TGraphErrors* Calibration::getGraph() {return graphB_;}
TF1* Calibration::getFunctionA() {return functionA_;}
TF1* Calibration::getFunctionB() {return functionB_;}
TF1* Calibration::getFunctionC() {return functionC_;}
TF1* Calibration::getFunctionAlpha() {return functionAlpha_;}
TF1* Calibration::getFunctionBeta() {return functionBeta_;}
TF1* Calibration::getFunctionGamma() {return functionGamma_;}
double Calibration::getCalibratedEnergy(double ETrue, double ecalEnergy, 
		double hcalEnergy)
{
	double a = functionA_->Eval(ETrue);
	double b = functionB_->Eval(ETrue);
	double c = functionC_->Eval(ETrue);

	return a+ b*ecalEnergy + c*hcalEnergy;
}
double Calibration::getCalibratedEnergy(double ETrue, double ecalEnergy, 
		double hcalEnergy, double eta)
{
	double etaPow;
	double factor_;
	double a = functionA_->Eval(ETrue);
	double b = functionB_->Eval(ETrue);
	double c = functionC_->Eval(ETrue);
	double alpha = functionAlpha_->Eval(ETrue);
	double beta = functionBeta_->Eval(ETrue);
	double counterAlpha = 0;
	double counterBeta = 0;

	if(isBarrel_) 
	{
		etaPow = eta*eta;
		factor_ = factorB;
		if(ecalEnergy>0) {  //shubham
			counterAlpha = alpha;
			counterBeta = beta;
		}

	}
	else 
	{

		if(ecalEnergy > 0) {
			etaPow = 0.04 + (fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5) ;
			/*
				 if (fabs(eta) < 2.5) {
			//etaPow = 0.6 + (fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5) ;
			etaPow =  1.8*(fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5) ;
			}
			else {
			etaPow = -0.6 + (fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5) ;
			}
			*/
		}
		else  // H hadrons here
		{

			if( fabs(eta)<2.5) {
				etaPow=0.05;
			}
			else  {
				etaPow = 0.04 + (fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5) ;
				//etaPow = (fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5) ;

				//Giving better result
				//etaPow = -0.6*(fabs(eta) - 1.5)*(fabs(eta) - 1.5) + 1.1*(fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5)*(fabs(eta) - 1.5);
			}

		}
		factor_ = factorE;

	}



	// if(fabs(eta)>1.5 && ecalEnergy==0)
	//   cout<<alpha<<"  "<<beta<<"   "<<ETrue<<endl;

	return a + (1.0 + alpha + factor_*beta*etaPow)*b*ecalEnergy + 
		(1.0 + alpha + beta*etaPow - counterAlpha - counterBeta*etaPow)*
		c*hcalEnergy;
}

double Calibration::getCalibratedEnergyWithGamma(double ETrue, double ecalEnergy, 
		double hcalEnergy, double eta)
{
	// double etaPow;
	// double etaPow2;

	//spandey change 3 oct, 2017
	double etaPow = 0;
	double etaPow2 = 0;

	double factor_;
	double a = functionA_->Eval(ETrue);
	double b = functionB_->Eval(ETrue);
	double c = functionC_->Eval(ETrue);
	double alpha = functionAlpha_->Eval(ETrue);
	double beta = functionBeta_->Eval(ETrue);
	double gamma = functionGamma_->Eval(ETrue);
	double counterAlpha = 0;
	double counterBeta = 0;

	if(isBarrel_) 
	{
		etaPow = eta*eta;
		factor_ = factorB;
		if(ecalEnergy>0) {
			counterAlpha = alpha;
			counterBeta = beta;
		}
		gamma = 0;
	}
	else 
	{
		etaPow = fabs(eta);
		etaPow2 = fabs(eta)*fabs(eta) ;
		// etaPow = eta*eta;
		factor_ = factorE;
	}

	// if(fabs(eta)>1.5 && ecalEnergy==0)
	//   cout<<alpha<<"  "<<beta<<"   "<<ETrue<<endl;

	return a + (1.0 + alpha + gamma*etaPow + factor_*beta*etaPow2)*b*ecalEnergy + 
		(1.0 + alpha + gamma*etaPow + beta*etaPow2 - counterAlpha - counterBeta*etaPow)*
		c*hcalEnergy;
}



void Calibration::setETrueMax(double ETrueMax){ETrueMax_ = ETrueMax;}


bool Calibration::fitAsToFunction(TF1 *functionA)
{
	functionA_ = functionA;
	//   graphA_->Fit(functionA_->GetName(), "Q", "", 0, ETrueMax_);
	return true;
}
bool Calibration::fitAsToFunction()
{
	graphA_->Fit(functionA_->GetName(), "Q", "", 0, ETrueMax_);
	return true;
}

bool Calibration::fitBsToFunction(TF1 *functionB)
{
	functionB_ = functionB;
	graphB_->Fit(functionB_->GetName(), "Q", "", 1.5, ETrueMax_);
	return true;
}
bool Calibration::fitBsToFunction()
{
	graphB_->Fit(functionB_->GetName(), "Q", "", 1.5, ETrueMax_);
	return true;
}
bool Calibration::fitCsToFunction(TF1 *functionC)
{
	functionC_ = functionC;
	graphC_->Fit(functionC_->GetName(), "Q", "", 1.5, ETrueMax_);

	return true;
}
bool Calibration::fitCsToFunction()
{
	graphC_->Fit(functionC_->GetName(), "Q", "", 1.5, ETrueMax_);
	return true;
}

bool Calibration::setAlphasToFunction(TF1 *functionAlpha)
{
	functionAlpha_ = functionAlpha;
	return true;
}

bool Calibration::fitAlphasToFunction(TF1 *functionAlpha)
{
	functionAlpha_ = functionAlpha;
	graphAlpha_->Fit(functionAlpha_->GetName(), "Q", "", 2., ETrueMax_); //2.
	return true;
}
bool Calibration::fitAlphasToFunction()
{
	graphAlpha_->Fit(functionAlpha_->GetName(), "Q", "", 2., ETrueMax_); //2.
	return true;
}

bool Calibration::setBetasToFunction(TF1 *functionBeta)
{
	functionBeta_ = functionBeta;
	return true;
}

bool Calibration::fitBetasToFunction(TF1 *functionBeta)
{
	functionBeta_ = functionBeta;
	graphBeta_->Fit(functionBeta_->GetName(), "Q", "", 2.0, ETrueMax_);
	return true;
}
bool Calibration::fitBetasToFunction()
{
	graphBeta_->Fit(functionBeta_->GetName(), "Q", "", 2.0, ETrueMax_);
	return true;
}

bool Calibration::fitGammasToFunction(TF1 *functionGamma)
{
	functionGamma_ = functionGamma;
	graphGamma_->Fit(functionGamma_->GetName(), "Q", "", 2.0, ETrueMax_);
	return true;
}
bool Calibration::fitGammasToFunction()
{
	graphGamma_->Fit(functionGamma_->GetName(), "Q", "", 2.0, ETrueMax_);
	return true;
}



void Calibration::drawCoeffGraph(string graph, string tag, string outFileName)
{
	string rootOut = outFileName+".root";
	TFile *fout_ = new TFile(rootOut.c_str(),"RECREATE");

	//  cout<<" Tag = "<<tag<<endl;

	string saveString;
	//TCanvas* canvas = new TCanvas( (graph+tag).c_str() , graph.c_str(), 1200,600 );
	TCanvas* canvas = new TCanvas( (graph+tag).c_str() , graph.c_str(), 1000,600 );
	TH2F* histo = new TH2F("histoCG", "", sampleRangeHigh, 0, sampleRangeHigh, sampleRangeHigh,  -3.0, 3.0); 

	canvas->cd();
	histo->SetStats(0);
	histo->GetXaxis()->SetTitle("True Energy(GeV)");
	histo->GetYaxis()->SetTitle("Value");
	histo->Draw();

	gPad->SetGridx();
	gPad->SetGridy();

	// TLegend* leg=new TLegend(0.53,0.23,0.91,0.44);
	// leg->SetFillColor(0); leg->SetShadowColor(0);
	// TLine* line=new TLine(0,0,0,0);
	if(graph == "a" || graph == "A") 
	{
		histo->SetTitle("A Parameter");
		graphB_->SetTitle("A vs True Energy");
		histo->GetYaxis()->SetTitle( ("A coefficient ("+tag+")").c_str() );
		graphB_->SetMarkerStyle(22);
		graphB_->SetMarkerSize(1);
		graphB_->SetFillColor(0);

		graphB_->Draw("P");
		// if(tag=="EH") {
		// 	faBarrel->Draw("Lsame+");
		//   	faBarrel52x->Draw("Lsame+");
		// }

		//  leg->AddEntry(

		saveString = "ACoefficient" + tag + ".png";
		canvas->SaveAs(saveString.c_str());
		graphB_->Write();
	}
	if(graph == "b" || graph == "B") 
	{
		histo->SetTitle("B Parameter");
		graphC_->SetTitle("B vs True Energy");
		histo->GetYaxis()->SetTitle( ("B coefficient ("+tag+")").c_str() );
		graphC_->SetMarkerStyle(22);
		graphC_->SetMarkerSize(1);
		graphC_->SetFillColor(0);

		graphC_->Draw("P");
		// if(tag=="EH") {
		// 	faBarrel->Draw("Lsame+");
		//   	faBarrel52x->Draw("Lsame+");
		//}

		//  leg->AddEntry(

		saveString = "BCoefficient" + tag + ".png";
		canvas->SaveAs(saveString.c_str());
		graphC_->Write();
	}
	else if(graph == "c" || graph == "C") 
	{
		histo->SetTitle("C parameter");
		graphC_->SetTitle("C vs True Energy");
		histo->GetYaxis()->SetTitle( ("C coefficient ("+tag+")").c_str() );
		graphC_->SetMarkerStyle(22);
		graphC_->SetMarkerSize(1);
		//graphC_->SetMarkerColor(1);
		graphC_->SetFillColor(0);

		graphC_->Draw("P");
		// if(tag=="EH") {
		// 	fbBarrel->Draw("Lsame+");
		// 	//   	fbBarrel52x->Draw("Lsame+");
		// }
		// else {
		// 	fcBarrel->Draw("Lsame+");
		// 	//    	fcBarrel52x->Draw("Lsame+");
		// }

		saveString = "CCoefficient" + tag + ".png";
		canvas->SaveAs(saveString.c_str());
		graphC_->Write();
	}
	else if(graph == "alpha" || graph == "Alpha") 
	{
		histo->SetTitle("Alpha parameter");
		graphAlpha_->SetTitle("Alpha vs True Energy");
		histo->GetYaxis()->SetTitle( ("#alpha coefficient ("+tag+")").c_str() );
		graphAlpha_->SetMarkerStyle(22);
		graphAlpha_->SetMarkerSize(1);
		graphAlpha_->SetMarkerColor(2);
		graphAlpha_->SetFillColor(0);

		graphAlpha_->Draw("P");
		faEtaBarrel->Draw("Lsame+");
		//   faEtaBarrel52x->Draw("Lsame+");

		saveString = "AlphaCoefficient" + tag + ".png";
		canvas->SaveAs(saveString.c_str());
		graphAlpha_->Write();
	}
	else if(graph == "beta" || graph == "Beta") 
	{
		histo->SetTitle("Beta parameter");
		graphBeta_->SetTitle("Beta vs True Energy");
		histo->GetYaxis()->SetTitle( ("#beta coefficient ("+tag+")").c_str() );
		graphBeta_->SetMarkerStyle(22);
		graphBeta_->SetMarkerSize(1);
		graphBeta_->SetMarkerColor(2);
		graphBeta_->SetFillColor(0);

		graphBeta_->Draw("P");
		fbEtaBarrel->Draw("Lsame+");
		//    fbEtaBarrel52x->Draw("Lsame+");

		saveString = "BetaCoefficient" + tag + ".png";
		canvas->SaveAs(saveString.c_str());
		graphBeta_->Write();
	}  
	else if(graph == "gamma" || graph == "Gamma") 
	{
		histo->SetTitle("Gamma parameter");
		graphGamma_->SetTitle("Gamma vs True Energy");
		histo->GetYaxis()->SetTitle( ("#gamma coefficient ("+tag+")").c_str() );
		graphGamma_->SetMarkerStyle(22);
		graphGamma_->SetMarkerSize(1);
		graphGamma_->SetMarkerColor(2);
		graphGamma_->SetFillColor(0);

		graphGamma_->Draw("P");
		// fbEtaBarrel->Draw("Lsame+");
		// fbEtaBarrel52x->Draw("Lsame+");

		saveString = "GammaCoefficient" + tag + ".png";
		canvas->SaveAs(saveString.c_str());
		graphGamma_->Write();
	}  



	else cout << "No graph with that name" <<endl;

	TLine* line=new TLine(1,2,1,2);
	line->SetLineColor(kRed+1);
	line->SetLineWidth(2);


	// leg->AddEntry(line,"coef 52X (new PF Ecal cluster calib)","l");
	fout_->Write();
	fout_->Close();


}
void Calibration::drawSigmaGraph(string graph)
{

	TCanvas* canvas2 = new TCanvas();
	TH2F* histo2 = new TH2F("histoS", "", 100, 0, ETrueMax_, 100,  0, .1); 

	canvas2->cd();
	histo2->SetStats(0);
	histo2->Draw();

	gPad->SetGridx();
	gPad->SetGridy();

	if(graph == "b" || graph =="B")
	{
		graphBError_->SetMarkerStyle(22);
		graphBError_->SetMarkerColor(2);
		graphBError_->SetMarkerSize(.5);
		graphBError_->Draw("P");

	}
	else if(graph == "c" || graph =="C")
	{
		graphCError_->SetMarkerStyle(22);
		graphCError_->SetMarkerColor(2);
		graphCError_->SetMarkerSize(.5);
		graphCError_->Draw("P");
	}
	else if(graph == "alpha" || graph =="Alpha")
	{
		graphAlphaError_->SetMarkerStyle(22);
		graphAlphaError_->SetMarkerColor(2);
		graphAlphaError_->SetMarkerSize(.5);
		graphAlphaError_->Draw("P");
	}
	else if(graph == "beta" || graph =="Beta")
	{
		graphBetaError_->SetMarkerStyle(22);
		graphBetaError_->SetMarkerColor(2);
		graphBetaError_->SetMarkerSize(.5);
		graphBetaError_->Draw("P");
	}
	else cout<<"No graph with that name"<<endl;

	delete histo2;

}
void Calibration::printBs()
{

	for(unsigned i = 0; i < as_.size(); i++)
	{
		cout<<bs_[i];
	}
}

void Calibration::printCs()
{

	for(unsigned i = 0; i < as_.size(); i++)
	{
		cout<<cs_[i]<<endl;
	}
}
void Calibration::printBetas()
{

	for(unsigned i = 0; i < betas_.size(); i++)
	{
		cout<<betas_[i];
	}
}
void Calibration::printAlphas()
{

	for(unsigned i = 0; i < alphas_.size(); i++)
	{
		cout<<"Alphas: "<<alphas_[i]<<endl;;
	}
}

void Calibration::printGammas()
{

	for(unsigned i = 0; i < gammas_.size(); i++)
	{
		cout<<"Gammas: "<<gammas_[i]<<endl;;
	}
}
///////////////////////////////////////////////////////////////////////////////
//Global functions used in the main of the code.
///////////////////////////////////////////////////////////////////////////////


//Takes apart a TH2 and creates response and resolution plots from it. Note: 
//the TGraphs will not draw correctly without passing the TGraphs as references
//to the function.

void drawGausFit(TH2F* inHisto, TGraph* response, TGraph* resolution, TString resolution_out)
{

	if(inHisto->GetEntries() == 0) return;

	vector<TH1F*> ETrueBin;
	TF1* gaus; 
	string name;
	char num[4];
	float rebin = 1.;
	TCanvas* canvas;
	TCanvas* temp = new TCanvas();
	//TLine *line = new TLine(0.0,0.0,sampleRangeHigh,0.0);
	int rangelow_ = 0, rangehigh_ = sampleRangeHigh, bins_ = sampleRangeHigh;

	if (drawpT) {
		rangehigh_ = 100;
		bins_ = 100;
	}
	TLine *line = new TLine(0.0,0.0,rangehigh_,0.0);

	// TH2F* respHisto = new TH2F("respHisto", "", sampleRangeHigh, 0, sampleRangeHigh, 100, -0.5, 0.5);
	// //TH2F* resoHisto = new TH2F("resoHisto", "", sampleRangeHigh, 0, sampleRangeHigh, 100, 0.0, 0.5);
	// TH2F* resoHisto = new TH2F("resoHisto", "", sampleRangeHigh, 0, sampleRangeHigh, 200, 0.0, 1.0);

	TH2F* respHisto = new TH2F("respHisto", "", bins_, rangelow_, rangehigh_, 100, -0.5, 0.5);
	//TH2F* resoHisto = new TH2F("resoHisto", "", sampleRangeHigh, 0, sampleRangeHigh, 100, 0.0, 0.5);
	TH2F* resoHisto = new TH2F("resoHisto", "", bins_, rangelow_, rangehigh_, 200, 0.0, 1.0);



	TGraph* averages;
	TGraph* rmss;

	vector<double> ETrue;
	vector<double> gausMean; 
	vector<double> gausSigma;
	vector<double> average;
	vector<double> rms;

	TFile* file1=new TFile(resolution_out+"_projections.root","recreate");


	temp->cd();//This TCanvas is only used since when we do the fit down below 
	//it creates an unwanted TCanvas. We will get rid of it later on 
	//in the function.

	// TCanvas* cccc=new TCanvas("balda","bacla");
	//cout<<"ETrue.back(), gausMean[0].back()"<<endl;
	//cout<<"**********Draw Gaus**********"<<endl;

	cout << resolution_out << endl;

	for(unsigned bin = 2; bin < sampleRangeHigh; )
	{
		name = "histcorhybrid";
		sprintf(num, "%i", bin);
		name += num;
		//Split up the TH2 into many TH1's for each ETrue bin.

		ETrueBin.push_back((TH1F*)inHisto->ProjectionY(name.c_str(),bin, 
					bin + 4*rebin));
		//cout <<"bin to  bin + 4*rebin: "<<bin<<" to "<<(bin + 4*rebin)<<endl;//"   "<<ETrueBin.back()->GetEntries()<<endl;
		//if(ETrueBin.back()->GetEntries() > 5)
		if(ETrueBin.back()->Integral() > 5)
		{
			//Fit each ETrue bin to a gaus (iteratively done to get better fit)
			//cout<<"ETrueBin.back()->GetEntries():"<<ETrueBin.back()->GetEntries()<<endl;
			if(bin > 2) {

				gaus =new TF1("gaus","gaus(0)",-3,3);
				gaus->SetParameters(500.,0.,0.2);
				ETrueBin.back()->Fit("gaus", "Q", "", -1.0, 0.4);
				//ETrueBin.back()->Fit("gaus", "Q", "", -0.7, 0.7);


				gaus = ETrueBin.back()->GetFunction("gaus");
				//cout<<name<<" "<<gaus->GetParameter(1)<<"   "<<gaus->GetParameter(2)<<endl;

				if(gaus->GetParameter(2) < 0)
					goto here1;
				ETrueBin.back()->Fit("gaus", "Q", "",
						gaus->GetParameter(1) - 2*gaus->
						GetParameter(2), 0.4);  
				gaus = ETrueBin.back()->GetFunction("gaus");

				ETrueBin.back()->Fit("gaus", "Q", "",
						gaus->GetParameter(1) - 2*gaus->
						GetParameter(2), 0.4);
				gaus = ETrueBin.back()->GetFunction("gaus");

here1:
				// if(bin<=16)
				// gausMean.push_back(ETrueBin.back()->GetMean());
				// else


				//gausSigma.push_back(gaus->GetParameter(2)/(1.0 + min(0.0, gaus->GetParameter(1))));

				if (useMean) {
					gausMean.push_back(ETrueBin.back()->GetMean());
					gausSigma.push_back(ETrueBin.back()->GetRMS()/(1.0 + min(0.0, ETrueBin.back()->GetMean())));
				}

				else {
					gausMean.push_back(gaus->GetParameter(1));
					gausSigma.push_back(gaus->GetParameter(2)/(1.0 + min(0.0, gaus->GetParameter(1))));
					//gausSigma.push_back(gaus->GetParameter(2)/sqrt(ETrueBin.back()->Integral()));
				}
				//gausMean.push_back(gaus->GetParameter(1));
				// if (bin > 24 || bin == 2) {
				//   gausMean.push_back(gaus->GetParameter(1));
				// }
				// else {
				//   gausMean.push_back(ETrueBin.back()->GetMean());
				//   gaus->Delete();
				// }

			}
			else {

				gaus =new TF1("gaus","gaus",-3,3);
				gaus->SetParameters( 500, 10, 5, 0, 0.20 );
				gaus->FixParameter(2,5);
				ETrueBin.back()->Fit("gaus", "QN0", "", -1.0, 1.0);
				ETrueBin.back()->Fit("gaus", "QN0", "", -1.0, 1.0);
				ETrueBin.back()->Fit("gaus", "Q", "", -1.0, 1.0);

				gausMean.push_back(gaus->GetParameter(3));
				gausSigma.push_back(gaus->GetParameter(4)/
						(1.0 + min(0.0, gaus->GetParameter(3))));
			}


			// cout<<bin<<"   "<<median1(ETrueBin.back())<<endl;

			// TFile oFile( ("tmp/"+name+".root").c_str() ,"RECREATE");
			// ETrueBin.back()->Write();
			// gaus->Write();
			// oFile.Close();

			// cccc->cd();
			// ETrueBin.back()->Draw();
			// // //   gaus->Draw("same");
			// cccc->SaveAs( ("tmp/"+name+".png").c_str() );
			// cccc->SaveAs( ("tmp/"+name+".C").c_str() );

			ETrue.push_back(bin + 2.0*rebin);
			//cout<<"bin:"<<bin<<", rebin:"<<rebin<<", bin + 2*rebin:"<<(bin + 2*rebin)<<endl;
			//cout<<ETrue.back()<<", "<<gausMean.back()<<endl;
			//shubham
			//cout<<ETrue.back()<<" ";
			//  if(bin<=16)
			//  gausMean.push_back(ETrueBin.back()->GetMean());
			// else
			//   gausMean.push_back(gaus->GetParameter(1));



			average.push_back(ETrueBin.back()->GetMean());
			rms.push_back(ETrueBin.back()->GetRMS());


			//cout<<bin<<"   "<<ETrue.back()<<"   "<<ETrueBin.back()->GetMean()<<" <> "<<gausMean.back()<<"   "<<ETrueBin.back()->GetMeanError()<<"   "<<gaus->GetParError(1)<<endl;
			//cout<<bin<<"   "<<ETrue.back()<<"   "<<ETrueBin.back()->GetMean()<<" <> "<<gausMean.back()<<"   "<<ETrueBin.back()->GetMeanError()<<endl;

			if (false)
				gaus->Delete();

			(ETrueBin.back())->Write();


		}


		bin += 2*rebin;

		//Increase bin size with increasing ETrue since there are fewer high 
		//energy events than low energy ones.
		if(bin > 10) rebin = 2.0;
		if(bin > 100) rebin = 5.0; //20
		if(bin > 1000) rebin = 20.0; //50
		//delete gaus;

	}

	file1->Close();

	int temp1 = (int)ETrue.size()-2;
	float temp2[temp1];
	float temp3[temp1];
	float temp4[temp1];
	float temp5[temp1];
	float temp6[temp1];

	for(int i=2;i<temp1;++i) {
		temp2[i] = ETrue.at(i);
		temp3[i] = gausMean.at(i);
		temp4[i] = gausSigma.at(i);
		//temp5[i] = average.at(i);
		temp5[i] = 0;
		temp6[i] = rms.at(i);
	}

	response   = new TGraph(temp1, temp2, temp3);
	resolution = new TGraph(temp1, temp2, temp4);
	averages   = new TGraph(temp1, temp2, temp5);
	rmss       = new TGraph(temp1, temp2, temp6);
  TGraphErrors* Response = new TGraphErrors(temp1, temp2, temp3, temp5, temp4);

	//Set up the graphs to look how you want them to.
	response->SetMarkerStyle(22);
	response->SetMarkerSize(0.8);
	response->SetMarkerColor(1);

	Response->SetMarkerStyle(22);
	Response->SetMarkerSize(0.8);
	Response->SetMarkerColor(1);
	Response->SetLineColor(1);

	resolution->SetMarkerStyle(22);
	resolution->SetMarkerSize(0.8);
	resolution->SetMarkerColor(1);

	averages->SetMarkerStyle(22);
	averages->SetMarkerSize(0.8);
	averages->SetMarkerColor(1);

	rmss->SetMarkerStyle(22);
	rmss->SetMarkerSize(0.8);
	rmss->SetMarkerColor(1);

	line->SetLineStyle(1);
	line->SetLineWidth(2);
	line->SetLineColor(2);

	TFile *fresol = new TFile(resolution_out+".root","RECREATE");
  response->SetName("response");
  resolution->SetName("resolution");
	response->Write();
	resolution->Write();
	//fresol->Write();
	fresol->Close();

/*
	canvas = new TCanvas(("canvas "+ (string)(inHisto->GetName()) ).c_str(), ("Response and Resolution "+ (string)(inHisto->GetName())).c_str(), 1000, 500);
	canvas->Divide(2, 1);
	temp->~TCanvas();  //destroy the TCanvas 

	canvas->cd(1);
	gPad->SetGridx();
	gPad->SetGridy();
	respHisto->SetStats(0);
	respHisto->SetTitle("Response");
	respHisto->Draw();
	response->Draw("P");
	//response->Write();
	line->Draw();

	canvas->cd(2);
	gPad->SetGridx();
	gPad->SetGridy();
	resoHisto->SetStats(0);
	resoHisto->SetTitle("Resolution");
	resoHisto->Draw();
	resolution->Draw("P");
	//resolution->Write();

	respHisto->GetYaxis()->SetTitle("(E_{cor}-E_{true})/E_{true}");
	respHisto->GetXaxis()->SetTitle("E_{true} [GeV]");

	resoHisto->GetYaxis()->SetTitle("#sigma(E)/E_{true}");
	resoHisto->GetXaxis()->SetTitle("E_{true} [GeV]");
*/
	canvas = new TCanvas(("canvas "+ (string)(inHisto->GetName()) ).c_str(), ("Response"+ (string)(inHisto->GetName())).c_str(), 500, 500);
	temp->~TCanvas();  //destroy the TCanvas 

	gPad->SetGridx();
	gPad->SetGridy();
	respHisto->SetStats(0);
	respHisto->SetTitle("");
	respHisto->Draw();
	//response->Draw("P");
	Response->Draw("EP");
	//response->Write();
	line->Draw();

	respHisto->GetYaxis()->SetTitle("(E_{cor}-E_{true})/E_{true}");
	respHisto->GetXaxis()->SetTitle("E_{true} [GeV]");

	string legend;
	if(drawResoFit) {
		//MM Fit Resolution
		TF1* f=new TF1( ("ResoFit"+ (string)(inHisto->GetName())).c_str(),"sqrt([0]*[0]+[1]*[1]/x+[2]*[2]/(x*x))",30,1000);// 3.5*4


		if(resolution_out == "resolution_raw_H_barrel"){
			// h hadron barrel, raw
			f->SetParameter(0, 0.0742524);
			f->SetParameter(1, 1.04368);
			f->SetParameter(2, 3.28362);
		}

		if(resolution_out == "resolution_E_corr_H_barrel"){
			// h hadron barrel, energy corr
			f->SetParameter(0, 0.059129);
			f->SetParameter(1, 1.10921);
			f->SetParameter(2, 0.00137298);
		}

		if(resolution_out == "resolution_Eta_corr_H_barrel"){
			// h hadron barrel, eta corr
			f->SetParameter(0, 0.0609861);
			f->SetParameter(1, 1.10442);
			f->SetParameter(2, 0.000104829);
		}

		if(resolution_out == "resolution_raw_H_endcap"){
			// h hadron endcap raw
			f->SetParameter(0, 0.0821552);
			f->SetParameter(1, 0.637689);
			f->SetParameter(2, 6.5361);
		}

		if(resolution_out == "resolution_E_corr_H_endcap"){
			// h hadron endcap E correction
			f->SetParameter(0, 0.066565);
			f->SetParameter(1, 0.877389);
			f->SetParameter(2, 4.74634);
		}

		if(resolution_out == "resolution_Eta_corr_H_endcap"){
			// h hadron endcap Eta correction
			f->SetParameter(0, 0.0742353);
			f->SetParameter(1, 0.736757);
			f->SetParameter(2, 5.95198);
		}

		if(resolution_out == "resolution_raw_EH_barrel"){
			// eh hadron barrel, raw 
			f->SetParameter(0, 0.11771);
			f->SetParameter(1, 1.73285);
			f->SetParameter(2, 2.9844e-05);
		}

		if(resolution_out == "resolution_E_corr_EH_barrel"){
			// eh hadron barrel, E corr 
			f->SetParameter(0, 0.103392);
			f->SetParameter(1, 1.28855);
			f->SetParameter(2, -3.29676e-07);
		}

		if(resolution_out == "resolution_Eta_corr_EH_barrel"){
			// eh hadron barrel, Eta corr 
			f->SetParameter(0, 0.103794);
			f->SetParameter(1, 1.249);
			f->SetParameter(2, 1.52679e-11);
		}

		if(resolution_out == "resolution_raw_EH_endcap"){
			// eh hadron endcap raw
			f->SetParameter(0, -0.00816874);
			f->SetParameter(1, 1.87745);
			f->SetParameter(2, -2.43074);
		}

		if(resolution_out == "resolution_E_corr_EH_endcap"){
			// eh hadron endcap E corr
			f->SetParameter(0, 0.0222726);
			f->SetParameter(1, 1.68105);
			f->SetParameter(2, -0.00293701);
		}

		if(resolution_out == "resolution_Eta_corr_EH_endcap"){
			// eh hadron endcap Eta corr
			f->SetParameter(0, 0.0541866);
			f->SetParameter(1, 1.57918);
			f->SetParameter(2, 1.3701e-05);
		}

		resolution->Fit(("ResoFit"+ (string)(inHisto->GetName())).c_str(),"QR");
		resolution->Fit(("ResoFit"+ (string)(inHisto->GetName())).c_str(),"QR");
		resolution->Fit(("ResoFit"+ (string)(inHisto->GetName())).c_str(),"R");
		//resolution->Fit(("ResoFit"+ (string)(inHisto->GetName())).c_str(),"QR");
		//resolution->Fit(("ResoFit"+ (string)(inHisto->GetName())).c_str(),"QR");
		//resolution->Fit(("ResoFit"+ (string)(inHisto->GetName())).c_str(),"R");



		int fres0 = (int)(f->GetParameter(0)*100.);
		int fres1 = (int)(10.*(f->GetParameter(0)*100.-fres0));
		int fres2 = (int)(f->GetParameter(1)*100.);
		// char text[100];
		// sprintf(text,"#sigma/E = %i%/#sqrt{E} + %i.%i%",fres2,fres0,fres1);
		/*
			 TString text = "#sigma/E = ";
			 text+=(int)fres2;
			 text+="%/#sqrt{E} + ";
			 text+=(int)fres0;
			 text+=".";
			 text+=(int)fres1;

*/
		int noise = (int)(f->GetParameter(2)*100.);
		int noise_deci = (int)(10*(f->GetParameter(2)*100. - noise));
		int stach = (int)(f->GetParameter(1)*100);
		int stach_deci = (int)(10*(f->GetParameter(1)*100. - stach));
		int const_term = (int)(f->GetParameter(0)*100);
		int const_term_deci = (int)(10*(f->GetParameter(0)*100 - const_term));

		TString text = "#sigma/E = ";
		//text += noise;
		//text += ".";
		//text += noise_deci;
		//text += "%/E #oplus ";
		text += stach;
		text += ".";
		text += stach_deci;
		text += "%/#sqrt{E} #oplus ";
		text += const_term;
		text += ".";
		text += const_term_deci;
		text += "%";
		cout << "Resolution: " << noise << "   " << stach << "   " << const_term << endl;

		legend += text;
		TLegend *leg=new TLegend(0.30,0.75,0.85,0.85);
		leg->AddEntry((resolution),legend.c_str(),"lp");
		leg->SetTextSize(0.04);
		//leg->Draw();


	}

	if (saveCanvas) {
		TString saveName = resolution_out+".png";
    canvas->SaveAs(saveName.ReplaceAll("resolution", "response"));

    canvas = new TCanvas(("canvas "+ (string)(inHisto->GetName()) ).c_str(), ("Resolution"+ (string)(inHisto->GetName())).c_str(), 500, 500);
    temp->~TCanvas();  //destroy the TCanvas 

    gPad->SetGridx();
    gPad->SetGridy();
    resoHisto->SetStats(0);
    resoHisto->SetTitle("");
    resoHisto->Draw();
    resolution->Draw("EP");

    resoHisto->GetYaxis()->SetTitle("#sigma(E)/E_{true}");
    resoHisto->GetXaxis()->SetTitle("E_{true} [GeV]");
    TLegend *leg=new TLegend(0.30,0.75,0.85,0.85);
    leg->AddEntry((resolution),legend.c_str(),"lp");
    leg->SetTextSize(0.04);
    leg->Draw();
    canvas->SaveAs(resolution_out+".png");
		//  //string cname = ((string)(inHisto->GetName()) ) + ".png";
		//  char  cname[200];
		//  sprintf(cname,  "%s_JME_GT_sample.C",inHisto->GetName());
		//  canvas->Print(cname);
	}


}

void drawEtaDependence(TH2F* inHisto, TGraph* responseEta)
{
	if(inHisto->GetEntries() == 0) return;

	vector<TH1F*> etaBin;
	TF1* gaus; 
	TString name;
	//char num[4];

	TCanvas* canvas;
	TCanvas* temp = new TCanvas();
	TLine* line = new TLine(0, 0, 3, 0);
	//TLine* line = new TLine(-3, 0, 3, 0);

	TH2F* respHisto = new TH2F("respHisto", "", 30, 0.0, 3.00, 100, -1.0, 1.0);
	//TH2F* respHisto = new TH2F("respHisto", "", 60, -3.0, 3.00, 100, -1.0, 1.0);

	vector<double> etaAverage;
	vector<double> gausMean; 
	vector<double> gausSigma;
	vector<double> average;
	vector<double> etaRms;

	TFile* file1=new TFile("projections_eta.root","recreate");
	temp->cd();//This TCanvas is only used since when we do the fit down below 
	//it creates an unwanted TCanvas. We will get rid of it later on 
	//in the function.

	float mR=0;
	float mR2=0;
	int N=0;

	//  TCanvas* cccc=new TCanvas("bala","bala");

	for(unsigned bin = 1; bin < (unsigned)inHisto->GetNbinsX(); bin = bin + 1)
	{
		name = "histEta";
		//      sprintf(num, "%i", bin);
		TString name2 = name;
		name2 += bin;
		//Split up the TH2 into many TH1's for each eta bin.

		etaBin.push_back((TH1F*)inHisto->ProjectionY(name2,bin, bin + 1));

		name += inHisto->GetXaxis()->GetBinCenter(bin);


		if(etaBin.back()->GetEntries() > 0)
		{
			//Fit each eta bin to a gaus (iteratively done to get better fit)

			gaus =new TF1("gaus","gaus(0)",-3,3);
			//gaus->SetParameters(500.,0.,0.2);
			gaus->SetParameters(500.,etaBin.back()->GetMean(),etaBin.back()->GetRMS());

			float rrms  = etaBin.back()->GetRMS();
			float mmean = etaBin.back()->GetMean();
			//etaBin.back()->Fit("gaus", "Q", "", -1.0, 1.0);
			etaBin.back()->Fit("gaus", "Q", "", mmean-rrms, mmean+rrms);
			// gaus = etaBin.back()->GetFunction("gaus");

			int nsig = 2.0;
			if(inHisto->GetXaxis()->GetBinLowEdge(bin) > 1.5) nsig = 1;
			etaBin.back()->Fit("gaus", "Q", "",
					gaus->GetParameter(1) - nsig*gaus->
					GetParameter(2), 1.0);  
			// gaus = etaBin.back()->GetFunction("gaus");

			etaBin.back()->Fit("gaus", "Q", "",
					gaus->GetParameter(1) - nsig*gaus->
					GetParameter(2), 1.0);


			// etaBin.back()->Fit("gaus", "Q", "",
			//                    gaus->GetParameter(1) - gaus->
			//                    GetParameter(2), 1.0);  
			// // gaus = etaBin.back()->GetFunction("gaus");

			// etaBin.back()->Fit("gaus", "Q", "",
			//                    gaus->GetParameter(1) - gaus->
			//                    GetParameter(2), 1.0);
			// gaus = etaBin.back()->GetFunction("gaus");

			etaAverage.push_back(inHisto->GetXaxis()->GetBinCenter(bin));
			etaRms.push_back(0.1);

			if (useMean) 
				gausMean.push_back(etaBin.back()->GetMean());
			else 
				gausMean.push_back( gaus->GetParameter(1) );

			gausSigma.push_back(etaBin.back()->GetRMS());

			if(etaAverage.back()>1.6) {
				mR += gausMean.back();
				mR2 += gausMean.back()*gausMean.back();
				N++;
			}

			// cccc->cd();
			// etaBin.back()->Draw();
			// gaus->Draw("same");
			// cccc->SaveAs( ("tmp/Eta"+name+".png") );
			// cccc->SaveAs( ("tmp/Eta"+name+".root") );
			//cout<<gaus->GetParameter(1)<<endl;


			(etaBin.back())->Write();
		}

		//Increase bin size with increasing eta since there are fewer high 
		//energy events than low energy ones.
	}

	//  delete cccc;
	file1->Close();
	responseEta = new TGraph(etaAverage.size(), &etaAverage[0], &gausMean[0]); 
	TGraphErrors* ResponseEta = new TGraphErrors(etaAverage.size(), &etaAverage[0], &gausMean[0], 0, &gausSigma[0]); 
	//&etaRms[0], &gausSigma[0]); 

	responseEta->SetMarkerStyle(22);
	responseEta->SetMarkerSize(1);
	responseEta->SetMarkerColor(4);

	ResponseEta->SetMarkerStyle(22);
	ResponseEta->SetMarkerSize(1);
	ResponseEta->SetMarkerColor(1);
	ResponseEta->SetLineColor(1);

	if(changeRange) {
		responseEta->SetMinimum(-1.0);
		responseEta->SetMaximum(1.0);
	}

	line->SetLineStyle(1);
	line->SetLineWidth(2);
	line->SetLineColor(2);

	canvas = new TCanvas( ("canvas"+ (string)(inHisto->GetName()) ).c_str(), ("Response and Resolution "+ (string)(inHisto->GetName()) ).c_str(), 
			1000, 500);


	temp->~TCanvas();  //destroy the TCanvas 

	canvas->cd();
	canvas->SetFillColor(0);

	gPad->SetGridx();
	gPad->SetGridy();
	respHisto->SetStats(0);
	respHisto->SetTitle("");
	respHisto->Draw();
	//responseEta->Draw("P");
	ResponseEta->Draw("EP");
	line->Draw();   
	respHisto->GetXaxis()->SetRangeUser(0,3);
	//respHisto->GetXaxis()->SetRangeUser(-3,3);
	if(changeRange)  respHisto->GetYaxis()->SetRangeUser(-1.0,1.0);
	else respHisto->GetYaxis()->SetRangeUser(-0.5,0.5);
	respHisto->GetXaxis()->SetTitle("|#eta|");
	//respHisto->GetXaxis()->SetTitle("#eta");
	respHisto->GetYaxis()->SetTitle("(E_{cor}-E_{true})/E_{true}");


	// TF1*  f_eta = new TF1("etaFit", "[0]*(x - 1.5)*(x - 1.5) + [1]*(x - 1.5)*(x - 1.5)*(x - 1.5)*(x - 1.5) + [2]" , 1.5, 3.0);
	// f_eta->SetParameter(0,0.18);//,-0.16,0.0);
	// f_eta->SetParameter(1,-0.16);//,-0.16,0.0);
	// f_eta->SetParameter(2,0.0);//,-0.16,0.0);
	// responseEta->Fit("etaFit","","", 1.5, 2.85);

	//Spread
	//cout<<" Endcap spread and mean for "<<inHisto->GetName()<<endl;

	mR/=N;
	mR2/=N;
	// cout<<" mean = "<<mR<<endl;
	// cout<<" rms = "<<sqrt(mR2- pow(mR,2) )<<endl;


	char  cname[200];
	sprintf(cname, "%s_JME_GT_sample.png",inHisto->GetName());
	canvas->Print(cname);


}

void drawCompare(TGraph& response1, TGraph& response2, TGraph& resolution1, TGraph& resolution2)
{


	TCanvas* Compare = new TCanvas("Compare" ,"", 1000, 500);
	TH2F * respHisto = new TH2F("respHisto", "", 100, 0, 1000, 100, -1, 1);
	TH2F * resoHisto = new TH2F("resoHisto", "", 100, 0, 1000, 100, 0, 1);
	TLegend * legend1 = new TLegend(0.75, 0.75, 0.95, 0.9);
	TLegend * legend2 = new TLegend(0.75, 0.75, 0.95, 0.9);

	response1.SetMarkerColor(4);
	response1.SetMarkerStyle(22);
	response1.SetMarkerSize(0.8);

	resolution1.SetMarkerColor(4);
	resolution1.SetMarkerStyle(22);
	resolution1.SetMarkerSize(0.8);

	response2.SetMarkerColor(2);
	response2.SetMarkerStyle(22);
	response2.SetMarkerSize(0.8);

	resolution2.SetMarkerColor(2);
	resolution2.SetMarkerStyle(22);
	resolution2.SetMarkerSize(0.8);

	legend1->AddEntry(&response1, "Raw");
	legend1->AddEntry(&response2, "Corrected");
	legend2->AddEntry(&resolution1, "Raw");
	legend2->AddEntry(&resolution2, "Corrected");

	Compare->Divide(2,1);

	Compare->cd(1);
	gPad->SetGridx();
	gPad->SetGridy();
	respHisto->SetStats(0);
	respHisto->SetTitle("Response");
	respHisto->Draw();
	response1.Draw("P");
	response2.Draw("P");
	legend1->Draw();

	Compare->cd(2);
	gPad->SetGridx();
	gPad->SetGridy();
	resoHisto->SetStats(0);
	resoHisto->SetTitle("Resolution");
	resoHisto->Draw();
	resolution1.Draw("P");
	resolution2.Draw("P");
	legend2->Draw();

}

vector<float> assignvalues(vector<float> *pfcID_, vector<float> *Ecalenergy_, 
		vector<float> *Hcalenergy_, vector<float> *dr) {

	vector<float> energies;
	float e = 0.0 , h = 0.0;
	for(unsigned ii = 0; ii < pfcID_->size(); ii++) {
		//cout<<" pfcID_:" << pfcID_->at(ii) << endl;
		if (old_logic) {
			//if (pfcID_->at(ii) == 4 && dr->at(ii) < 0.2) e += Ecalenergy_->at(ii);
			//if (pfcID_->at(ii) == 5 && dr->at(ii) < 0.4) h += Hcalenergy_->at(ii);
			if (pfcID_->at(ii) == 4) e += Ecalenergy_->at(ii);
			if (pfcID_->at(ii) == 5) h += Hcalenergy_->at(ii);

		}
		else {
			//if (pfcID_->at(ii) == 5 && dr->at(ii) < 0.4) {
			if (pfcID_->at(ii) == 5) {
				e += Ecalenergy_->at(ii);
				h += Hcalenergy_->at(ii);
			}
		}
		}
		energies.push_back(e);
		energies.push_back(h);
		return energies;

	}


	//Takes apart a TTree from a root file and puts the wanted information into 
	//vectors. 
	void getValuesFromTree(vector<double>& ETrueEnergies, 
			vector<double>& ecalEnergies, 
			vector<double>& hcalEnergies, vector<double>& etas, 
			vector<double>& phis)
	{
		vector<float>*         true_=0;
		vector<float>*         p_=0;
		vector<float>*         eta_=0;
		vector<float>*         phi_=0;
		TBranch        *b_true; 
		TBranch        *b_p;   
		TBranch        *b_eta;    
		TBranch        *b_phi;    

		vector<float>        *pfcs_=0;
		vector<float>        *E_ecal_=0;
		vector<float>        *E_hcal_=0;
		vector<float>        *dr_=0;
		TBranch        *b_pfcs;   
		TBranch        *b_E_ecal;
		TBranch        *b_E_hcal;
		TBranch        *b_dr;

		vector<float>  *pfc_eta_=0;
		TBranch        *b_pfc_eta_=0;   
		vector<float>  *pfc_phi_=0;
		TBranch        *b_pfc_phi_=0;   

		TFile *ftemp = new TFile("SinglePion/PFHadCalibration.root");
		TTree* sTree=(TTree*)ftemp->Get("pfHadCalibNTuple/Candidates");

		sTree->SetMakeClass(1);

		sTree->SetBranchAddress("true_energy", &true_);
		sTree->SetBranchAddress("true_eta", &eta_);
		sTree->SetBranchAddress("true_phi", &phi_);
		sTree->SetBranchAddress("pfc_trackRef_p", &p_);
		sTree->SetBranchAddress("pfc_id", &pfcs_);
		sTree->SetBranchAddress("pfc_trackRef_eta", &pfc_eta_);
		sTree->SetBranchAddress("pfc_trackRef_phi", &pfc_phi_);
		sTree->SetBranchAddress("pfc_ecal", &E_ecal_);
		sTree->SetBranchAddress("pfc_hcal", &E_hcal_);

		double sigmaEcalHcal=1;
		long veto = 0 ;
		//int count = 0;
		bool flag[10] = {0,0,0,0,0,0,0,0,0,0};
		float e_true, ecal, hcal, minDr, Dr, true_index;

		cout << sTree->GetEntries() << endl;

		//for( unsigned entry = 0; entry < std::min((unsigned)500000000,(unsigned)(sTree->GetEntriesFast()) ); entry++) {
		for(int entry = 0; entry < sTree->GetEntries(); entry++) { 
			sTree->GetEntry(entry);
			//sTree->GetEntry(1266);

			if(pfcs_->size() == 0 || true_->size() == 0) continue;

			for(int i = 0; i < (int)pfcs_->size(); ++i){
				minDr = 99.;  Dr = 999.; true_index = -1;
				for(int j = 0; j < (int)true_->size(); ++j){
					Dr = (pfc_eta_->at(i)-eta_->at(j))*(pfc_eta_->at(i)-eta_->at(j)) + (pfc_phi_->at(i)-phi_->at(j))*(pfc_phi_->at(i)-phi_->at(j));
					if((minDr > Dr) && ((fabs(eta_->at(j)) <= 2.4 && p_->at(i) > 0) || fabs(eta_->at(j)) > 2.4)) { minDr = Dr; true_index = j; }
				}

				if(true_index >= 0) {
					if(Dr < 1.){
						e_true = true_->at(true_index);
            if(e_true > 500) continue;
						ecal = E_ecal_->at(i);
						hcal = E_hcal_->at(i);
						ETrueEnergies.push_back(e_true);
						etas.push_back(eta_->at(true_index));
						phis.push_back(phi_->at(true_index));
						ecalEnergies.push_back(ecal);
						hcalEnergies.push_back(hcal);
						if(fabs(eta_->at(true_index))<1.5) sigmaEcalHcal = sqrt(0.08*0.08 + 1.04*1.04*(std::max((double)(ecal + hcal), 1.0)));
						else																  	sigmaEcalHcal = sqrt(0.04*0.04 + 1.80*1.80*(std::max((double)(ecal + hcal), 1.0)));
						sigmas.push_back(sigmaEcalHcal);

					}
				}
			}

			/*
				 if(sTree->GetBranchStatus("true"))
				 ETrueEnergies.push_back(true_);
				 else
				 ETrueEnergies.push_back(p_);
			//if(pfcs_->size() != 0) {
			if(pfcs_->size() == 0) {
			//vector<float> tmp = assignvalues(pfcs_, E_ecal_, E_hcal_, dr_);
			vector<float> tmp = assignvalues(pfcs_, E_ecal_, E_hcal_, 0);
			ecalEnergies.push_back(tmp.at(0));
			hcalEnergies.push_back(tmp.at(1));
			}
			else {
			ecalEnergies.push_back(ecal_);
			hcalEnergies.push_back(hcal_);
			}
			etas.push_back(eta_);
			phis.push_back(phi_);


			if(fabs(eta_)<1.5) 
			sigmaEcalHcal = sqrt(0.08*0.08 + 1.04*1.04*(std::max((double)(ecal_ + hcal_), 1.0)));
			else
			sigmaEcalHcal = sqrt(0.04*0.04 + 1.80*1.80*(std::max((double)(ecal_ + hcal_), 1.0)));

			sigmas.push_back(sigmaEcalHcal);


			if(fabs(eta_) > 2.5 && ecalEnergies.back() != 0 && false) {
			cout<<"***************"<<endl;
			cout<<fabs(eta_)<<" "<<ecalEnergies.back()<<endl;

			}
			//cout<< "**************" << endl;

			// cout<<" pfcID_.size(): " << pfcID_->size() << " Eecal->size(): " << E_ecal_->size()
			// 	   << " Ehcal->size(): " << E_hcal_->size() << " dr: " << dr_->size() << endl;
			// for(int ii = 0; ii < pfcID_->size() && entry < 20; ii++) {
			// 	 cout<<" pfcID_:" << pfcID_->at(ii) << endl;
			// }
			*/


			unsigned N = sTree->GetEntriesFast();
			int frac = ((double)entry/N)*100;
			switch(frac) {
				case 10 : if (!flag[0]) { cout<<"10%"<<endl; flag[0] = 1; } break;
				case 20 : if (!flag[1]) { cout<<"20%"<<endl; flag[1] = 1; } break;
				case 30 : if (!flag[2]) { cout<<"30%"<<endl; flag[2] = 1; } break;
				case 40 : if (!flag[3]) { cout<<"40%"<<endl; flag[3] = 1; } break;
				case 50 : if (!flag[4]) { cout<<"50%"<<endl; flag[4] = 1; } break;
				case 60 : if (!flag[5]) { cout<<"60%"<<endl; flag[5] = 1; } break;
				case 70 : if (!flag[6]) { cout<<"70%"<<endl; flag[6] = 1; } break;
				case 80 : if (!flag[7]) { cout<<"80%"<<endl; flag[7] = 1; } break;
				case 90 : if (!flag[8]) { cout<<"90%"<<endl; flag[8] = 1; } break;
				case 99 : if (!flag[9]) { cout<<"100%"<<endl; flag[9] = 1; } break;
				default : break;

			}

		}

		cout<<" Entries "<<ecalEnergies.size()<<endl;
		cout<<" Vetoed events "<<veto<<endl;
		//exit(0);

		}



		/// Bin Manager =========================================
		vector<double> BinsETrue;
		vector<double> BinsETrueEta;

		unsigned int GetETrueBin(double etrue) {

			bool find=false;

			int bm=0;
			int bM=BinsETrue.size()-1;
			if(etrue< BinsETrue[ bm ]) return -1;
			if(etrue> BinsETrue[ bM ]) return -1;
			int n=0;
			while(!find) {

				if(etrue <= BinsETrue[ bm+(bM-bm)/2 ] ) {
					bM = bm+(bM-bm)/2;
				}
				else {
					bm = bm+(bM-bm)/2;
				}
				if( fabs(bm-bM)==1 )  {
					return bm;
				}

				if(n>(int)BinsETrue.size()) return -1;
				n++;
			}
			return -1;
		}


		unsigned int GetETrueBinEta(double etrue) {

			bool find=false;

			int bm=0;
			int bM=BinsETrueEta.size()-1;

			if(etrue< BinsETrueEta[ bm ]) return -1;
			if(etrue> BinsETrueEta[ bM ]) return -1;
			int n=0;
			while(!find) {

				if(etrue <= BinsETrueEta[ bm+(bM-bm)/2 ] ) {
					bM = bm+(bM-bm)/2;
				}
				else {
					bm = bm+(bM-bm)/2;
				}
				if( fabs(bm-bM)==1 )  {
					return bm;
				}

				if(n>(int)BinsETrueEta.size()) return -1;
				n++;
			}
			return -1;
		}

		///======================================================


		///////////////////////////////////////////////////////////////////////////////
		//All the needed variables for the main (calibChris) function.
		///////////////////////////////////////////////////////////////////////////////

		TFile* inputFile;
		TTree* sTree;

		vector<double> ETrueEnergies;  //The values that are taken from the root file
		vector<double> ecalEnergies;
		vector<double> hcalEnergies;
		vector<double> etas;
		vector<double> phis;


		vector<ABC*> barrelABCEcalHcal; //Vectors of the ABC objects
		vector<ABC*> barrelABCEcal;     //which hold all the calibration 
		vector<ABC*> barrelABCHcal;     //constants for an individual bin.
		vector<ABC*> endcapABCEcalHcal;
		vector<ABC*> endcapABCEcal;
		vector<ABC*> endcapABCHcal;

		vector<AlphaBeta*> barrelAlphaBetaEcalHcal; //Vectors of the AlphaBeta objects which 
		vector<AlphaBeta*> barrelAlphaBetaHcal;
		vector<AlphaBeta*> endcapAlphaBetaEcalHcal; //hold all the calibration constants for 
		vector<AlphaBeta*> endcapAlphaBetaHcal; //an individual bin.

		TF1* functionBarrelEcalHcalA;     //Functions that the calibration equations
		TF1* functionBarrelEcalHcalB;     //are fit to
		TF1* functionBarrelEcalHcalC;  
		TF1* functionEndcapEcalHcalA;
		TF1* functionEndcapEcalHcalB;
		TF1* functionEndcapEcalHcalC;  

		TF1* functionBarrelHcalA;
		TF1* functionBarrelHcalB;
		TF1* functionBarrelHcalC;  
		TF1* functionEndcapHcalA;
		TF1* functionEndcapHcalB;
		TF1* functionEndcapHcalC;  

		TF1* functionBarrelAlphaEcalHcal;
		TF1* functionBarrelBetaEcalHcal;
		TF1* functionBarrelAlphaHcal;
		TF1* functionBarrelBetaHcal;

		TF1* functionEndcapAlphaEcalHcal;
		TF1* functionEndcapBetaEcalHcal;
		TF1* functionEndcapAlphaHcal;
		TF1* functionEndcapBetaHcal;
		TF1* functionEndcapGammaHcal;

		//Calibration objects which hold the all the calibration costants as functions
		//of ETrue. 
		Calibration* barrelWithEcalHcalCalib = new Calibration(sampleRangeHigh, true);
		Calibration* barrelWithEcalCalib = new Calibration(sampleRangeHigh, true);
		Calibration* barrelWithHcalCalib = new Calibration(sampleRangeHigh, true);
		Calibration* endcapWithEcalHcalCalib = new Calibration(sampleRangeHigh, false);
		Calibration* endcapWithEcalCalib = new Calibration(sampleRangeHigh, false);
		Calibration* endcapWithHcalCalib = new Calibration(sampleRangeHigh, false);

		//Temporary varibles that will be used in for loops just to cut down on the 
		//length of the lines of code.
		double etrue;
		double eta;
		double bpar;
		double cpar;
		double etrueMax;
		double barrelEcalHcalB;
		double barrelEcalHcalC;
		double barrelHcalC;
		double barrelAlpha;
		double barrelBeta;
		double endcapEcalHcalB;
		double endcapEcalHcalC;
		double endcapHcalC;
		double endcapAlpha;
		double endcapBeta;
		double correctedE;
		double correctedEta;

		const char* functionEndcapEcalHcalB_e;
		const char* functionEndcapEcalHcalC_e;
		const char* functionEndcapHcalC_e;
		const char* functionEndcapAlphaEH_e;
		const char* functionEndcapBetaEH_e;
		const char* functionEndcapAlphaH_e;
		const char* functionEndcapBetaH_e;
		const char* functionBarrelEcalHcalB_e;
		const char* functionBarrelEcalHcalC_e;
		const char* functionBarrelHcalC_e;
		const char* functionBarrelAlphaEH_e;
		const char* functionBarrelBetaEH_e;
		const char* functionBarrelAlphaH_e;
		const char* functionBarrelBetaH_e;

		//All the differenct types of TH2's that will be filled in order to make 
		//resolution and response plots

		TH2F* h_trueE_vs_mod_eta_response = new TH2F("h_trueE_vs_mod_eta_response","True Energy vs eta distribution",6,0.0,3.0,33,2,sampleRangeHigh);
		TH2F* h_trueE_vs_mod_eta_response_normalized = new TH2F("h_trueE_vs_mod_eta_response_normalized","True Energy vs eta distribution with response on z axis (EH-hadrons)",6,0.0,3.0,33,2,sampleRangeHigh);

		TH2F * h_response_vs_phi_barrel_EH = new TH2F("h_response_vs_phi_barrel_EH", "EH hadrons Response vs #phi in Barrel", 70, -3.5, 3.5, 30, -1.5, 1.5); //shubham
		TH2F * h_response_vs_phi_EndCap_EH_posZ = new TH2F("h_response_vs_phi_EndCap_EH_posZ", "EH hadrons Response vs #phi for +z in EndCap", 70, -3.5, 3.5, 30, -1.5, 1.5); //shubham
		TH2F * h_response_vs_phi_EndCap_EH_negZ = new TH2F("h_response_vs_phi_EndCap_EH_negZ", "EH hadrons Response vs #phi for -z in EndCap", 70, -3.5, 3.5, 30, -1.5, 1.5); //shubham

		TH2F * h_response_vs_phi_barrel_H = new TH2F("h_response_vs_phi_barrel_H", "H hadrons Response vs #phi in Barrel", 70, -3.5, 3.5, 30, -1.5, 1.5); //shubham
		TH2F * h_response_vs_phi_EndCap_H_posZ = new TH2F("h_response_vs_phi_EndCap_H_posZ", "H hadrons Response vs #phi for +z in EndCap", 70, -3.5, 3.5, 30, -1.5, 1.5); //shubham
		TH2F * h_response_vs_phi_EndCap_H_negZ = new TH2F("h_response_vs_phi_EndCap_H_negZ", "H hadrons Response vs #phi for -z in EndCap", 70, -3.5, 3.5, 30, -1.5, 1.5); //shubham


		TH2F* Raw = new TH2F("Raw","", 1000, 0, 1000, 150, -1.5, 1.5);
		TH2F* corrEta = new TH2F("corrEta", "", 1000, 0, 1000, 150, -1.5, 1.5);

		TH2F* rawBarrel = new TH2F("rawBarrel","", 1000, 0, 1000, 150, -1.5, 1.5);
		TH2F* corrBarrel = new TH2F("corrBarrel", "", 1000, 0, 1000, 150, -1.5, 1.5);
		TH2F* corrEtaBarrel = new TH2F("corrEtaBarrel", "", 1000, 0, 1000, 150, -1.5, 
				1.5);
		TH2F* rawBarrelEcalHcal = new TH2F("rawBarrelEcalHcal","", 1000, 0, 1000, 150, 
				-1.5, 1.5);
		TH2F* corrBarrelEcalHcal = new TH2F("corrBarrelEcalHcal", "", 1000, 0, 1000, 
				150, -1.5, 1.5);
		TH2F* corrEtaBarrelEcalHcal = new TH2F("corrEtaBarrelEcalHcal", "", 1000, 0, 
				1000, 150, -1.5, 1.5);
		TH2F* rawBarrelHcal = new TH2F("rawBarrelHcal","", 1000, 0, 1000, 150, -1.5, 1.5 );
		//1000, 0.0, 5.0);
		TH2F* corrBarrelHcal = new TH2F("corrBarrelHcal", "", 1000, 0, 1000, 150, -1.5,
				1.5);
		TH2F* corrEtaBarrelHcal = new TH2F("corrEtaBarrelHcal", "", 1000, 0, 1000, 150,
				-1.5, 1.5);

		TH2F* rawEndcap = new TH2F("rawEndcap","", 1000, 0, 1000, 150, -1.5, 1.5);
		TH2F* corrEndcap = new TH2F("corrEndcap", "", 1000, 0, 1000, 150, -1.5, 1.5);
		TH2F* corrEtaEndcap = new TH2F("corrEtaEndcap", "", 1000, 0, 1000, 150, -1.5, 1.5);
		TH2F* rawEndcapEcalHcal = new TH2F("rawEndcapEcalHcal","", 1000, 0, 1000, 150, -1.5, 1.5);
		TH2F* corrEndcapEcalHcal = new TH2F("corrEndcapEcalHcal", "", 1000, 0, 1000, 150, -1.5, 1.5);
		TH2F* corrEtaEndcapEcalHcal = new TH2F("corrEtaEndcapEcalHcal", "", 1000, 0, 1000, 150, -1.5, 1.5);
		TH2F* rawEndcapHcal = new TH2F("rawEndcapHcal","", 1000, 0, 1000, 150, -1.5, 1.5);
		TH2F* corrEndcapHcal = new TH2F("corrEndcapHcal", "", 1000, 0, 1000, 150, -1.5,	1.5);
		TH2F* corrEtaEndcapHcal = new TH2F("corrEtaEndcapHcal", "", 1000, 0, 1000, 150,	-1.5, 1.5);

		TH2F * rawEtaDependenceEH = new TH2F("rawEtaDependenceEH","Response vs. Eta", 60, 0.0, 3.0, 150, -1.0,1.0 );
		TH2F * corrEtaDependenceEH = new TH2F("corrEtaDependenceEH","Response vs. Eta", 60, 0.0, 3.0, 150, -1.0,1.0 );
		TH2F * hcorrEtaDependenceEH = new TH2F("hcorrEtaDependenceEH","Response vs. Eta", 60, 0., 3.0, 150, -1.0,1.0 );
		TH2F * hhcorrEtaDependenceEH = new TH2F("hhcorrEtaDependenceEH","Response vs. Eta", 120, -3.0, 3.0, 150, -1.0,1.0 );

		TH2F * rawEtaDependenceH = new TH2F("rawEtaDependenceH","Response vs. Eta", 60, 0.0, 3.0, 120, -1.0,1.0 );
		TH2F * corrEtaDependenceH = new TH2F("corrEtaDependenceH","Response vs. Eta", 60, 0.0, 3.0, 120, -1.0,1.0 );
		TH2F * hcorrEtaDependenceH = new TH2F("hcorrEtaDependenceH","Response vs. Eta", 60, 0., 3.0, 120, -1.0,1.0 );
		TH2F * hhcorrEtaDependenceH = new TH2F("hhcorrEtaDependenceH","Response vs. Eta", 120, -3., 3.0, 150, -1.0,1.0 );

		TH1F * trueTempHisto = new TH1F("trueTempHisto", "true", sampleRangeHigh, 0, sampleRangeHigh);
		TH1F * ecalTempHisto = new TH1F("ecalTempHisto", "ecal", sampleRangeHigh, 0, sampleRangeHigh);

		TProfile2D* corrEtaDependenceProfEH=new TProfile2D("EH","", 40, 0,100, 75, 0, 3.0);
		TProfile2D* corrEtaDependenceProfH=new TProfile2D("H","", 40, 0,100, 75, 0, 3.0);

		TH2F* bcplot= new TH2F("bcplot","bcplot",1000,-1.,1.,1000,-1.,1.);

		//Temporary TGraphs to passed drawGausFit
		TGraph* response;
		TGraph* resolution;
		/////
		TGraph* responseRaw;
		TGraph* resolutionRaw;

		TGraph* responseRawH;
		TGraph* resolutionRawH;

		TGraph* responseRawEH;
		TGraph* resolutionRawEH;
		/////
		TGraph* responseCorBar;
		TGraph* resolutionCorBar;
		/////
		TGraph* responseCorBarH;
		TGraph* resolutionCorBarH;

		TGraph* responseCorEtaBarH;
		TGraph* resolutionCorEtaBarH;
		/////
		TGraph* responseCorBarEH;
		TGraph* resolutionCorBarEH;

		TGraph* responseCorEtaBarEH;
		TGraph* resolutionCorEtaBarEH;
		/////
		TGraph* responseRawEndH;
		TGraph* resolutionRawEndH;

		TGraph* responseRawEndEH;
		TGraph* resolutionRawEndEH;
		/////
		TGraph* responseCorEnd;
		TGraph* resolutionCorEnd;
		/////
		TGraph* responseCorEndH;
		TGraph* resolutionCorEndH;

		TGraph* responseCorEtaEndH;
		TGraph* resolutionCorEtaEndH;
		/////
		TGraph* responseCorEndEH;
		TGraph* resolutionCorEndEH;

		TGraph* responseCorEtaEndEH;
		TGraph* resolutionCorEtaEndEH;
		/////

		TGraph* responseEta;
		TGraph* resolutionEta;

		TGraph* responseEtaEtaEH;
		TGraph* responseEtaHCorrEtaEH;

		TGraph* responseEtaEtaH;
		TGraph* responseEtaHCorrEtaH;

		///////////////////////////////////////////////////////////////////////////////
		//This is the main of the macro. Everything that you want output must be added 
		//in here. I have it so that all the variables that I use were defined above 
		//since it looks neater.
		///////////////////////////////////////////////////////////////////////////////
		void calibChris() 
		{
		double ecal;
		double hcal;
			gROOT->Reset();
			gStyle->SetCanvasColor(0);

			InitBarrelAlpha();
			LoadOldThresholds();
			//LoadNewThresholds();

			gStyle->SetOptFit(0);

			//Open the file, get the tree and fill of the vectors of values you need.
			//inputFile = TFile::Open("IsolatedChargedHadronsFromQCD.root");
			//inputFile = TFile::Open("pfcalibTestTag_all.root");
			// inputFile = TFile::Open("IsolatedChargedHadronsFromMinBias.root");
			// sTree = (TTree*)inputFile->Get("s;1");

			//TChain* chain= new TChain("s");




			/// HCAL issue SAMPLE - MC-v2
			//chain->Add("./input_sample/PGun_930pre1_JetMET_HCALScaleStudies_2_500.root");


			///JME_checks sample
			//chain->Add("/d0/scratch/cghuh3811/PFHadCalibration/CMSSW_10_4_0_pre4/src/Offline/SinglePion_PT0to200/PFHadCalibration.root");

			//sTree = (TTree*)chain;
			//TFile *f1 = new TFile("SinglePion_PT0to200/PFHadCalibration.root");
			//sTree=(TTree*)f1->Get("s");


			cout<<"Reading input tree..."<<endl;
			//getValuesFromTree(sTree, ETrueEnergies, ecalEnergies, 
			getValuesFromTree(ETrueEnergies, ecalEnergies, 
					hcalEnergies, etas, phis);




			if (strcmp(_region_, "barrel") == 0) {
				_etaMin_ = 0.0;
				_etaMax_ = 1.5;
			}
			else if (strcmp(_region_, "EC_within_tracker") == 0 ) {
				_etaMin_ = 1.5;
				_etaMax_ = 2.5;
			}

			else if (strcmp(_region_, "EC_outside_tracker") == 0 ) {
				_etaMin_ = 2.5;
				//_etaMax_ = 3.0;
				_etaMax_ = 2.75;
			}

			else if (strcmp(_region_,  "Full") == 0 ) {
				_etaMin_ = 1.5;
				_etaMax_ = 2.75;
				//_etaMax_ = 2.4;
			}

			// cout<< " _region_: " << _region_<< " , (_region_ == EC_outside_tracker): " 
			//     << (strcmp(_region_ , "EC_outside_tracker") == 0) << " _etaMax_: " 
			//     << _etaMax_ << " ,_etaMin:_ " << _etaMin_ << endl;


			//Create all the ABC objects you need with increasing bin size
			//since there are fewer events at higher energies. 
			cout<<"Creating abc and alphabeta objects..."<<endl;

			BinsETrue.clear();
			BinsETrueEta.clear();

			for(double bin = 0.0; bin < 10.0; bin = bin + lBs)
			{
				barrelABCEcalHcal.push_back(new ABC(bin, bin + lBs, true));
				barrelABCEcal.push_back(new ABC(bin, bin + lBs, true));
				barrelABCHcal.push_back(new ABC(bin, bin + lBs, true));
				endcapABCEcalHcal.push_back(new ABC(bin, bin + lBs, false));
				endcapABCEcal.push_back(new ABC(bin, bin + lBs,false));
				endcapABCHcal.push_back(new ABC(bin, bin + lBs, false));
				BinsETrue.push_back(bin);
			}



			for(double bin = 10.0; bin < 100.0 ; bin = bin + mBs) //2
			{
				barrelABCEcalHcal.push_back(new ABC(bin, bin + mBs, true));
				barrelABCEcal.push_back(new ABC(bin, bin + mBs, true));
				barrelABCHcal.push_back(new ABC(bin, bin + mBs, true));
				endcapABCEcalHcal.push_back(new ABC(bin, bin + mBs, false));
				endcapABCEcal.push_back(new ABC(bin, bin + mBs,false));
				endcapABCHcal.push_back(new ABC(bin, bin + mBs, false));
				BinsETrue.push_back(bin);
			}


			for(double bin = 100.0; bin < 1000.0 ; bin = bin + hBs) //10
			{
				barrelABCEcalHcal.push_back(new ABC(bin, bin + hBs, true));
				barrelABCEcal.push_back(new ABC(bin, bin + hBs, true));
				barrelABCHcal.push_back(new ABC(bin, bin + hBs, true));
				endcapABCEcalHcal.push_back(new ABC(bin, bin + hBs, false));
				endcapABCEcal.push_back(new ABC(bin, bin + hBs,false));
				endcapABCHcal.push_back(new ABC(bin, bin + hBs, false));  
				BinsETrue.push_back(bin);
			}
			BinsETrue.push_back( BinsETrue.back() + hBs );



			// cout<<"barrelABCEcalHcal size: "<<barrelABCEcalHcal.size()<<endl;
			// cout<<"barrelABCEcal size: "<<barrelABCEcal.size()<<endl;
			// cout<<"barrelABCHcal size: "<<barrelABCHcal.size()<<endl;
			/*for(int i = 0; i < barrelABCEcalHcal.size(); i++) {
				if((barrelABCEcalHcal.at(i)->getSize()) != 0 )
				cout<<"EcalHcal: found one!! at "<<i<<endl;
				if((barrelABCEcal.at(i)->getSize()) != 0 )
				cout<<"Ecal: found one!! at "<<i<<endl;
				if((barrelABCHcal.at(i)->getSize()) != 0 )
				cout<<"Hcal: found one!! at "<<i<<endl;

				}*/
			//cout<<"(barrelABCEcalHcal.at(300)->getBinLowEdge()) : "<<(barrelABCEcalHcal.at(300)->getBinLowEdge())<<endl;
			//cout<<"(barrelABCEcalHcal.at(300)->getBinHighEdge()) : "<<(barrelABCEcalHcal.at(300)->getBinHighEdge())<<endl;
			//cout<<"(barrelABCEcalHcal.at(0)->getETrue(0)) : "<<(barrelABCEcalHcal.at(0)->getETrue(0))<<endl;





			for(double bin = 0.0; bin < 10.0; bin = bin + lBs*RBE)
			{
				barrelAlphaBetaEcalHcal.push_back(new AlphaBeta(bin, bin + lBs*RBE, true));
				barrelAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + lBs*RBE, true));
				endcapAlphaBetaEcalHcal.push_back(new AlphaBeta(bin, bin + lBs*RBE, false));
				endcapAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + lBs*RBE, false));
				BinsETrueEta.push_back(bin);
				// barrelAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + lBs, true));
				// endcapAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + lBs, false));

			}
			for(double bin = 10.0; bin < 100.0 ; bin = bin + mBs*RBE)
			{
				barrelAlphaBetaEcalHcal.push_back(new AlphaBeta(bin, bin + mBs*RBE, true));
				barrelAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + mBs*RBE, true));
				endcapAlphaBetaEcalHcal.push_back(new AlphaBeta(bin, bin + mBs*RBE, false));
				endcapAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + mBs*RBE, false));
				BinsETrueEta.push_back(bin);
				//   barrelAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + mBs, true));
				//   endcapAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + mBs, false));
			}

			for(double bin = 100.0; bin < 1000.0 ; bin = bin + hBs*RBE)
			{
				barrelAlphaBetaEcalHcal.push_back(new AlphaBeta(bin, bin + hBs*RBE, true));
				barrelAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + hBs*RBE, true));
				endcapAlphaBetaEcalHcal.push_back(new AlphaBeta(bin, bin + hBs*RBE, false));
				endcapAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + mBs*RBE, false));
				BinsETrueEta.push_back(bin);
				// barrelAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + hBs, true));
				// endcapAlphaBetaHcal.push_back(new AlphaBeta(bin, bin + hBs, false));
			}
			BinsETrueEta.push_back( BinsETrueEta.back() + hBs*RBE );

			//Fill all the ABC Objects with their respective events. They are all 
			//divided up into the six possible case ( (endcap or barrel)x(ecalhcal or 
			//ecal or hcal))


			TH1F* EcalSpectrum=new TH1F("EcalSpectrum","EcalSpectrum",1000,0,100);

			cout<<"Filling abc objects..."<<endl;
			for( unsigned bin = 0; bin < barrelABCEcal.size(); ++bin)
			{
				barrelABCEcalHcal[bin]->computeA(aEH);
				barrelABCEcal[bin]->computeA(aE);
				barrelABCHcal[bin]->computeA(aH);

				endcapABCEcalHcal[bin]->computeA(aEHe);
				endcapABCEcal[bin]->computeA(aEe);
				endcapABCHcal[bin]->computeA(aHe);
			}


			// cout<<"ETrueEnergies size: "<<ETrueEnergies.size()<<endl;
			// //cout<<"GetETrueBinEta(100): "<<GetETrueBinEta(99.9858)<<endl;
			// cout<<"GetETrueBinEta(100): "<<GetETrueBinEta(100)<<endl;

			//Filling ==============================
			{

				unsigned bin = 0;
				for(unsigned entry = 0; entry < ETrueEnergies.size(); entry++)
				{
					etrue = ETrueEnergies[entry];
					ecal = ecalEnergies[entry];
					hcal = hcalEnergies[entry];
					eta = etas[entry];

					if(hcal == 0.0) continue;
					if( etrue <1 ) continue;
					if( etrue >sampleRangeHigh ) continue;
					// if( etrue <10 ) continue;
					// if( etrue >12 ) continue;

					bin = GetETrueBin( etrue );

					if( ecal > 0.0 && hcal > 0.0)
					{
						barrelABCEcalHcal[bin]->addEntry(etrue, ecal, hcal, eta);
						endcapABCEcalHcal[bin]->addEntry(etrue, ecal, hcal, eta);

						if(eta<1.3)
							EcalSpectrum->Fill(ecal);

					}
					else if(ecal > 0.0)
					{
						barrelABCEcal[bin]->addEntry(etrue, ecal, hcal ,eta);
						endcapABCEcal[bin]->addEntry(etrue, ecal, hcal ,eta);
					}
					else if(hcal > 0.0)
					{
						barrelABCHcal[bin]->addEntry(etrue, ecal, hcal, eta);
						endcapABCHcal[bin]->addEntry(etrue, ecal, hcal, eta);
					}

					bin = GetETrueBinEta( etrue );

					if(bin < barrelAlphaBetaEcalHcal.size())
					{


						if( ecal > 0.0 && hcal >= 0.0 )
						{
							endcapAlphaBetaEcalHcal[bin]->addEntry(etrue, ecal, hcal, eta);
							barrelAlphaBetaEcalHcal[bin]->addEntry(etrue, ecal, hcal, eta);
						}
						else {
							endcapAlphaBetaHcal[bin]->addEntry(etrue, ecal, hcal, eta);
							barrelAlphaBetaHcal[bin]->addEntry(etrue, ecal, hcal, eta);
						}
					}
				}
			}


			//   cout<<"#####################################################################"<<endl;
			//for(unsigned bin = 2; bin < barrelABCEcalHcal.size() - 1; ++bin) {
			// cout<<"barrelABCEcalHcal["<<bin<<"]->isEmptyInFitRange(): "<<barrelABCEcalHcal[bin]->isEmptyInFitRange()<<endl;
			//}
			//cout<<"#####################################################################"<<endl;

			//Filling ==============================  
			/*
				 TFile* file=new TFile("output.root","recreate");
				 EcalSpectrum->Write();
				 file->Close();
				 */

			//Compute the calibration constants along with their uncertainties for each
			//ETrue bin, then add their values to a Calibration object.
			cout<<"Computing a, b, c coefficients..."<<endl;

			for(unsigned bin = 2; bin < barrelABCEcalHcal.size() - 1; ++bin)
			{

				if(!barrelABCEcalHcal[bin]->isEmptyInFitRange())
				{ 
					barrelABCEcalHcal[bin]->computeETrueAverage();
					barrelABCEcalHcal[bin]->computeETrueRMS();
					barrelABCEcalHcal[bin]->computeA(aEH);
					barrelABCEcalHcal[bin]->computeBC();
					//exit(0);
				}

				if(!barrelABCEcal[bin]->isEmptyInFitRange())
				{ 
					barrelABCEcal[bin]->computeETrueAverage();
					barrelABCEcal[bin]->computeETrueRMS();
					barrelABCEcal[bin]->computeA(aEH);
					barrelABCEcal[bin]->computeB();
				}
				if(!barrelABCHcal[bin]->isEmptyInFitRange())
				{ 
					barrelABCHcal[bin]->computeETrueAverage();
					barrelABCHcal[bin]->computeETrueRMS();
					barrelABCHcal[bin]->computeA(aH);
					barrelABCHcal[bin]->computeC();
				}
				if(!endcapABCEcalHcal[bin]->isEmptyInFitRange())
				{
					endcapABCEcalHcal[bin]->computeETrueAverage();
					endcapABCEcalHcal[bin]->computeETrueRMS();
					endcapABCEcalHcal[bin]->computeA(aEHe);
					endcapABCEcalHcal[bin]->computeBC();
				}
				if(!endcapABCEcal[bin]->isEmptyInFitRange())
				{
					endcapABCEcal[bin]->computeETrueAverage();
					endcapABCEcal[bin]->computeETrueRMS();
					endcapABCEcal[bin]->computeA(aEe);
					endcapABCEcal[bin]->computeB();
				}
				if(!endcapABCHcal[bin]->isEmptyInFitRange())
				{
					endcapABCHcal[bin]->computeETrueAverage();
					endcapABCHcal[bin]->computeETrueRMS();
					endcapABCHcal[bin]->computeA(aHe);
					endcapABCHcal[bin]->computeC();
				}


				if(!barrelABCEcalHcal[bin]->isEmpty() && 
						barrelABCEcalHcal[bin]->getBinHighEdge() >
						barrelWithEcalHcalCalib->getETrueMax())
				{
					barrelWithEcalHcalCalib->setETrueMax(
							barrelABCEcalHcal[bin]->getBinHighEdge());
				}
				if(!barrelABCEcal[bin]->isEmpty() && 
						barrelABCEcal[bin]->getBinHighEdge() >
						barrelWithEcalCalib->getETrueMax())
				{
					barrelWithEcalCalib->setETrueMax(
							barrelABCEcal[bin]->getBinHighEdge());
				}
				if(!barrelABCHcal[bin]->isEmpty() && 
						barrelABCHcal[bin]->getBinHighEdge() >
						barrelWithHcalCalib->getETrueMax())
				{
					barrelWithHcalCalib->setETrueMax(
							barrelABCHcal[bin]->getBinHighEdge());
				}
				if(!endcapABCEcalHcal[bin]->isEmpty() && 
						endcapABCEcalHcal[bin]->getBinHighEdge() >
						endcapWithEcalHcalCalib->getETrueMax())
				{
					endcapWithEcalHcalCalib->setETrueMax(
							endcapABCEcalHcal[bin]->getBinHighEdge());
				}
				if(!endcapABCEcal[bin]->isEmpty() && 
						endcapABCEcal[bin]->getBinHighEdge() >
						endcapWithEcalCalib->getETrueMax())
				{
					endcapWithEcalCalib->setETrueMax(
							endcapABCEcal[bin]->getBinHighEdge());
				}
				if(!endcapABCHcal[bin]->isEmpty() && 
						endcapABCHcal[bin]->getBinHighEdge() >
						endcapWithHcalCalib->getETrueMax())
				{
					endcapWithHcalCalib->setETrueMax(
							endcapABCHcal[bin]->getBinHighEdge());
				}


				barrelWithEcalHcalCalib->addGraphPoints(barrelABCEcalHcal[bin]); 
				barrelWithEcalCalib->addGraphPoints(barrelABCEcal[bin]); 
				barrelWithHcalCalib->addGraphPoints(barrelABCHcal[bin]); 
				endcapWithEcalHcalCalib->addGraphPoints(endcapABCEcalHcal[bin]); 
				endcapWithEcalCalib->addGraphPoints(endcapABCEcal[bin]); 
				endcapWithHcalCalib->addGraphPoints(endcapABCHcal[bin]);                 


			}

			cout<<"Fitting a, b, c coefficients..."<<endl;
			//Initialize all the ABC graphs in the calibration objects.
			barrelWithEcalHcalCalib->initializeGraphs("abc");

			barrelWithEcalCalib->initializeGraphs("abc");

			barrelWithHcalCalib->initializeGraphs("abc");   

			endcapWithEcalHcalCalib->initializeGraphs("abc");

			endcapWithEcalCalib->initializeGraphs("abc");

			endcapWithHcalCalib->initializeGraphs("abc");   


			//Define the functions that you will fit your ABC calibration constants to.
			functionBarrelEcalHcalA = new TF1("functionBarrelEcalHcalA","[0]", 0, 1000);
			// functionBarrelEcalHcalB = new TF1("functionBarrelEcalHcalB","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])", 0, 1000);
			//functionBarrelEcalHcalB = new TF1("functionBarrelEcalHcalB","[0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5]))))", 0, 1000);
			//functionBarrelEcalHcalC = new TF1("functionBarrelEcalHcalC","[0]+(([1]+([2]/sqrt(x)))*exp(-(x^[4]/[3])))",0,1000); //[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])", 0, 1000);
			//functionBarrelEcalHcalC = new TF1("functionBarrelEcalHcalC","([0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5])))))",0,1000);

			functionEndcapEcalHcalA = new TF1("functionEndcapEcalHcalA","[0]", 0, 1000);
			//functionEndcapEcalHcalB = new TF1("functionEndcapEcalHcalB","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])", 0, 1000);
			//functionEndcapEcalHcalB = new TF1("functionEndcapEcalHcalB","[0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5]))))", 0, 1000);
			functionBarrelEcalHcalB = new TF1("functionBarrelEcalHcalB","([0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5])))))", 0, 1000);
			//functionBarrelEcalHcalB = new TF1("functionBarrelEcalHcalB","[0] + [1]*( [2]*x+[3]/( [4]*sqrt([5]*x) ) )*exp([6]*x) + [7]*exp([8]*x*x)", 0, 1000);
			functionBarrelEcalHcalC = new TF1("functionBarrelEcalHcalC","([0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5])))))", 0, 1000);
			//functionBarrelEcalHcalC = new TF1("functionBarrelEcalHcalC","[0] + [1]*( [2]*x+[3]/( [4]*sqrt([5]*x) ) )*exp([6]*x) + [7]*exp([8]*x*x)", 0, 1000);
			//functionEndcapEcalHcalB = new TF1("functionEndcapEcalHcalB","[0] + [1]*( [2]*x+[3]/( [4]*sqrt([5]*x) ) )*exp([6]*x) + [7]*exp([8]*x*x)", 0, 1000);
			functionEndcapEcalHcalB = new TF1("functionEndcapEcalHcalB","([0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5])))))", 0, 1000);
			functionEndcapEcalHcalC = new TF1("functionEndcapEcalHcalC","([0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5])))))", 0, 1000);
			//functionEndcapEcalHcalC = new TF1("functionEndcapEcalHcalC","[0] + [1]*( [2]*x+[3]/( [4]*sqrt([5]*x) ) )*exp([6]*x) + [7]*exp([8]*x*x)", 0, 1000);

			functionBarrelHcalA = new TF1("functionBarrelHcalA","[0]", 0, 1000);
			functionBarrelHcalB = new TF1("functionBarrelHcalB","[0]", 0, 1000);
			// functionBarrelHcalC = new TF1("functionBarrelHcalC","[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])", 0, 1000);
			//functionBarrelHcalC = new TF1("functionBarrelHcalC","[0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5]))))", 0, 1000);
			//spandey
			functionBarrelHcalC = new TF1("functionBarrelHcalC","([0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5])))))", 0, 1000);
			//functionBarrelHcalC = new TF1("functionBarrelHcalC","[0] + [1]*( [2]*x+[3]/( [4]*sqrt([5]*x) ) )*exp([6]*x) + [7]*exp([8]*x*x)", 0, 1000);

			functionEndcapHcalA = new TF1("functionEndcapHcalA","[0]", 0, 1000);
			functionEndcapHcalB = new TF1("functionEndcapHcalB","[0]", 0, 1000);
			functionEndcapHcalC = new TF1("functionEndcapHcalC","([0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5])))))", 0, 1000); //[0]+([1]+[2]/sqrt(x))*exp(-x/[3])-[4]*exp(-x*x/[5])
			//functionEndcapHcalC = new TF1("functionEndcapHcalC","[0] + [1]*( [2]*x+[3]/( [4]*sqrt([5]*x) ) )*exp([6]*x) + [7]*exp([8]*x*x)", 0, 1000);


			if(freezeparameters) {


				//Set the parameters of the function you just defined.
				functionBarrelEcalHcalA->FixParameter(0, aEH);

				//faBarrel
				functionBarrelEcalHcalB->FixParameter(0, -1.55434e-01);
				functionBarrelEcalHcalB->FixParameter(1,  1.18341e+00);
				functionBarrelEcalHcalB->FixParameter(2,  3.47347e+00);
				functionBarrelEcalHcalB->FixParameter(3,  1.98275e-02);
				functionBarrelEcalHcalB->FixParameter(4, -1.31039e+07);
				functionBarrelEcalHcalB->FixParameter(5,  3.66348e-02);
				functionBarrelEcalHcalB->FixParameter(6, -2.13566e+00);
				functionBarrelEcalHcalB->FixParameter(7, -5.40813e-02);
				//functionBarrelEcalHcalB->FixParameter(8, -1.61746e-08);


				//fbBarrel
				functionBarrelEcalHcalC->FixParameter(0, -5.74765e-01);
				functionBarrelEcalHcalC->FixParameter(1,  2.04313e+00);
				functionBarrelEcalHcalC->FixParameter(2, -5.17127e-01);
				functionBarrelEcalHcalC->FixParameter(3,  2.00532e-01);
				functionBarrelEcalHcalC->FixParameter(4,  1.51030e+00);
				functionBarrelEcalHcalC->FixParameter(5,  3.79849e-01);
				functionBarrelEcalHcalC->FixParameter(6, -1.40742e+00);
				functionBarrelEcalHcalC->FixParameter(7, -1.14521e-01);
				//functionBarrelEcalHcalC->FixParameter(8, -2.34041e-08);


				//fcBarrel
				functionBarrelHcalC->FixParameter(0, -1.17724e+00);
				functionBarrelHcalC->FixParameter(1,  3.41475e+01);
				functionBarrelHcalC->FixParameter(2,  5.53884e+01);
				functionBarrelHcalC->FixParameter(3,  1.96150e-01);
				functionBarrelHcalC->FixParameter(4,  3.22914e+01);
				functionBarrelHcalC->FixParameter(5,  2.03313e-01);
				functionBarrelHcalC->FixParameter(6, -6.21517e-01);
				functionBarrelHcalC->FixParameter(7, -7.42180e-01);
				//functionBarrelHcalC->FixParameter(8, -1.98386e-08);


				functionEndcapEcalHcalA->FixParameter(0, aEHe);

				//faEndcap
				functionEndcapEcalHcalB->FixParameter(0, -8.57902e+00);
				functionEndcapEcalHcalB->FixParameter(1,  7.08540e+00);
				functionEndcapEcalHcalB->FixParameter(2,  2.36338e+01);
				functionEndcapEcalHcalB->FixParameter(3,  7.63581e-01);
				functionEndcapEcalHcalB->FixParameter(4, -2.70442e+00);
				functionEndcapEcalHcalB->FixParameter(5,  6.15888e-03);
				functionEndcapEcalHcalB->FixParameter(6, -3.66774e-01);
				functionEndcapEcalHcalB->FixParameter(7, -2.30884e+00);
				//functionEndcapEcalHcalB->FixParameter(8, );


				//fbEndcap
				functionEndcapEcalHcalC->FixParameter(0, -5.06646e+03);
				functionEndcapEcalHcalC->FixParameter(1,  5.06618e+03);
				functionEndcapEcalHcalC->FixParameter(2,  2.50246e+01);
				functionEndcapEcalHcalC->FixParameter(3,  2.03008e+02);
				functionEndcapEcalHcalC->FixParameter(4, -1.17423e+00);
				functionEndcapEcalHcalC->FixParameter(5,  3.08728e-03);
				functionEndcapEcalHcalC->FixParameter(6, -5.19150e-01);
				functionEndcapEcalHcalC->FixParameter(7, -2.47078e+00);
				//functionEndcapEcalHcalC->FixParameter(8, -8.86795e-05);

				functionBarrelHcalA->FixParameter(0, aH);
				functionBarrelHcalB->FixParameter(0, 0.0);

				functionEndcapHcalA->FixParameter(0, aHe);
				functionEndcapHcalB->FixParameter(0, 0.0);

				//fcEndcap 
				functionEndcapHcalC->FixParameter(0, -6.68983e-02);
				functionEndcapHcalC->FixParameter(1,  3.89284e+01);
				functionEndcapHcalC->FixParameter(2,  3.37361e-01);
				functionEndcapHcalC->FixParameter(3,  2.42446e-03);
				functionEndcapHcalC->FixParameter(4,  3.78988e+01);
				functionEndcapHcalC->FixParameter(5,  2.17331e-03);
				functionEndcapHcalC->FixParameter(6, -4.45696e+00);
				functionEndcapHcalC->FixParameter(7, -4.54130e+00);
				//functionEndcapHcalC->FixParameter(8, -7.36681e-05);


			}
			else {

				//Set the parameters of the function you just defined.
				functionBarrelEcalHcalA->FixParameter(0, aEH);
				// functionBarrelEcalHcalB->SetParameters(1.32991e+00,1.52538e+02,-7.89866e+02,2.56441e-01,
				// 					  -1.13519e+00,2.71646e+00,1.86857e-01,4.68538e-01);
				functionBarrelEcalHcalB->SetParameters(-1.38681e+01,1.49678e+01,3.45153e+00,1.04212e+00,-2.00910e-02,
						9.41444e-16,-1.31641e+00,-7.07963e+00);
				//** begin modified by seema
				functionBarrelEcalHcalB->FixParameter(0, -13.9219);
				functionBarrelEcalHcalB->FixParameter(1, 14.9124);
				functionBarrelEcalHcalB->FixParameter(2, 5.38578);
				functionBarrelEcalHcalB->FixParameter(3, 0.861981);
				functionBarrelEcalHcalB->FixParameter(4, -0.00759275);
				functionBarrelEcalHcalB->FixParameter(5, 3.73563e-23);
				functionBarrelEcalHcalB->FixParameter(6, -1.17946);
				functionBarrelEcalHcalB->FixParameter(7, -13.3644);
				//** end modified by seema

				functionBarrelEcalHcalC->SetParameters(1.70114,0.404676,-3.88962,1.2109e+06,
						0.970741,0.0527482,2.60552,-0.8956);

				//** begin modified by seema
				//functionBarrelEcalHcalC->FixParameter(0, 1.70114 );
				//functionBarrelEcalHcalC->FixParameter(1, 0.404676 );
				//functionBarrelEcalHcalC->FixParameter(2, -3.88962);
				functionBarrelEcalHcalC->FixParameter(3, 1.2109e+06); 
				//functionBarrelEcalHcalC->FixParameter(4, 0.970741 );
				//functionBarrelEcalHcalC->FixParameter(5, 0.0527482);
				//functionBarrelEcalHcalC->FixParameter(6, 2.60552);
				//functionBarrelEcalHcalC->FixParameter(7, -0.8956);	
				//** end modified by seema  
				functionEndcapEcalHcalA->FixParameter(0, aEHe);

				functionEndcapEcalHcalB->SetParameters(0.930193,11.9536,-30.0337,0.76133,
						0.0776373,7.3809e-10,0.158734,-6.92163);

				//** begin modified by seema  
				//functionEndcapEcalHcalB->FixParameter(0, 0.930193);
				functionEndcapEcalHcalB->FixParameter(0, 0.962468);
				functionEndcapEcalHcalB->FixParameter(1, 11.9536);
				//functionEndcapEcalHcalB->FixParameter(2, -30.0337);
				//functionEndcapEcalHcalB->FixParameter(2, -28.6722);
				functionEndcapEcalHcalB->FixParameter(2, -27.7088);
				//functionEndcapEcalHcalB->FixParameter(3, 0.76133);
				//functionEndcapEcalHcalB->FixParameter(3, 0.757575);   
				//functionEndcapEcalHcalB->FixParameter(3, 0.758274);   
				functionEndcapEcalHcalB->FixParameter(3, 0.755474);
				//functionEndcapEcalHcalB->FixParameter(4, 0.0776373);
				functionEndcapEcalHcalB->FixParameter(4, 0.0791012);
				//functionEndcapEcalHcalB->FixParameter(5, 7.3809e-10);
				//functionEndcapEcalHcalB->FixParameter(5, 2.6901e-11);
				functionEndcapEcalHcalB->FixParameter(5, 2.6901e-3);
				functionEndcapEcalHcalB->FixParameter(6, 0.158734);
				//functionEndcapEcalHcalB->FixParameter(7, -6.92163);
				functionEndcapEcalHcalB->FixParameter(7, -0.92163);
				//** end modified by seema  

				functionEndcapEcalHcalC->SetParameters(-0.436687,2.73698,-3.1509,1.20536,
						-1.39685,0.0180331,0.270058,-2.30372);
				//** begin modified by seema  
				//functionEndcapEcalHcalC->FixParameter(0, -0.436687 );
				functionEndcapEcalHcalC->FixParameter(0, -0.43671);
				//functionEndcapEcalHcalC->FixParameter(1, 2.73698);
				functionEndcapEcalHcalC->FixParameter(1, 2.90096);
				//functionEndcapEcalHcalC->FixParameter(2, -3.1509);
				functionEndcapEcalHcalC->FixParameter(2, -5.10099);
				//functionEndcapEcalHcalC->FixParameter(3, 1.20536);
				functionEndcapEcalHcalC->FixParameter(3, 1.20771);
				//functionEndcapEcalHcalC->FixParameter(4, -1.39685);
				functionEndcapEcalHcalC->FixParameter(4, -1.30656);
				//functionEndcapEcalHcalC->FixParameter(5, 0.0180331);
				functionEndcapEcalHcalC->FixParameter(5, 0.0189607);
				//functionEndcapEcalHcalC->FixParameter(6, 0.270058);
				functionEndcapEcalHcalC->FixParameter(6, 0.270027);
				functionEndcapEcalHcalC->FixParameter(7, -2.30372);			  
				//** end modified by seema  


				functionBarrelHcalA->FixParameter(0, aH);
				functionBarrelHcalB->FixParameter(0, 0.0);
				functionBarrelHcalC->SetParameters(1.58827e+00,4.06865e-01,-3.69939e+00,1.28926e+03,
						7.13400e-01,2.21925e-02,1.47842e+00,-1.22041e+00);

				functionEndcapHcalA->FixParameter(0, aHe);
				functionEndcapHcalB->FixParameter(0, 0.0);

				functionEndcapHcalC->SetParameters(1.13795,1.21698,-3.81192,115.409,
						0.673456,0.217077,1.95596,-0.252215);

				//CHANGED 30 Apr

				// functionEndcapHcalC->FixParameter(0, 1.13795);
				// functionEndcapHcalC->FixParameter(1, 1.21698);
				// functionEndcapHcalC->FixParameter(2, -3.81192);
				// //functionEndcapHcalC->FixParameter(3, 115.409);
				// functionEndcapHcalC->FixParameter(3, 60.0406);
				// functionEndcapHcalC->FixParameter(4, 0.673456);
				// functionEndcapHcalC->FixParameter(5, 0.217077);
				// functionEndcapHcalC->FixParameter(6, 1.95596);
				// functionEndcapHcalC->FixParameter(7, -0.252215);
			}

			barrelWithEcalHcalCalib->fitAsToFunction(functionBarrelEcalHcalA);
			//Printing parameters:
			barrelWithEcalHcalCalib->fitBsToFunction(functionBarrelEcalHcalB);
			barrelWithEcalHcalCalib->fitBsToFunction();



			barrelWithEcalHcalCalib->fitCsToFunction(functionBarrelEcalHcalC);


			barrelWithEcalHcalCalib->fitCsToFunction();


			barrelWithEcalHcalCalib->fitCsToFunction();

			endcapWithEcalHcalCalib->fitAsToFunction(functionEndcapEcalHcalA);

			// cout<<"********************************************"<<endl;
			// cout<<"Fit Parameters, functionEndcapEcalHcalB, First"<<endl;
			// for ( unsigned i = 0; i < 10; ++i ) {
			//   double barrelEcalHcalC_spandey = functionEndcapEcalHcalB->GetParameter(i);
			//   if ( barrelEcalHcalC_spandey != 0. )
			//     cout<<"  functionEndcapEcalHcalB,Parameter("<<i<<","<<barrelEcalHcalC_spandey<<");"<<endl;
			// }

			endcapWithEcalHcalCalib->fitBsToFunction(functionEndcapEcalHcalB);

			// cout<<"********************************************"<<endl;
			// cout<<"Fit Parameters, functionEndcapEcalHcalB, First"<<endl;
			// for ( unsigned i = 0; i < 10; ++i ) {
			//   double barrelEcalHcalC_spandey = functionEndcapEcalHcalB->GetParameter(i);
			//   if ( barrelEcalHcalC_spandey != 0. )
			//     cout<<"  functionEndcapEcalHcalB,Parameter("<<i<<","<<barrelEcalHcalC_spandey<<");"<<endl;
			// }

			endcapWithEcalHcalCalib->fitBsToFunction();

			// cout<<"********************************************"<<endl;
			// cout<<"Fit Parameters, functionEndcapEcalHcalB, First"<<endl;
			// for ( unsigned i = 0; i < 10; ++i ) {
			//   double barrelEcalHcalC_spandey = functionEndcapEcalHcalB->GetParameter(i);
			//   if ( barrelEcalHcalC_spandey != 0. )
			//     cout<<"  functionEndcapEcalHcalB,Parameter("<<i<<","<<barrelEcalHcalC_spandey<<");"<<endl;
			// }

			//   cout<<"********************************************"<<endl;
			endcapWithEcalHcalCalib->fitCsToFunction(functionEndcapEcalHcalC);
			endcapWithEcalHcalCalib->fitCsToFunction();
			endcapWithEcalHcalCalib->fitCsToFunction();
			//   cout<<"Fit check 1\n";
			barrelWithHcalCalib->fitAsToFunction(functionBarrelHcalA);
			barrelWithHcalCalib->fitBsToFunction(functionBarrelHcalB);
			//   cout<<"Fit check 1.a\n";
			barrelWithHcalCalib->fitBsToFunction();
			//   cout<<"Fit check 1.b\n";
			barrelWithHcalCalib->fitCsToFunction(functionBarrelHcalC);
			barrelWithHcalCalib->fitCsToFunction();

			barrelWithHcalCalib->fitCsToFunction();
			//   cout<<"Fit check 2\n";
			endcapWithHcalCalib->fitAsToFunction(functionEndcapHcalA);
			endcapWithHcalCalib->fitBsToFunction(functionEndcapHcalB);
			endcapWithHcalCalib->fitBsToFunction();

			//   cout<<"1 FITTING ENDCAP HCAL C#######"<<endl;
			endcapWithHcalCalib->fitCsToFunction(functionEndcapHcalC);
			//   cout<<"2 FITTING ENDCAP HCAL C#######"<<endl;
			endcapWithHcalCalib->fitCsToFunction();
			//   cout<<"3 FITTING ENDCAP HCAL C#######"<<endl;
			endcapWithHcalCalib->fitCsToFunction();
			//   cout<<"Fit check 3\n";

			//exit(0);
			//Here we fill up the AlphaBeta objects, compute alpha and beta, then add 
			//them to the Calibration objects. 
			cout<<"Computing alpha and beta coefficients..."<<endl;
			for(unsigned bin = 2; bin < barrelAlphaBetaEcalHcal.size() - 1; bin++)
			{
				for(unsigned entry = 0; entry < barrelAlphaBetaEcalHcal[bin]->getSize(); entry++)
				{

					etrue = barrelAlphaBetaEcalHcal[bin]->getETrue(entry);
					ecal = barrelAlphaBetaEcalHcal[bin]->getEcal(entry);
					hcal = barrelAlphaBetaEcalHcal[bin]->getHcal(entry);
					bpar = 1.0;
					cpar = 1.0;


					if(ecal > 0 && hcal > 0)
					{
						bpar = barrelWithEcalHcalCalib->getFunctionB()->Eval(etrue);
						cpar = barrelWithEcalHcalCalib->getFunctionC()->Eval(etrue);
					}
					else if(ecal > 0)
						bpar = barrelWithEcalHcalCalib->getFunctionB()->Eval(etrue);


					barrelAlphaBetaEcalHcal[bin]->correctEcal(entry, bpar);
					barrelAlphaBetaEcalHcal[bin]->correctHcal(entry, cpar);
				}


				for(unsigned entry = 0; entry < barrelAlphaBetaHcal[bin]->getSize(); entry++)
				{

					etrue = barrelAlphaBetaHcal[bin]->getETrue(entry);
					ecal = barrelAlphaBetaHcal[bin]->getEcal(entry);
					hcal = barrelAlphaBetaHcal[bin]->getHcal(entry);
					bpar = 1.0;
					cpar = 1.0;

					if(hcal > 0 && ecal==0)
						cpar = barrelWithHcalCalib->getFunctionC()->Eval(etrue);

					// if(etrue<10)
					//   cout<<etrue<<"   "<<cpar<<endl;

					barrelAlphaBetaHcal[bin]->correctEcal(entry, bpar);
					barrelAlphaBetaHcal[bin]->correctHcal(entry, cpar);

				}     

				for(unsigned entry = 0; entry < endcapAlphaBetaEcalHcal[bin]->getSize(); entry++)
				{

					etrue = endcapAlphaBetaEcalHcal[bin]->getETrue(entry);
					ecal = endcapAlphaBetaEcalHcal[bin]->getEcal(entry);
					hcal = endcapAlphaBetaEcalHcal[bin]->getHcal(entry);
					bpar = 1.0;
					cpar = 1.0;

					if(ecal > 0 && hcal > 0)
					{
						bpar = endcapWithEcalHcalCalib->getFunctionB()->Eval(etrue);
						cpar = endcapWithEcalHcalCalib->getFunctionC()->Eval(etrue);
					}
					else if(ecal > 0)
						bpar = endcapWithEcalHcalCalib->getFunctionB()->Eval(etrue);

					endcapAlphaBetaEcalHcal[bin]->correctEcal(entry, bpar);
					endcapAlphaBetaEcalHcal[bin]->correctHcal(entry, cpar);
				}

				for(unsigned entry = 0; entry < endcapAlphaBetaHcal[bin]->getSize(); entry++)
				{

					etrue = endcapAlphaBetaHcal[bin]->getETrue(entry);
					ecal = endcapAlphaBetaHcal[bin]->getEcal(entry);
					hcal = endcapAlphaBetaHcal[bin]->getHcal(entry);
					bpar = 1.0;
					cpar = 1.0;

					if(ecal == 0 && hcal > 0)
					{
						cpar = endcapWithHcalCalib->getFunctionC()->Eval(etrue);
					}
					endcapAlphaBetaHcal[bin]->correctEcal(entry, bpar);
					endcapAlphaBetaHcal[bin]->correctHcal(entry, cpar);
				}


				barrelAlphaBetaEcalHcal[bin]->computeSigmaEcalHcal();
				barrelAlphaBetaEcalHcal[bin]->computeETrueAverage();
				barrelAlphaBetaEcalHcal[bin]->computeETrueRMS();

				barrelAlphaBetaHcal[bin]->computeSigmaEcalHcal();
				barrelAlphaBetaHcal[bin]->computeETrueAverage();
				barrelAlphaBetaHcal[bin]->computeETrueRMS();

				endcapAlphaBetaEcalHcal[bin]->computeSigmaEcalHcal();
				endcapAlphaBetaEcalHcal[bin]->computeETrueAverage();
				endcapAlphaBetaEcalHcal[bin]->computeETrueRMS();

				endcapAlphaBetaHcal[bin]->computeSigmaEcalHcal();
				endcapAlphaBetaHcal[bin]->computeETrueAverage();
				endcapAlphaBetaHcal[bin]->computeETrueRMS();

				if(barrelAlphaBetaEcalHcal[bin]->computeAlphaBeta())
				{
					barrelWithEcalHcalCalib->addGraphPoints(barrelAlphaBetaEcalHcal[bin]);
					barrelWithEcalCalib->addGraphPoints(barrelAlphaBetaEcalHcal[bin]);
				}
				if(barrelAlphaBetaHcal[bin]->computeAlphaBeta()) {
					barrelWithHcalCalib->addGraphPoints(barrelAlphaBetaHcal[bin]);
				}

				if(endcapAlphaBetaEcalHcal[bin]->computeAlphaBeta())
				{
					endcapWithEcalHcalCalib->addGraphPoints(endcapAlphaBetaEcalHcal[bin]);
					endcapWithEcalCalib->addGraphPoints(endcapAlphaBetaEcalHcal[bin]);
				}


				if(endcapAlphaBetaHcal[bin]->computeAlphaBeta()) //FIXME
				{
					endcapWithHcalCalib->addGraphPoints(endcapAlphaBetaHcal[bin]);
				}
			}

			cout<<"Fitting alpha, beta coefficients..."<<endl;
			barrelWithEcalHcalCalib->initializeGraphs("alphabeta");
			barrelWithEcalCalib->initializeGraphs("alphabeta");
			barrelWithHcalCalib->initializeGraphs("alphabeta");   
			endcapWithEcalHcalCalib->initializeGraphs("alphabeta");
			endcapWithEcalCalib->initializeGraphs("alphabeta");
			endcapWithHcalCalib->initializeGraphs("alphabeta");   

			//functionBarrelAlphaEcalHcal = new TF1("functionBarrelAlphaEcalHcal","[0]+[1]*exp(-x/[2])", 0, 1000);
			//functionBarrelBetaEcalHcal = new TF1("functionBarrelBetaEcalHcal","[0]+[1]*exp(-x/[2])", 0, 1000);

			//functionBarrelAlphaHcal = new TF1("functionBarrelAlphaHcal","[0]+[1]*x", 0, 1000);// +[1]*exp(-x/[2])
			//functionBarrelBetaHcal = new TF1("functionBarrelBetaHcal","[0]+[1]*exp(-x/[2])", 0, 1000);

			//functionEndcapAlphaEcalHcal = new TF1("functionEndcapAlphaEcalHcal","[0]+[1]*exp(-x/[2])", 0, 1000);
			//functionEndcapBetaEcalHcal = new TF1("functionEndcapBetaEcalHcal","[0]+[1]*exp(-x/[2])",0,1000); //+[3]*[3]*exp(-x*x/([4]*[4]))

			//functionEndcapAlphaHcal = new TF1("functionEndcapAlphaHcal","[0]+[1]*exp(-x/[2])+[3]*[3]*exp(-x*x/([4]*[4]))", 0, 1000);// +[1]*exp(-x/[2])
			//functionEndcapBetaHcal = new TF1("functionEndcapBetaHcal","[0]+[1]*exp(-x/[2])+[3]*[3]*exp(-x*x/([4]*[4]))",0,1000);
			functionEndcapGammaHcal = new TF1("functionEndcapGammaHcal","[0]+[1]*exp(-x/[2])+[3]*[3]*exp(-x*x/([4]*[4]))",0,1000);

			functionBarrelAlphaEcalHcal = new TF1("functionBarrelAlphaEcalHcal","[0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5]))))", 0, 1000);
			functionBarrelBetaEcalHcal = new TF1("functionBarrelBetaEcalHcal","[0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5]))))", 0, 1000);
      //functionBarrelBetaEcalHcal = new TF1("functionBarrelBetaEcalHcal","[0] + [1]*( [2]*x+[3]/( [4]*sqrt([5]*x) ) )*exp([6]*x) + [7]*exp([8]*x*x)", 0, 1000); 
			functionBarrelAlphaHcal = new TF1("functionBarrelAlphaHcal","[0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5]))))", 0, 1000);
			functionBarrelBetaHcal = new TF1("functionBarrelBetaHcal","[0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5]))))", 0, 1000);
			functionEndcapAlphaEcalHcal = new TF1("functionEndcapAlphaEcalHcal","[0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5]))))", 0, 1000);
			functionEndcapBetaEcalHcal = new TF1("functionEndcapBetaEcalHcal","[0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5]))))", 0, 1000);
			functionEndcapAlphaHcal = new TF1("functionEndcapAlphaHcal","[0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5]))))", 0, 1000);
			functionEndcapBetaHcal = new TF1("functionEndcapBetaHcal","[0]+((([1]+([2]/sqrt(x)))*exp(-(x^[6]/[3])))-([4]*exp(-(x^[7]/[5]))))", 0, 1000);


			if(freezeparameters) {


				////////////////////////////////////////////////////


				//faEtaBarrelEH

				functionBarrelAlphaEcalHcal->FixParameter(0, -9.67378e-01);
				functionBarrelAlphaEcalHcal->FixParameter(1,  4.05581e+01);
				functionBarrelAlphaEcalHcal->FixParameter(2, -1.62321e-01);
				functionBarrelAlphaEcalHcal->FixParameter(3,  7.31830e-04);
				functionBarrelAlphaEcalHcal->FixParameter(4,  3.95861e+01);
				functionBarrelAlphaEcalHcal->FixParameter(5,  7.37024e-04);
				functionBarrelAlphaEcalHcal->FixParameter(6, -3.67952e+00);
				functionBarrelAlphaEcalHcal->FixParameter(7, -3.65751e+00);


				//fbEtaBarrelEH

				functionBarrelBetaEcalHcal->FixParameter(0, -4.26451e-01);
				functionBarrelBetaEcalHcal->FixParameter(1,  1.19824e+02);
				functionBarrelBetaEcalHcal->FixParameter(2,  1.53190e+00);
				functionBarrelBetaEcalHcal->FixParameter(3,  4.08701e-03);
				functionBarrelBetaEcalHcal->FixParameter(4,  1.19415e+02);
				functionBarrelBetaEcalHcal->FixParameter(5,  4.00613e-03);
				functionBarrelBetaEcalHcal->FixParameter(6, -2.08406e+00);
				functionBarrelBetaEcalHcal->FixParameter(7, -2.08986e+00);
                                                    

				//faEtaBarrelH

				functionBarrelAlphaHcal->FixParameter(0, -7.91008e-01);
				functionBarrelAlphaHcal->FixParameter(1,  4.04864e+01);
				functionBarrelAlphaHcal->FixParameter(2,  3.18832e-02);
				functionBarrelAlphaHcal->FixParameter(3,  4.93219e-02);
				functionBarrelAlphaHcal->FixParameter(4,  3.96898e+01);
				functionBarrelAlphaHcal->FixParameter(5,  4.68394e-02);
				functionBarrelAlphaHcal->FixParameter(6, -2.08181e+00);
				functionBarrelAlphaHcal->FixParameter(7, -2.09659e+00);


				//fbEtaBarrelH

				functionBarrelBetaHcal->FixParameter(0, -2.63647e+01);
				functionBarrelBetaHcal->FixParameter(1,  2.65125e+01);
				functionBarrelBetaHcal->FixParameter(2,  2.04895e+01);
				functionBarrelBetaHcal->FixParameter(3,  1.61225e+00);
				functionBarrelBetaHcal->FixParameter(4,  2.17624e-02);
				functionBarrelBetaHcal->FixParameter(5,  4.57794e-05);
				functionBarrelBetaHcal->FixParameter(6, -4.42631e-01);
				functionBarrelBetaHcal->FixParameter(7, -1.83439e+00);


				//faEtaEndcapEH

				functionEndcapAlphaEcalHcal->FixParameter(0, -8.31910e-01);
				functionEndcapAlphaEcalHcal->FixParameter(1,  4.04830e+01);
				functionEndcapAlphaEcalHcal->FixParameter(2,  7.97539e-02);
				functionEndcapAlphaEcalHcal->FixParameter(3,  2.45609e-03);
				functionEndcapAlphaEcalHcal->FixParameter(4,  3.96610e+01);
				functionEndcapAlphaEcalHcal->FixParameter(5,  2.44846e-03);
				functionEndcapAlphaEcalHcal->FixParameter(6, -2.46522e+00);
				functionEndcapAlphaEcalHcal->FixParameter(7, -2.45455e+00);

				//fbEtaEndcapEH

				functionEndcapBetaEcalHcal->FixParameter(0,  7.31823e-02);
				functionEndcapBetaEcalHcal->FixParameter(1,  1.19792e+02);
				functionEndcapBetaEcalHcal->FixParameter(2, -7.31083e+00);
				functionEndcapBetaEcalHcal->FixParameter(3,  1.76734e-02);
				functionEndcapBetaEcalHcal->FixParameter(4,  1.19456e+02);
				functionEndcapBetaEcalHcal->FixParameter(5,  1.87185e-02);
				functionEndcapBetaEcalHcal->FixParameter(6, -1.40489e+00);
				functionEndcapBetaEcalHcal->FixParameter(7, -1.38142e+00);


				//faEtaEndcapH

				functionEndcapAlphaHcal->FixParameter(0, -2.13979e+01);
				functionEndcapAlphaHcal->FixParameter(1,  1.58322e+00);
				functionEndcapAlphaHcal->FixParameter(2, -1.26740e+00);
				functionEndcapAlphaHcal->FixParameter(3, -2.91817e-01);
				functionEndcapAlphaHcal->FixParameter(4, -1.87510e+01);
				functionEndcapAlphaHcal->FixParameter(5,  6.05940e-01);
				functionEndcapAlphaHcal->FixParameter(6, -1.85322e-01);
				functionEndcapAlphaHcal->FixParameter(7, -4.42461e-01);


				//fbEtaEndcapH

				functionEndcapBetaHcal->FixParameter(0, -3.43105e+00);
				functionEndcapBetaHcal->FixParameter(1,  1.00690e+02);
				functionEndcapBetaHcal->FixParameter(2, -4.20111e+01);
				functionEndcapBetaHcal->FixParameter(3,  3.32362e+00);
				functionEndcapBetaHcal->FixParameter(4,  8.69782e+01);
				functionEndcapBetaHcal->FixParameter(5,  1.51010e+00);
				functionEndcapBetaHcal->FixParameter(6, -1.10964e-01);
				functionEndcapBetaHcal->FixParameter(7, -3.67676e-01);


				if(functionBarrelAlphaEcalHcal->GetMaximum() > 1e5) cout << "functionBarrelAlphaEcalHcal is diverge" << endl;
				if(functionBarrelAlphaEcalHcal->GetMinimum() < -1e5) cout << "functionBarrelAlphaEcalHcal is diverge" << endl;
				if(functionBarrelBetaEcalHcal->GetMaximum() > 1e5) cout << "functionBarrelBetaEcalHcal is diverge" << endl;
				if(functionBarrelBetaEcalHcal->GetMinimum() < -1e5) cout << "functionBarrelBetaEcalHcal is diverge" << endl;
				if(functionBarrelAlphaHcal->GetMaximum() > 1e5) cout << "functionBarrelAlphaHcal is diverge" << endl;
				if(functionBarrelAlphaHcal->GetMinimum() < -1e5) cout << "functionBarrelAlphaHcal is diverge" << endl;
				if(functionBarrelBetaHcal->GetMaximum() > 1e5) cout << "functionBarrelBetaHcal is diverge" << endl;
				if(functionBarrelBetaHcal->GetMinimum() < -1e5) cout << "functionBarrelBetaHcal is diverge" << endl;
				if(functionEndcapAlphaEcalHcal->GetMaximum() > 1e5) cout << "functionEndcapAlphaEcalHcal is diverge" << endl;
				if(functionEndcapAlphaEcalHcal->GetMinimum() < -1e5) cout << "functionEndcapAlphaEcalHcal is diverge" << endl;
				if(functionEndcapBetaEcalHcal->GetMaximum() > 1e5) cout << "functionEndcapBetaEcalHcal is diverge" << endl;
				if(functionEndcapBetaEcalHcal->GetMinimum() < -1e5) cout << "functionEndcapBetaEcalHcal is diverge" << endl;
				if(functionEndcapAlphaHcal->GetMaximum() > 1e5) cout << "functionEndcapAlphaHcal is diverge" << endl;
				if(functionEndcapAlphaHcal->GetMinimum() < -1e5) cout << "functionEndcapAlphaHcal is diverge" << endl;
				if(functionEndcapBetaHcal->GetMaximum() > 1e5) cout << "functionEndcapBetaHcal is diverge" << endl;
				if(functionEndcapBetaHcal->GetMinimum() < -1e5) cout << "functionEndcapBetaHcal is diverge" << endl;


			}

			else {
				functionBarrelAlphaEcalHcal->SetParameters(0.02, -0.1, sampleRangeHigh);
				// functionBarrelBeta->SetParameters(-0.02, 0.4, sampleRangeHigh);
				//  functionBarrelAlpha->SetParameters(-2.33313e-02,-7.56070e+00,1.39070e+00,1.13114e+00);
				functionBarrelBetaEcalHcal->SetParameters(1.17842e-01,1.71167e-01,5.88921e+00);

				functionBarrelAlphaHcal->SetParameters(0.02, -0.1, sampleRangeHigh);
				functionBarrelBetaHcal->SetParameters(1.17842e-01,1.71167e-01,5.88921e+00);

				functionEndcapAlphaEcalHcal->SetParameters(0.02, -0.1, sampleRangeHigh);
				//functionEndcapBetaEcalHcal->SetParameters(0.07, -2.5, 6.0, 0.3, 175.0);
				functionEndcapBetaEcalHcal->SetParameters(0.0399873, -1.51747, 3.22236);

				functionEndcapAlphaHcal->SetParameters(0.02, -0.1, sampleRangeHigh, 0.5, 0.6);
				functionEndcapBetaHcal->SetParameters(0.07, -2.5, 6.0, 0.3, 175.0);
				functionEndcapGammaHcal->SetParameters(-1.71458e+00,9.61337e+00,2.94747e+00);

			}



			barrelWithEcalHcalCalib->fitAlphasToFunction(functionBarrelAlphaEcalHcal);
			barrelWithEcalHcalCalib->fitAlphasToFunction();
			barrelWithEcalHcalCalib->fitBetasToFunction(functionBarrelBetaEcalHcal);
			barrelWithEcalHcalCalib->fitBetasToFunction();
			endcapWithEcalHcalCalib->fitAlphasToFunction(functionEndcapAlphaEcalHcal);
			endcapWithEcalHcalCalib->fitAlphasToFunction();
			endcapWithEcalHcalCalib->fitBetasToFunction(functionEndcapBetaEcalHcal);
			endcapWithEcalHcalCalib->fitBetasToFunction();

			barrelWithHcalCalib->fitAlphasToFunction(functionBarrelAlphaHcal);
			barrelWithHcalCalib->fitAlphasToFunction();
			barrelWithHcalCalib->fitBetasToFunction(functionBarrelBetaHcal);
			barrelWithHcalCalib->fitBetasToFunction();
			endcapWithHcalCalib->fitAlphasToFunction(functionEndcapAlphaHcal);
			endcapWithHcalCalib->fitAlphasToFunction();
			endcapWithHcalCalib->fitBetasToFunction(functionEndcapBetaHcal);
			endcapWithHcalCalib->fitBetasToFunction();
			endcapWithHcalCalib->fitGammasToFunction(functionEndcapGammaHcal);
			endcapWithHcalCalib->fitGammasToFunction();



			//Fill all the TH2's that can be put into drawGausFit in order to produce 
			//response and resolution plots.
			cout<<"Making response and resolution plots..."<<endl;
			for(unsigned entry = 0; entry < ETrueEnergies.size(); ++entry)
			{

				etrue = ETrueEnergies[entry];
				ecal = ecalEnergies[entry];
				hcal = hcalEnergies[entry];
				eta = abs(etas[entry]);
				double phi = phis[entry];
				if((ecal + hcal) < 0.5) continue;
				if( etrue < 1.0) continue;
				if( hcal == 0) continue;
				//if( etrue/cosh(eta) > 10.0) continue;
				// if( ecal > 0) continue;
				if(fabs(eta) < 2.5) continue; // delete me

				if(fabs(eta) < 1.5) //alpha beta fit range for barrel
				{     
					Raw->Fill(etrue, (ecal + hcal - etrue)/etrue);
					if(ecal > 0)
					{


						correctedEta = barrelWithEcalHcalCalib->
							getCalibratedEnergy(etrue, ecal, hcal, eta);

						correctedE = barrelWithEcalHcalCalib->
							getCalibratedEnergy(etrue, ecal, hcal);


						if(drawpT) {
							etrue = etrue/cosh(eta);
							correctedEta = correctedEta/cosh(eta);
							ecal = ecal/cosh(eta);
							hcal = hcal/cosh(eta);
							correctedE = correctedE/cosh(eta);
						}

						corrEta->Fill(etrue, (correctedEta - etrue)/etrue);
						corrEtaBarrel->Fill(etrue, (correctedEta - etrue)/etrue);
						corrEtaBarrelEcalHcal->Fill(etrue, (correctedEta - etrue)/etrue);

						rawEtaDependenceEH->Fill(eta, (ecal + hcal - etrue)/etrue);
						//if (etrue > 20) {
						corrEtaDependenceEH->Fill(eta, (correctedEta - etrue)/etrue);
						hcorrEtaDependenceEH->Fill(eta, (correctedE - etrue)/etrue);
						hhcorrEtaDependenceEH->Fill(etas[entry], (correctedEta - etrue)/etrue);
						//}
						corrEtaDependenceProfEH->Fill(etrue, eta, (correctedEta - etrue)/etrue);


						h_trueE_vs_mod_eta_response_normalized->Fill(eta,etrue, (correctedEta - etrue)/etrue);
						h_trueE_vs_mod_eta_response->Fill(eta,etrue);



					}
					else 
					{

						correctedEta = barrelWithHcalCalib->
							getCalibratedEnergy(etrue, ecal, hcal, eta);

						correctedE = barrelWithHcalCalib->
							getCalibratedEnergy(etrue, ecal, hcal);


						if(drawpT) {
							etrue = etrue/cosh(eta);
							correctedEta = correctedEta/cosh(eta);
							ecal = ecal/cosh(eta);
							hcal = hcal/cosh(eta);
							correctedE = correctedE/cosh(eta);
						}

						if(etrue>7 && etrue<9) {
							for(int k=0;k<1000;k++) {
								float step=k/500.-0.99995;
								float b= step;
								float a = (etrue - 3.5 )/hcal - 1 -b*eta*eta;
								bcplot->Fill(b,a);
							}
						}



						corrEta->Fill(etrue, (correctedEta - etrue)/etrue);
						corrEtaBarrel->Fill(etrue, (correctedEta - etrue)/etrue);
						corrEtaBarrelHcal->Fill(etrue, (correctedEta - etrue)/etrue);

						rawEtaDependenceH->Fill(eta, (ecal + hcal - etrue)/etrue);
						//if((fabs(eta) < 1.5) && (correctedEta != correctedE)) cout<<"yolo "<<fabs(eta)<<", correctedEta:"<<correctedEta<<", correctedE:"<<correctedE<<", (correctedEta != correctedE):"
						//<<(correctedEta != correctedE)<<endl;
						corrEtaDependenceH->Fill(eta, (correctedEta - etrue)/etrue);
						hcorrEtaDependenceH->Fill(eta, (correctedE - etrue)/etrue);
						hhcorrEtaDependenceH->Fill(etas[entry], (correctedEta - etrue)/etrue);
						corrEtaDependenceProfH->Fill(etrue, eta, (correctedEta - etrue)/etrue);

					}
					//if(fabs(eta) < 1.0) //b, c fit range
					if(fabs(eta) < 1.5) //b, c fit range //shubham Mar 27
					{
						rawBarrel->Fill(etrue, (ecal + hcal - etrue)/etrue);

						if(ecal > 0)
						{
							correctedE = barrelWithEcalHcalCalib->
								getCalibratedEnergy(etrue, ecal, hcal);


							if(drawpT) {
								etrue = etrue/cosh(eta);
								correctedEta = correctedEta/cosh(eta);
								ecal = ecal/cosh(eta);
								hcal = hcal/cosh(eta);
								correctedE = correctedE/cosh(eta);
							}

							//rawBarrelEcalHcal->Fill(etrue, (ecal + hcal  - etrue)/etrue );
							rawBarrelEcalHcal->Fill(etrue, (ecal + hcal  - etrue)/etrue );
							corrBarrel->Fill(etrue, (correctedE - etrue)/etrue);
							corrBarrelEcalHcal->Fill(etrue, (correctedE - etrue)/etrue);

							// hcorrEtaDependence->Fill(eta, (correctedE - etrue)/etrue);

							// rawEtaDependence->Fill(eta, (ecal + hcal - etrue)/etrue);
							// corrEtaDependence->Fill(eta, (correctedEta - etrue)/etrue);

							// if(entry<5000) 
							// 	 cout<<entry<<"   "<<eta<<"   "<<etrue<<"   "<<ecal+hcal<<"   "<<correctedE<<"   "<<correctedEta<<endl;


							h_response_vs_phi_barrel_EH->Fill(phi, (correctedE - etrue)/etrue); //shuham


						}
						else
						{
							correctedE = barrelWithHcalCalib->
								getCalibratedEnergy(etrue, ecal, hcal);


							if(drawpT) {
								etrue = etrue/cosh(eta);
								correctedEta = correctedEta/cosh(eta);
								ecal = ecal/cosh(eta);
								hcal = hcal/cosh(eta);
								correctedE = correctedE/cosh(eta);
							}

							rawBarrelHcal->Fill(etrue, ( ecal + hcal - etrue)/etrue );// (etrue-3.0)/(ecal+hcal) );//, 11936/(3917*sigmas[entry]*sigmas[entry]) );// ( ecal + hcal - etrue)/etrue );

							corrBarrel->Fill(etrue, (correctedE- etrue )/etrue);// 
							corrBarrelHcal->Fill(etrue, (correctedE- etrue )/etrue);

							h_response_vs_phi_barrel_H->Fill(phi, (correctedE - etrue)/etrue); //shuham


						}
					}
				}

				//if(fabs(eta) < 3.0 && fabs(eta) > 1.5) //WITHIN TRACKER alpha beta fit range for endcap 
				//if(fabs(eta) < 3.0 && fabs(eta) > 1.55) //FULL EndCap alpha beta fit range for endcap   //shubham
				//if(fabs(eta) < 3.0 && fabs(eta) > 2.5) //OUTSIDE TRACKER alpha beta fit range for endcap   //shubham
				if(fabs(eta) < _etaMax_ && fabs(eta) > _etaMin_) 
				{
					//if (fabs(eta) > 2.7) cout<<"yolo "<<fabs(eta)<<endl;
					Raw->Fill(etrue, (ecal + hcal - etrue)/etrue);

					////////////////////////
					// RAW Proxy
					double etrue_proxy;
					if (fabs(eta) > 2.5)
						etrue_proxy = etrue;//ecal + hcal;
					else
						etrue_proxy = etrue;

					if(ecal > 0)
					{
						correctedEta = endcapWithEcalHcalCalib->
							getCalibratedEnergy(etrue_proxy, ecal, hcal, eta);

						correctedE = endcapWithEcalHcalCalib->
							getCalibratedEnergy(etrue_proxy, ecal, hcal);

						if(drawpT) {
							etrue = etrue/cosh(eta);
							etrue_proxy = etrue_proxy/cosh(eta);
							correctedEta = correctedEta/cosh(eta);
							ecal = ecal/cosh(eta);
							hcal = hcal/cosh(eta);
							correctedE = correctedE/cosh(eta);
						}

						corrEta->Fill(etrue, (correctedEta - etrue)/etrue);
						corrEtaEndcap->Fill(etrue, (correctedEta - etrue)/etrue);

						corrEtaEndcapEcalHcal->Fill(etrue, (correctedEta - etrue)/etrue);
						//////changed changed changed 30 Apr 
						//corrEtaEndcapEcalHcal->Fill((ecal+hcal), (correctedEta - etrue)/etrue);

						rawEtaDependenceEH->Fill(eta, (ecal + hcal - etrue)/etrue);
						//if (etrue > 20) {
						corrEtaDependenceEH->Fill(eta, (correctedEta - etrue)/etrue);
						hcorrEtaDependenceEH->Fill(eta, (correctedE - etrue)/etrue); //FIXME
						hhcorrEtaDependenceEH->Fill(etas[entry], (correctedEta - etrue)/etrue); //FIXME
						//}
						corrEtaDependenceProfEH->Fill(etrue, eta, (correctedEta - etrue)/etrue);

						h_trueE_vs_mod_eta_response_normalized->Fill(eta,etrue, (correctedEta - etrue)/etrue);
						h_trueE_vs_mod_eta_response->Fill(eta,etrue);

					}
					else
					{
						correctedEta = endcapWithHcalCalib->
							getCalibratedEnergy(etrue_proxy, ecal, hcal, eta);

						correctedE = endcapWithHcalCalib->
							getCalibratedEnergy(etrue_proxy, ecal, hcal);


						if(drawpT) {
							etrue = etrue/cosh(eta);
							etrue_proxy = etrue_proxy/cosh(eta);
							correctedEta = correctedEta/cosh(eta);
							ecal = ecal/cosh(eta);
							hcal = hcal/cosh(eta);
							correctedE = correctedE/cosh(eta);
						}

						corrEta->Fill(etrue, (correctedEta - etrue)/etrue);            
						corrEtaEndcap->Fill(etrue, (correctedEta - etrue)/etrue);
						corrEtaEndcapHcal->Fill(etrue, (correctedEta - etrue)/etrue);

						rawEtaDependenceH->Fill(eta, (ecal + hcal - etrue)/etrue);
						corrEtaDependenceH->Fill(eta, (correctedEta - etrue)/etrue);
						hcorrEtaDependenceH->Fill(eta, (correctedE - etrue)/etrue);
						hhcorrEtaDependenceH->Fill(etas[entry], (correctedEta - etrue)/etrue);
						corrEtaDependenceProfH->Fill(etrue, eta, (correctedEta - etrue)/etrue);

					}
					//if(fabs(eta) < 2.2) //b, c fi trange
					if(fabs(eta) < 3.0) //b, c fi trange   //shubham
					{
						rawEndcap->Fill(etrue, (ecal + hcal - etrue)/etrue);

						if(ecal > 0)
						{

							correctedEta = endcapWithEcalHcalCalib->
								getCalibratedEnergy(etrue_proxy, ecal, hcal, eta);

							correctedE = endcapWithEcalHcalCalib->
								getCalibratedEnergy(etrue_proxy, ecal, hcal);


							if(drawpT) {
								etrue = etrue/cosh(eta);
								etrue_proxy = etrue_proxy/cosh(eta);
								correctedEta = correctedEta/cosh(eta);
								ecal = ecal/cosh(eta);
								hcal = hcal/cosh(eta);
								correctedE = correctedE/cosh(eta);
							}

							rawEndcapEcalHcal->Fill(etrue, (ecal + hcal - etrue)/etrue);
							corrEndcap->Fill(etrue, (correctedE - etrue)/etrue);
							corrEndcapEcalHcal->Fill(etrue, (correctedE - etrue)/etrue);



							// rawEtaDependence->Fill(eta, (ecal + hcal - etrue)/etrue);
							// corrEtaDependence->Fill(eta, (correctedEta - etrue)/etrue);
							// hcorrEtaDependence->Fill(eta, (correctedE - etrue)/etrue);

							//cout<<"yolo, eta:"<<eta<<endl;
							if(etas[entry] > 0)
								h_response_vs_phi_EndCap_EH_posZ->Fill(phi,(correctedE - etrue)/etrue);
							else if(etas[entry] < 0)
								h_response_vs_phi_EndCap_EH_negZ->Fill(phi,(correctedE - etrue)/etrue);

						}
						else 
						{
							correctedE = endcapWithHcalCalib->
								getCalibratedEnergy(etrue, ecal, hcal);


							if(drawpT) {
								etrue = etrue/cosh(eta);
								etrue_proxy = etrue_proxy/cosh(eta);
								correctedEta = correctedEta/cosh(eta);
								ecal = ecal/cosh(eta);
								hcal = hcal/cosh(eta);
								correctedE = correctedE/cosh(eta);
							}

							rawEndcapHcal->Fill(etrue, (ecal + hcal - etrue)/etrue);
							corrEndcap->Fill(etrue, (correctedE - etrue)/etrue);
							corrEndcapHcal->Fill(etrue, (correctedE - etrue)/etrue);

							if(etas[entry] > 0)
								h_response_vs_phi_EndCap_H_posZ->Fill(phi,(correctedE - etrue)/etrue);
							else if(etas[entry] < 0)
								h_response_vs_phi_EndCap_H_negZ->Fill(phi,(correctedE - etrue)/etrue);



						}
					}
					else  {   //shubham
						if(ecal > 0) 
							corrEndcapEcalHcal->Fill(etrue, (correctedE - etrue)/etrue);
					}
				}  
			}

			////////////////////////////////////////////////////////////////////////////
			//Add all the draw functions that you would like here, as well as any 
			//additional output you would like.
			////////////////////////////////////////////////////////////////////////////

			cout<<" Now Summary "<<endl;

			//   exit(0);
			//rawBarrel->Draw("colz");
			//rawBarrelEcalHcal->Draw("colz");
			//rawBarrelHcal->Draw("colz");

			drawGausFit(rawBarrelHcal,responseRawH,resolutionRawH, "resolution_raw_H_barrel");
			drawGausFit(corrBarrelHcal,responseCorBarH,resolutionCorBarH, "resolution_E_corr_H_barrel");
			drawGausFit(corrEtaBarrelHcal,responseCorEtaBarH,resolutionCorEtaBarH, "resolution_Eta_corr_H_barrel");
			drawGausFit(rawEndcapHcal,responseRawEndH,resolutionRawEndH, "resolution_raw_H_endcap");
			drawGausFit(corrEndcapHcal,responseCorEndH,resolutionCorEndH, "resolution_E_corr_H_endcap");
			drawGausFit(corrEtaEndcapHcal, responseCorEtaEndH, resolutionCorEtaEndH, "resolution_Eta_corr_H_endcap");

			drawGausFit(rawBarrelEcalHcal,responseRawEH,resolutionRawEH, "resolution_raw_EH_barrel");
			drawGausFit(corrBarrelEcalHcal,responseCorBarEH,resolutionCorBarEH, "resolution_E_corr_EH_barrel");
			drawGausFit(corrEtaBarrelEcalHcal, responseCorEtaBarEH, resolutionCorEtaBarEH, "resolution_Eta_corr_EH_barrel");
			drawGausFit(rawEndcapEcalHcal,responseRawEndEH,resolutionRawEndEH, "resolution_raw_EH_endcap");
			drawGausFit(corrEndcapEcalHcal,responseCorEndEH,resolutionCorEndEH, "resolution_E_corr_EH_endcap");
			drawGausFit(corrEtaEndcapEcalHcal,responseCorEtaEndEH,resolutionCorEtaEndEH, "resolution_Eta_corr_EH_endcap");




			//drawGausFit(rawBarrel,responseRaw,resolutionRaw);
			// something for overall

			drawEtaDependence(rawEtaDependenceEH, responseEtaEtaEH);
			drawEtaDependence(hcorrEtaDependenceEH, responseEtaHCorrEtaEH);
			drawEtaDependence(corrEtaDependenceEH, responseEtaEtaEH);
			//drawEtaDependence(hhcorrEtaDependenceEH, responseEtaHCorrEtaEH);

			drawEtaDependence(rawEtaDependenceH, responseEtaEtaH);
			drawEtaDependence(hcorrEtaDependenceH, responseEtaHCorrEtaH);
			drawEtaDependence(corrEtaDependenceH, responseEtaEtaH);
			//drawEtaDependence(hhcorrEtaDependenceH, responseEtaHCorrEtaH);

			//drawGausFit(corrEta,response, resolution);
			//drawCompare(responseRaw, response, resolutionRaw, resolution);





			// barrel H calibration coefficient
			barrelWithHcalCalib->drawCoeffGraph("C", "H_barrel",  "coeffC_barrel");
			barrelWithHcalCalib->drawCoeffGraph("Alpha","H_barrel", "coeffAlpha_H_barrel");
			barrelWithHcalCalib->drawCoeffGraph("Beta", "H_barrel", "coeffBeta_H_barrel");

			// endcap H calibration coefficient
			endcapWithHcalCalib->drawCoeffGraph("C", "H_endcap", "coeffC_endcap");
			endcapWithHcalCalib->drawCoeffGraph("Alpha","H_endcap", "coeffAlpha_H_endcap");
			endcapWithHcalCalib->drawCoeffGraph("Beta", "H_endcap", "coeffBeta_H_endcap");

			// barrel EH calibration coefficient
			barrelWithEcalHcalCalib->drawCoeffGraph("A","EH_barrel", "coeffA_barrel");
			barrelWithEcalHcalCalib->drawCoeffGraph("B", "EH_barrel", "coeffB_barrel");
			barrelWithEcalHcalCalib->drawCoeffGraph("Alpha","EH_barrel", "coeffAlpha_EH_barrel");
			barrelWithEcalHcalCalib->drawCoeffGraph("Beta", "EH_barrel", "coeffBeta_EH_barrel");

			// endcap EH calibration coefficient
			endcapWithEcalHcalCalib->drawCoeffGraph("A","EH_endcap", "coeffA_endcap");
			endcapWithEcalHcalCalib->drawCoeffGraph("B", "EH_endcap", "coeffB_endcap");
			endcapWithEcalHcalCalib->drawCoeffGraph("Alpha","EH_endcap", "coeffAlpha_EH_endcap");
			endcapWithEcalHcalCalib->drawCoeffGraph("Beta", "EH_endcap", "coeffBeta_EH_endcap");

			//cout<<"Check pt 1"<<endl;
			/*
				 h_trueE_vs_mod_eta_response_normalized->SetXTitle("|#eta|");
				 h_trueE_vs_mod_eta_response_normalized->SetYTitle("True Energy");

				 h_trueE_vs_mod_eta_response_normalized->Divide(h_trueE_vs_mod_eta_response);

				 h_trueE_vs_mod_eta_response_normalized->SetMinimum(-0.2);
				 h_trueE_vs_mod_eta_response_normalized->SetMaximum(0.2);
				 h_trueE_vs_mod_eta_response_normalized->Draw("colz");
				 */

			//h_response_vs_phi_barrel_EH->Draw(); //shuham

			h_response_vs_phi_EndCap_EH_posZ->SetXTitle("#phi");
			h_response_vs_phi_EndCap_EH_negZ->SetXTitle("#phi");
			h_response_vs_phi_barrel_EH->SetXTitle("#phi"); //shuham
			h_response_vs_phi_EndCap_H_posZ->SetXTitle("#phi");
			h_response_vs_phi_EndCap_H_negZ->SetXTitle("#phi");
			h_response_vs_phi_barrel_H->SetXTitle("#phi");


			h_response_vs_phi_EndCap_EH_posZ->SetYTitle("(E_{corr} - E_{true} / E_{true})");
			h_response_vs_phi_EndCap_EH_negZ->SetYTitle("(E_{corr} - E_{true} / E_{true})");
			h_response_vs_phi_barrel_EH->SetYTitle("(E_{corr} - E_{true} / E_{true})"); //shuham
			h_response_vs_phi_EndCap_H_posZ->SetYTitle("(E_{corr} - E_{true} / E_{true})");
			h_response_vs_phi_EndCap_H_negZ->SetYTitle("(E_{corr} - E_{true} / E_{true})");
			h_response_vs_phi_barrel_H->SetYTitle("(E_{corr} - E_{true} / E_{true})");


			TFile* file=new TFile("output.root","recreate");
			h_response_vs_phi_EndCap_EH_posZ->Write();
			h_response_vs_phi_EndCap_EH_negZ->Write();
			h_response_vs_phi_barrel_EH->Write(); //shuham
			h_response_vs_phi_EndCap_H_posZ->Write();
			h_response_vs_phi_EndCap_H_negZ->Write();
			h_response_vs_phi_barrel_H->Write(); //shuham

			//h_occupancy_correct_response->Write();                                                                                                                                                                 
			file->Close();



			// don't know what these are, may be all inclusive
			//barrelWithEcalHcalCalib->drawCoeffGraph("Alpha","EH");
			//barrelWithEcalHcalCalib->drawCoeffGraph("Beta", "EH");
			//endcapWithHcalCalib->drawCoeffGraph("Gamma", "H");



			// TCanvas *cded = new TCanvas("cefzf","ceced");
			// bcplot->Draw("colz");
			// corrEtaDependenceProf->Draw("colz");


			functionBarrelEcalHcalB_e = functionBarrelEcalHcalB->GetTitle();
			functionBarrelEcalHcalC_e = functionBarrelEcalHcalC->GetTitle();
			functionBarrelHcalC_e = functionBarrelHcalC->GetTitle();
			functionBarrelAlphaEH_e = functionBarrelAlphaEcalHcal->GetTitle();
			functionBarrelBetaEH_e = functionBarrelBetaEcalHcal->GetTitle();

			functionBarrelAlphaH_e = functionBarrelAlphaHcal->GetTitle();
			functionBarrelBetaH_e = functionBarrelBetaHcal->GetTitle();


			functionEndcapEcalHcalB_e = functionEndcapEcalHcalB->GetTitle();
			functionEndcapEcalHcalC_e = functionEndcapEcalHcalC->GetTitle();
			functionEndcapHcalC_e = functionEndcapHcalC->GetTitle();
			functionEndcapAlphaEH_e = functionEndcapAlphaEcalHcal->GetTitle();
			functionEndcapBetaEH_e = functionEndcapBetaEcalHcal->GetTitle();

			functionEndcapAlphaH_e = functionEndcapAlphaHcal->GetTitle();
			functionEndcapBetaH_e = functionEndcapBetaHcal->GetTitle();


			//FUnction printing =============================================
			//takes more place, but easier to read
			//Thresholds first
			cout<<"  threshE = "<<barrelABCEcalHcal[2]->getA()<<";"<<endl;
			cout<<"  threshH = "<<barrelABCHcal[2]->getA()<<";"<<endl; 

			//Now functions : Ecal coef barrel
			cout<<"  faBarrel = new TF1(\"faBarrel\",\""<<
				functionBarrelEcalHcalB_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelEcalHcalB->GetNpar()-1)) break;
				barrelEcalHcalB = functionBarrelEcalHcalB->GetParameter(i);
				cout<<"  faBarrel->SetParameter("<<i<<","<<barrelEcalHcalB<<");"<<endl;
			}
			// Hcal coef barrel for ecalHcal
			cout<<"  fbBarrel = new TF1(\"fbBarrel\",\""<<
				functionBarrelEcalHcalC_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelEcalHcalC->GetNpar()-1)) break;
				barrelEcalHcalC = functionBarrelEcalHcalC->GetParameter(i);
				cout<<"  fbBarrel->SetParameter("<<i<<","<<barrelEcalHcalC<<");"<<endl;
			}
			// Hcal coef barrel for Hcal
			cout<<"  fcBarrel = new TF1(\"fcBarrel\",\""<<
				functionBarrelHcalC_e<<"\",1.,1000.);"<<endl;

			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelHcalC->GetNpar()-1)) break;
				barrelHcalC = functionBarrelHcalC->GetParameter(i);
				cout<<"  fcBarrel->SetParameter("<<i<<","<<barrelHcalC<<");"<<endl;
			}
			//alpha function EcalHcal
			cout<<"  faEtaBarrelEH = new TF1(\"faEtaBarrelEH\",\""<<
				functionBarrelAlphaEH_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelAlphaEcalHcal->GetNpar()-1)) break;
				barrelAlpha = functionBarrelAlphaEcalHcal->GetParameter(i);
				cout<<"  faEtaBarrelEH->SetParameter("<<i<<","<<barrelAlpha<<");"<<endl;
			}
			//beta function EcalHcal
			cout<<"  fbEtaBarrelEH = new TF1(\"fbEtaBarrelEH\",\""<<
				functionBarrelBetaEH_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelBetaEcalHcal->GetNpar()-1)) break;
				barrelBeta = functionBarrelBetaEcalHcal->GetParameter(i);
				cout<<"  fbEtaBarrelEH->SetParameter("<<i<<","<<barrelBeta<<");"<<endl;
			}
			//alpha function Hcal
			cout<<"  faEtaBarrelH = new TF1(\"faEtaBarrelH\",\""<<
				functionBarrelAlphaH_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelAlphaHcal->GetNpar()-1)) break;
				barrelAlpha = functionBarrelAlphaHcal->GetParameter(i);
				cout<<"  faEtaBarrelH->SetParameter("<<i<<","<<barrelAlpha<<");"<<endl;
			}
			//beta function Hcal
			cout<<"  fbEtaBarrelH = new TF1(\"fbEtaBarrelH\",\""<<
				functionBarrelBetaH_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelBetaHcal->GetNpar()-1)) break;
				barrelBeta = functionBarrelBetaHcal->GetParameter(i);
				cout<<"  fbEtaBarrelH->SetParameter("<<i<<","<<barrelBeta<<");"<<endl;
			}


			//Now endcaps (just a copy)
			//Now functions : Ecal coef Endcap
			cout<<"  faEndcap = new TF1(\"faEndcap\",\""<<
				functionEndcapEcalHcalB_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapEcalHcalB->GetNpar()-1)) break;
				endcapEcalHcalB = functionEndcapEcalHcalB->GetParameter(i);
				cout<<"  faEndcap->SetParameter("<<i<<","<<endcapEcalHcalB<<");"<<endl;
			}
			// Hcal coef endcap for ecalHcal
			cout<<"  fbEndcap = new TF1(\"fbEndcap\",\""<<
				functionEndcapEcalHcalC_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapEcalHcalC->GetNpar()-1)) break;
				endcapEcalHcalC = functionEndcapEcalHcalC->GetParameter(i);
				cout<<"  fbEndcap->SetParameter("<<i<<","<<endcapEcalHcalC<<");"<<endl;
			}
			// Hcal coef endcap for Hcal
			cout<<"  fcEndcap = new TF1(\"fcEndcap\",\""<<
				functionEndcapHcalC_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapHcalC->GetNpar()-1)) break;
				endcapHcalC = functionEndcapHcalC->GetParameter(i);
				cout<<"  fcEndcap->SetParameter("<<i<<","<<endcapHcalC<<");"<<endl;
			}
			//alpha function for EcalHcal
			cout<<"  faEtaEndcapEH = new TF1(\"faEtaEndcapEH\",\""<<
				functionEndcapAlphaEH_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapAlphaEcalHcal->GetNpar()-1)) break;
				endcapAlpha = functionEndcapAlphaEcalHcal->GetParameter(i);
				cout<<"  faEtaEndcapEH->SetParameter("<<i<<","<<endcapAlpha<<");"<<endl;
			}
			//beta function for EcalHcal
			cout<<"  fbEtaEndcapEH = new TF1(\"fbEtaEndcapEH\",\""<<
				functionEndcapBetaEH_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapBetaEcalHcal->GetNpar()-1)) break;
				endcapBeta = functionEndcapBetaEcalHcal->GetParameter(i);
				cout<<"  fbEtaEndcapEH->SetParameter("<<i<<","<<endcapBeta<<");"<<endl;
			}
			//alpha function for Hcal
			cout<<"  faEtaEndcapH = new TF1(\"faEtaEndcapH\",\""<<
				functionEndcapAlphaH_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapAlphaHcal->GetNpar()-1)) break;
				endcapAlpha = functionEndcapAlphaHcal->GetParameter(i);
				cout<<"  faEtaEndcapH->SetParameter("<<i<<","<<endcapAlpha<<");"<<endl;
			}
			//beta function for Hcal
			cout<<"  fbEtaEndcapH = new TF1(\"fbEtaEndcapH\",\""<<
				functionEndcapBetaH_e<<"\",1.,1000.);"<<endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapBetaHcal->GetNpar()-1)) break;
				endcapBeta = functionEndcapBetaHcal->GetParameter(i);
				cout<<"  fbEtaEndcapH->SetParameter("<<i<<","<<endcapBeta<<");"<<endl;
			}



			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelEcalHcalB->GetNpar()-1)) break;
				barrelEcalHcalB = functionBarrelEcalHcalB->GetParameter(i);
				cout<<barrelEcalHcalB<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelEcalHcalC->GetNpar()-1)) break;
				barrelEcalHcalC = functionBarrelEcalHcalC->GetParameter(i);
				cout<<barrelEcalHcalC<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelHcalC->GetNpar()-1)) break;
				barrelHcalC = functionBarrelHcalC->GetParameter(i);
				cout<<barrelHcalC<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelAlphaEcalHcal->GetNpar()-1)) break;
				barrelAlpha = functionBarrelAlphaEcalHcal->GetParameter(i);
				cout<<barrelAlpha<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelBetaEcalHcal->GetNpar()-1)) break;
				barrelBeta = functionBarrelBetaEcalHcal->GetParameter(i);
				cout<<barrelBeta<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelAlphaHcal->GetNpar()-1)) break;
				barrelAlpha = functionBarrelAlphaHcal->GetParameter(i);
				cout<<barrelAlpha<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionBarrelBetaHcal->GetNpar()-1)) break;
				barrelBeta = functionBarrelBetaHcal->GetParameter(i);
				cout<<barrelBeta<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapEcalHcalB->GetNpar()-1)) break;
				endcapEcalHcalB = functionEndcapEcalHcalB->GetParameter(i);
				cout<<endcapEcalHcalB<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapEcalHcalC->GetNpar()-1)) break;
				endcapEcalHcalC = functionEndcapEcalHcalC->GetParameter(i);
				cout<<endcapEcalHcalC<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapHcalC->GetNpar()-1)) break;
				endcapHcalC = functionEndcapHcalC->GetParameter(i);
				cout<<endcapHcalC<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapAlphaEcalHcal->GetNpar()-1)) break;
				endcapAlpha = functionEndcapAlphaEcalHcal->GetParameter(i);
				cout<<endcapAlpha<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapBetaEcalHcal->GetNpar()-1)) break;
				endcapBeta = functionEndcapBetaEcalHcal->GetParameter(i);
				cout<<endcapBeta<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapAlphaHcal->GetNpar()-1)) break;
				endcapAlpha = functionEndcapAlphaHcal->GetParameter(i);
				cout<<endcapAlpha<<", ";
			}
			cout << endl;
			for ( int i = 0; i < 10; ++i ) 
			{
				if ( i > (functionEndcapBetaHcal->GetNpar()-1)) break;
				endcapBeta = functionEndcapBetaHcal->GetParameter(i);
				cout<<endcapBeta<<", ";
			}
			cout << endl;



		}

