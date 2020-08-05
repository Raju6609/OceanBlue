import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Order} from '../model/order.model';
import {BestAskBid} from '../model/bestaskbid.model';

@Injectable({providedIn: 'root'})
export class OrderService {
  constructor(private http: HttpClient) {
  }

  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>('assets/order-book.json');
  }

  getBestAskBids(): Observable<BestAskBid[]> {
    return this.http.get<BestAskBid[]>('assets/best-askbid.json');
  }
}
