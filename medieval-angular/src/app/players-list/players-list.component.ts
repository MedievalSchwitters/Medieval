import { Component, OnInit } from '@angular/core';
import { Players } from '../player';
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
  playersAddedByCSV = false;
  paused: boolean = false;
  protosAnthropos: Person|null = null;
  

  constructor(private http: HttpClient) { }

  addPlayersByCSV(): void{
    console.log("addPlayersByCSV");
    this.http.get('assets/player_list.csv', {responseType: 'text'}) //apparently JSON expected by defauly, so hardcode response type
    .subscribe(data => this.deadPlayers = data.split(','));
    this.playersAddedByCSV = true;
  }

  alivifyPlayer(player: string): void{
    this.deadPlayers = this.deadPlayers.filter(name => name !== player);
    this.livingPlayers.push(player);
  }

  killPlayer(player: string): void{
    this.livingPlayers = this.livingPlayers.filter(name => name !== player);
    this.deadPlayers.push(player);
  }

  updateFerility(people: Person[]){
    people.forEach(person => {
      
    });
  }

  iterateTime(){
    this.paused = !this.paused;

  }
  
  ngOnInit(): void {
  }

}
