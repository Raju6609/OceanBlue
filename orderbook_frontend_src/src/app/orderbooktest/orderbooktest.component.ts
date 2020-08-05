import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-orderbooktest',
  templateUrl: './orderbooktest.component.html',
  styleUrls: ['./orderbooktest.component.css']
})
export class OrderbooktestComponent implements OnInit {

  orderbook : any;

  constructor(private http:HttpClient) { }

  ngOnInit() {
    let resp = this.http.get("http://127.0.0.1:5000/orderbook");
    resp.subscribe((data)=>this.orderbook=data);
  }

}
