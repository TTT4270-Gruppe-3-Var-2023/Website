//Henter tilstandsrapport for alle toaletter.
toiletLocationsStatus(){
  vector<Status> statusAllLocations = {
    toiletLocation1(),
    toiletLocation2(),
    toiletLocation3()
    }
  return statusAllLocations;
}

//Tilstandsrapportene må kunne oppdateres hyppig.

//Tilstandsrapport lokasjon1
toiletLocation1(){
  //Returnerer køstatus.
}

//Tilstandsrapport lokasjon2
toiletLocation2(){
  //Returnerer køstatus.
}

//Tilstandsrapport lokasjon3
toiletLocation3(){
  //Returnerer køstatus.
}

class StatusByCategory{
private:
  Color s;
  double waitingMinutes;
  string category;
public:
  Status(double wm, string c):waitingMinutes{wm},category{c},s{}{
    if()//kalkulerer hvilken fargestatus som tilhører objektet utifra hvor lang ventetiden er.
      c = Color::green || Color::yellow || Color::red; //Grønn->Ledige plasser, Gul->Kort ventetid, -> Rød->Lang ventetid   
  }
  //Må inneholde set-funksjoner som oppdaterer tilstandene til objektet.
  //Må inneholde get-funksjoner.
};
