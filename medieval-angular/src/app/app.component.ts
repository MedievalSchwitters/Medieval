import { HttpClient } from '@angular/common/http';
import { AfterViewInit, Component, ElementRef, Injectable, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
import * as go from 'gojs';
import { Person } from './person';
import { MessageService as Chronicle } from './message.service';
import { MessageService } from 'primeng/api';
import { waitForAsync } from '@angular/core/testing';






@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [MessageService]
})
export class AppComponent implements OnChanges{
  title = 'medieval-angular';

  public model: go.TreeModel = new go.TreeModel([]);
  turn = 1;
  deadPlayers: string[] = [];
  livingPlayers: string[] = [];
  playerIncarnations: Map<string, number> = new Map();
  people: Person[] = [];
  playersAddedByCSV = false;
  paused: boolean = false;
  protosAnthropos: Person | null = null;
  eligableProgenitors: Person[] = []; //represents the fertile people who have not yet had a child during this pause
  livingPeople: Person[] = [];
  personKey = 1; //assigned to people to uniqely identify them, used in tree
  playersToAddInput: String = "";

  //config stuff
  maxAge = 10;
  maxNumChildren = 2;
  adultAge = 3;
  elderlyAge = 7;
  @ViewChild("scrollButton") scrollButton: ElementRef | null = null;
  constructor(private http: HttpClient, private chronicle: Chronicle, private messageService: MessageService) { }

  addPlayersByCSV(): void {
    this.http.get('assets/player_list.csv', { responseType: 'text' }) //apparently JSON expected by defauly, so hardcode response type
      .subscribe(data => this.deadPlayers = data.split(','));
    this.playersAddedByCSV = true;
  }

  alivifyPlayer(player: string): void {
    if (!this.protosAnthropos) {
      let incarnation = this.intToRoman(this.getIncarnation(player)!);
      this.chronicle.add(player + " " + incarnation + " was created ex nihilo.");
      this.people = [];
      this.protosAnthropos = new Person(this.personKey++, player);
      this.addNode(this.protosAnthropos.key, this.protosAnthropos.name + " " + incarnation, 0);
      this.people.push(this.protosAnthropos);
      this.deadPlayers = this.deadPlayers.filter(name => name !== player);
      this.livingPlayers.push(player);
      this.livingPeople.push(this.protosAnthropos);
      return;
    }
    if (this.eligableProgenitors.length) {
      let progenitor = this.eligableProgenitors.pop();
      let child = new Person(this.personKey++, player);
      progenitor!.children++;
      let childIncarnation = this.intToRoman(this.getIncarnation(child.name)!);
      let progenitorIncarnation = this.intToRoman(this.getIncarnation(progenitor!.name)!);
      this.chronicle.add(child.name + " " + childIncarnation + " was born to " + progenitor!.name + " " + progenitorIncarnation);
      this.people.push(child);
      this.livingPeople.push(child);
      this.deadPlayers = this.deadPlayers.filter(name => name !== player);
      this.livingPlayers.push(player);
      this.addNode(child.key, child.name + " " + childIncarnation, progenitor!.key);
    }
    else {
      this.messageService.add({ key: "br", severity: 'info', summary: 'Info', detail: 'No More Eligible Progenitors This Turn' });
    }
  }

  killPlayer(player: string): void {
    this.livingPlayers = this.livingPlayers.filter(name => name !== player);
    this.deadPlayers.push(player);
    let person = this.getPersonByName(player);
    if (person) { //pretty sure I'm only doing this to make the compiler happy
      person.alive = false;
      const node = this.model.findNodeDataForKey(person.key);
      this.model.startTransaction();
      this.model.set(node!, 'color', "red");
      this.model.commitTransaction();
      this.chronicle.add(person.name + " " + this.intToRoman(this.getIncarnation(player)!) + " died at the age of " + person.age);

      this.incrementIncarnation(player);
      if (this.eligableProgenitors.includes(person)){
        this.eligableProgenitors.splice(this.eligableProgenitors.indexOf(person));
      }
    }
    this.livingPeople = this.livingPeople.filter(person => person.name !== player);
  }

  updateFerility() {
    this.people.forEach(person => {
      if (this.adultAge <= person.age && person.age < this.elderlyAge &&
        person.alive && person.children < this.maxNumChildren) {
        person.fertile = true;
      } else {
        person.fertile = false;
      }
    });
  }

  nextTurn() {
    //this.messages.clear();
    if (!this.protosAnthropos) {
      this.messageService.add({ key: "br", severity: 'info', detail: "The Game has not yet begun. Create a Person." });
      return;
    }
    for (let index = 0; index < this.livingPeople.length; index++) {
      const person = this.livingPeople[index];
      if (person.age >= this.maxAge) {
        this.messageService.add({ key: "br", severity: 'error', detail: person.name + "'s time has come. Kill them to proceed." });
        return;
      }
    };
    this.chronicle.add("TURN " + this.turn);
    this.turn++;
    this.people.forEach(person => {
      person.age++;
    });
    this.updateFerility();
    this.updateEligableProgenitors();
    //this.scrollDown();
  }

  getPersonByName(name: string): Person | null {
    for (let i = 0; i < this.livingPeople.length; i++) {
      if (this.livingPeople[i].name === name) {
        return this.livingPeople[i]
      }
    }
    return null;
  }

  addNode(key: number, name: string, parentKey: number) {
    this.model.startTransaction();
    this.model.addNodeData({ 'key': key, 'name': name, 'parent': parentKey, 'color': 'green' })
    this.model.commitTransaction();
  }

  updateMaxAge(newMaxAge: number) {
    this.maxAge = newMaxAge;
  }

  updateMaxNumChildren(newMaxNumChildren: number) {
    this.maxNumChildren = newMaxNumChildren;
  }

  updateAdultAge(newAdultAge: number) {
    this.adultAge = newAdultAge;
  }

  updateElderlyAge(newElderlyAge: number) {
    this.elderlyAge = newElderlyAge;
  }

  getIncarnation(player: string) {
    if (!this.playerIncarnations.get(player)) {
      this.playerIncarnations.set(player, 1);
      return 1;
    }
    else {
      return this.playerIncarnations.get(player);
    }
  }

  incrementIncarnation(player: string) {
    this.playerIncarnations.set(player, this.playerIncarnations.get(player)! + 1);
  }

  updateEligableProgenitors() {
    this.eligableProgenitors = [];
    this.people.forEach(person => {
      if (person.fertile) {
        this.eligableProgenitors.push(person);
      }
    });
    this.eligableProgenitors.sort(() => Math.random() - 0.5);
  }

  intToRoman(num: number) {
    const rules = new Map([
      ["M", 1000],
      ["CM", 900],
      ["D", 500],
      ["CD", 400],
      ["C", 100],
      ["XC", 90],
      ["L", 50],
      ["XL", 40],
      ["XXX", 30],
      ["XX", 20],
      ["X", 10],
      ["IX", 9],
      ["V", 5],
      ["IV", 4],
      ["I", 1]
    ])
    let res = "";
    const romans = Array.from(rules.keys());
    for (let i = 0; i < romans.length; ++i) {
      const val = rules.get(romans[i]);
      while (num >= val!) {
        num -= val!;
        res += romans[i];
      }
    }
    return res;
  };

  ngOnChanges(changes: SimpleChanges): void {
    this.scrollDown();
  }
  scrollDown(){
    setTimeout(() => {this.scrollButton?.nativeElement.click();}, 500);
  }

}
