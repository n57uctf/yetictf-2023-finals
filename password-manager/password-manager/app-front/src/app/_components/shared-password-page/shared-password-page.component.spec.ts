import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SharedPasswordPageComponent } from './shared-password-page.component';

describe('SharedPasswordPageComponent', () => {
  let component: SharedPasswordPageComponent;
  let fixture: ComponentFixture<SharedPasswordPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SharedPasswordPageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SharedPasswordPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
