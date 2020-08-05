import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { BestAskBidComponent } from './order-book/components/best-askbid/best-askbid.component';
import { OrderBookPageComponent } from './order-book/components/order-book-page/order-book-page.component';
import { OrderBookDetailsComponent } from './order-book/components/order-book-details/order-book-details.component';
import {CommonModule} from '@angular/common';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {ButtonModule, DialogModule, InputTextModule, MessageModule, RadioButtonModule, TableModule} from 'primeng';
import { OrderbooktestComponent } from './orderbooktest/orderbooktest.component';

@NgModule({
  declarations: [
    AppComponent,
    OrderBookPageComponent,
    OrderBookDetailsComponent,
    BestAskBidComponent,
    OrderbooktestComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    TableModule,
    HttpClientModule,
    InputTextModule,
    DialogModule,
    ButtonModule,
    RadioButtonModule,
    MessageModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
