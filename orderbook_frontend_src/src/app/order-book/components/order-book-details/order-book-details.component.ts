import {Component, OnDestroy, OnInit} from '@angular/core';
import {OrderService} from '../../services/order.service';
import {Subject} from 'rxjs';
import {Order} from '../../model/order.model';
import {BestAskBid} from '../../model/bestaskbid.model';
import {takeUntil} from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';

export class OrderBook implements Order {
  constructor(public askQty?, public askPrice?, public bidQty?, public bidPrice?) {}
}

export class BestAskBidOrder implements BestAskBid {
  constructor(public bestAsk?, public bestBid?) {}
}


@Component({
  selector: 'app-order-book-details',
  templateUrl: './order-book-details.component.html',
  styleUrls: ['./order-book-details.component.css']
})
export class OrderBookDetailsComponent implements OnInit, OnDestroy {

  displayDialog: boolean;
  displayDetailsDialog: boolean;

  order: Order;
  bestbidask: BestAskBid;


  selectedOrder: Order;
  newOrder: boolean;
  cols: any[];
  orderType: string = 'ask';
  orders: Order[];

  private destroy$: Subject<void> = new Subject<void>();

  constructor(private service: OrderService) { }

  ngOnInit() {
    let resp = this.http.get("http://127.0.0.1:5000/orderbook");
    resp.subscribe((data)=>this.orderbook=data);
  }

  ngOnInit() {
    this.service.getOrders().pipe(takeUntil(this.destroy$)).subscribe((data: Order[]) => this.orders = data);
    this.cols = [
      { field: 'askQty', header: 'Ask Qty' },
      { field: 'askPrice', header: 'Ask Price' },
      { field: 'bidQty', header: 'Bid Qty' },
      { field: 'bidPrice', header: 'Bid Price' }
    ];
  }

  showDialogToAdd() {
    this.newOrder = true;
    this.order = new OrderBook();
    this.displayDialog = true;
  }

  showGetBestAskBid() {
    this.newOrder =false;
    this.bestbidask = new BestAskBidOrder();
    this.displayDialog = true;
  }


  save() {
    const orders = [...this.orders];
    if (this.newOrder) {
      orders.push(this.order);
    } else {
      orders[this.findSelectedOrderIndex()] = this.order;
    }
    this.orders = orders;
    this.order = null;
    this.displayDialog = false;
    this.displayDetailsDialog = false;
  }

  onRowSelect(event) {
    this.newOrder = false;
    this.order = {...event.data};
    this.displayDetailsDialog = true;
  }

  findSelectedOrderIndex(): number {
    return this.orders.indexOf(this.selectedOrder);
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

}
