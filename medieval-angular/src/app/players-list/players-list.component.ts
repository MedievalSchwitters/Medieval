import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Person } from '../person';

@Component({
  selector: 'app-players-list',
  templateUrl: './players-list.component.html',
  styleUrls: ['./players-list.component.css']
})
export class PlayersListComponent implements OnInit {
  deadPlayers: string[] = [];
  livingPlayers: string[] = [];
  people: Person[] = [];
  playersAddedByCSV = false;
  paused: boolean = false;
  protosAnthropos: Person|null = null;
  eligableProgenitors: Person[] = []; //represents the fertile people who have not yet had a child during this pause
  livingPeople: Person[] = [];

  //config stuff
  maxAge = 10;
  maxNumChildren = 2;
  adultAge = 3;
  elderlyAge = 7;
  
  constructor(private http: HttpClient) { }

  addPlayersByCSV(): void{
    console.log("addPlayersByCSV");
    this.http.get('assets/player_list.csv', {responseType: 'text'}) //apparently JSON expected by defauly, so hardcode response type
    .subscribe(data => this.deadPlayers = data.split(','));
    this.playersAddedByCSV = true;
  }

  alivifyPlayer(player: string): void{
    if (!this.protosAnthropos){
      console.log(player + " created ex nihlo; may they not eat any forbidden fruits...");
      this.people = [];
      this.protosAnthropos = new Person(player);
      this.people.push(this.protosAnthropos);
      this.deadPlayers = this.deadPlayers.filter(name => name !== player);
      this.livingPlayers.push(player);
      this.livingPeople.push(this.protosAnthropos);
      return;
    }
    if(this.eligableProgenitors.length){
      let progenitor = this.eligableProgenitors.pop();
      let child = new Person(player);
      progenitor?.children.push(child);
      console.log(child.name + " has been born to " + progenitor?.name);
      this.people.push(child);
      this.livingPeople.push(child);
      this.deadPlayers = this.deadPlayers.filter(name => name !== player);
      this.livingPlayers.push(player);
    }
    else{
      console.log("no more eligable progenitors this round");
    }
  }

  killPlayer(player: string): void{
    this.livingPlayers = this.livingPlayers.filter(name => name !== player);
    this.deadPlayers.push(player);
    this.livingPeople = this.livingPeople.filter(person => person.name !== player);
  }

  updateFerility(){
    this.people.forEach(person => {
      if (this.adultAge <= person.age && person.age < this.elderlyAge && 
        person.alive && person.children.length <= this.maxNumChildren){
        person.fertile = true;
      } else {
        person.fertile = false;
      }
    });
  }

  pauseButton(){
    if(this.paused){
      this.paused = !this.paused;
    }
    else{
      this.people.forEach(person => {
        person.age++;
      });
      this.updateFerility();
      this.eligableProgenitors = [];
      this.people.forEach(person => {
        if(person.fertile){
          this.eligableProgenitors.push(person);
        }
      });
      this.eligableProgenitors.sort(() => Math.random() - 0.5);
      this.paused = !this.paused;
    }
  }

  getPersonByName(name: string): Person | null{
    for(let i = 0; i < this.livingPeople.length; i++){
      if(this.livingPeople[i].name === name){
        return this.livingPeople[i]
      }
    }
    return null;
  }
  
  ngOnInit(): void {
  }

}
