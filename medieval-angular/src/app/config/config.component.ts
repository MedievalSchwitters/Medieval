import { Component, Input, OnInit } from '@angular/core';


@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.css']
})
export class ConfigComponent implements OnInit {

  constructor() { }

  @Input() maxAge: number = 0;

  @Input() maxNumChildren: number = 0;

  @Input() adultAge: number = 0;

  @Input() elderlyAge: number = 0;

  @Input() playersToAddInput: String = "";

  @Input() deadPlayers: string[] = [];

  @Input() livingPlayers: string[] = [];
  ngOnInit(): void {
  }

  addPlayers(){
    if(!this.playersToAddInput){
      return;
    }
    const playersToAdd = this.playersToAddInput.split(",");
    for(let i = 0; i < playersToAdd.length; i++){
      playersToAdd[i] = playersToAdd[i].trim();
      if(!this.deadPlayers.includes(playersToAdd[i]) && !this.livingPlayers.includes(playersToAdd[i])){
        this.deadPlayers.push(playersToAdd[i]);
      }
    }
    this.playersToAddInput = "";
  }
}
