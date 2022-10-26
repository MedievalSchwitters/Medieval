import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class MessageService {
  messages: string[] = [];

  add(message: string) {
    this.messages.push(message);
    if(this.messages.length > 7){
      this.messages.shift();
    }
  }

  clear() {
    this.messages = [];
  }
}
