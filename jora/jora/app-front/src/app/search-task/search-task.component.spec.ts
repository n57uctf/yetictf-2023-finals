import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchTaskComponent } from './search-task.component';

describe('SearchTaskComponent', () => {
  let component: SearchTaskComponent;
  let fixture: ComponentFixture<SearchTaskComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SearchTaskComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SearchTaskComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
