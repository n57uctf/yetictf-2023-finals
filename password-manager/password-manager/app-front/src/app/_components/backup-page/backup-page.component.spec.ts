import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BackupPageComponent } from './backup-page.component';

describe('BackupPageComponent', () => {
  let component: BackupPageComponent;
  let fixture: ComponentFixture<BackupPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BackupPageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BackupPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
