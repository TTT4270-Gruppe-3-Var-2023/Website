//Henter tilstandsrapport for alle toaletter.
barLocationsStatus(){
  vector<Status> statusAllLocations = {
    barLocation1(),
    barLocation2(),
    barLocation3()
    }
  return statusAllLocations;
}

//Tilstandsrapportene må kunne oppdateres hyppig.

//Tilstandsrapport lokasjon1
barLocation1(){
  //Returnerer køstatus.
}

//Tilstandsrapport lokasjon2
barLocation2(){
  //Returnerer køstatus.
}

//Tilstandsrapport lokasjon3
barLocation3(){
  //Returnerer køstatus.
}

class Status{
private:
  Color s;
  double waitingMinutes;
  //string category;
public:
  Status(double wm, string c):waitingMinutes{wm},category{c},s{}{
    if()//kalkulerer hvilken fargestatus som tilhører objektet utifra hvor lang ventetiden er.
      c = Color::green || Color::yellow || Color::red; //Grønn->Ledige plasser, Gul->Kort ventetid, -> Rød->Lang ventetid   
  }
  //Må inneholde set-funksjoner som oppdaterer tilstandene til objektet.
  //Må inneholde get-funksjoner.
};
