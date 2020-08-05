import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OrderbooktestComponent } from './orderbooktest.component';

describe('OrderbooktestComponent', () => {
  let component: OrderbooktestComponent;
  let fixture: ComponentFixture<OrderbooktestComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OrderbooktestComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrderbooktestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
