import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.css']
})
export class ConfigComponent implements OnInit {

  constructor() { }

  @Output() maxAgeEvent = new EventEmitter<number>;

  @Input() maxAge: number = 10;

  @Output() maxNumChildrenEvent = new EventEmitter<number>;

  @Input() maxNumChildren: number = 2;

  @Output() adultAgeEvent = new EventEmitter<number>;

  @Input() adultAge: number = 3;

  @Output() elderlyAgeEvent = new EventEmitter<number>;

  @Input() elderlyAge: number = 7;

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
      if(!this.deadPlayers.includes(playersToAdd[i]) && !this.livingPlayers.includes(playersToAdd[i]) && playersToAdd[i].length < 19){
        this.deadPlayers.push(playersToAdd[i]);
      }
    }
    this.playersToAddInput = "";
  }

  emitMaxAge(){
    this.maxAgeEvent.emit(this.maxAge);
  }

  emitMaxNumChildren(){
    this.maxNumChildrenEvent.emit(this.maxNumChildren);
  }

  emitAdultAge(){
    this.adultAgeEvent.emit(this.adultAge);
  }

  emitElderlyAge(){
    this.elderlyAgeEvent.emit(this.elderlyAge);
  }

}
