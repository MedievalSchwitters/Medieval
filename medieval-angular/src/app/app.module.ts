import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PlayersListComponent } from './players-list/players-list.component';
import {HttpClientModule} from '@angular/common/http';
import { TreeComponent } from './tree/tree.component';
import { GojsAngularModule } from 'gojs-angular';



@NgModule({
  declarations: [
    AppComponent,
    PlayersListComponent,
    TreeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    GojsAngularModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
