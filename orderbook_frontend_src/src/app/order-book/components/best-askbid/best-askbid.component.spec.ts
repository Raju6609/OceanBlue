import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BestAskBidComponent } from './best-askbid.component';

describe('BestAskBidComponent', () => {
  let component: BestAskBidComponent;
  let fixture: ComponentFixture<BestAskBidComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BestAskBidComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BestAskBidComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
