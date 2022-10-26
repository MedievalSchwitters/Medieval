import { HttpClient } from '@angular/common/http';
import { Component, Injectable } from '@angular/core';
import * as go from 'gojs';
import { Person } from './person';
import { FormBuilder } from '@angular/forms';
import { MessageService } from './message.service';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'medieval-angular';

  public model: go.TreeModel = new go.TreeModel(
    [
      // { 'key': 1, 'name': 'Stella Payne Diaz', 'title': 'CEO' },
      // { 'key': 2, 'name': 'Luke Warm', 'title': 'VP Marketing/Sales', 'parent': 1 },
      // { 'key': 3, 'name': 'Meg Meehan Hoffa', 'title': 'Sales', 'parent': 2 },
      // { 'key': 4, 'name': 'Peggy Flaming', 'title': 'VP Engineering', 'parent': 1 },
      // { 'key': 5, 'name': 'Saul Wellingood', 'title': 'Manufacturing', 'parent': 4 },
      // { 'key': 6, 'name': 'Al Ligori', 'title': 'Marketing', 'parent': 2 },
      // { 'key': 7, 'name': 'Dot Stubadd', 'title': 'Sales Rep', 'parent': 3 },
      // { 'key': 8, 'name': 'Les Ismore', 'title': 'Project Mgr', 'parent': 5 },
      // { 'key': 9, 'name': 'April Lynn Parris', 'title': 'Events Mgr', 'parent': 6 },
      // { 'key': 10, 'name': 'Xavier Breath', 'title': 'Engineering', 'parent': 4 },
      // { 'key': 11, 'name': 'Anita Hammer', 'title': 'Process', 'parent': 5 },
      // { 'key': 12, 'name': 'Billy Aiken', 'title': 'Software', 'parent': 10 },
      // { 'key': 13, 'name': 'Stan Wellback', 'title': 'Testing', 'parent': 10 },
      // { 'key': 14, 'name': 'Marge Innovera', 'title': 'Hardware', 'parent': 10 },
      // { 'key': 15, 'name': 'Evan Elpus', 'title': 'Quality', 'parent': 5 },
      // { 'key': 16, 'name': 'Lotta B. Essen', 'title': 'Sales Rep', 'parent': 3 }
    ]
  );
  deadPlayers: string[] = [];
  livingPlayers: string[] = [];
  people: Person[] = [];
  playersAddedByCSV = false;
  paused: boolean = false;
  protosAnthropos: Person|null = null;
  eligableProgenitors: Person[] = []; //represents the fertile people who have not yet had a child during this pause
  livingPeople: Person[] = [];
  personKey = 1; //assigned to people to uniqely identify them, used in tree
  playersToAddInput: String = "";

  //config stuff
  maxAge = 10;
  maxNumChildren = 2;
  adultAge = 3;
  elderlyAge = 7;
  
  constructor( private http: HttpClient, private messages: MessageService ) { }

  addPlayersByCSV(): void{
    this.http.get('assets/player_list.csv', {responseType: 'text'}) //apparently JSON expected by defauly, so hardcode response type
    .subscribe(data => this.deadPlayers = data.split(','));
    this.playersAddedByCSV = true;
  }

  alivifyPlayer(player: string): void{
    if (!this.protosAnthropos){
      this.messages.add(player + " created ex nihilo; may they not eat any forbidden fruits...");
      this.people = [];
      this.protosAnthropos = new Person(this.personKey++, player);
      this.addNode(this.protosAnthropos.key, this.protosAnthropos.name, 0);
      this.people.push(this.protosAnthropos);
      this.deadPlayers = this.deadPlayers.filter(name => name !== player);
      this.livingPlayers.push(player);
      this.livingPeople.push(this.protosAnthropos);
      return;
    }
    if(this.eligableProgenitors.length){
      let progenitor = this.eligableProgenitors.pop();
      let child = new Person(this.personKey++, player);
      progenitor!.children++;
      this.messages.add(child.name + " has been born to " + progenitor!.name);
      this.people.push(child);
      this.livingPeople.push(child);
      this.deadPlayers = this.deadPlayers.filter(name => name !== player);
      this.livingPlayers.push(player);
      this.addNode(child.key, child.name, progenitor!.key);
    }
    else{
      this.messages.add("no more eligable progenitors this round");
    }
  }

  killPlayer(player: string): void{
    this.livingPlayers = this.livingPlayers.filter(name => name !== player);
    this.deadPlayers.push(player);
    let person = this.getPersonByName(player);
    if(person){
      person.alive = false;
      const node = this.model.findNodeDataForKey(person.key);
      this.model.startTransaction();
      this.model.set(node!, 'color', "red");
      this.model.commitTransaction();
    }
    this.livingPeople = this.livingPeople.filter(person => person.name !== player);
  }

  updateFerility(){
    this.people.forEach(person => {
      if (this.adultAge <= person.age && person.age < this.elderlyAge && 
        person.alive && person.children <= this.maxNumChildren){
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
      this.messages.clear();
      this.livingPeople.forEach(person => {
        if(person.age > this.maxAge){
          this.messages.add(person.name + "'s time has come. Kill them to proceed.")
          return;
        }
      });
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

  addNode(key: number, name: string, parentKey: number){
    this.model.startTransaction();
    this.model.addNodeData({'key': key, 'name': name, 'parent': parentKey, 'color': 'green'})
    this.model.commitTransaction();
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
