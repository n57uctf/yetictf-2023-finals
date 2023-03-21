import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-shared-password-page',
  templateUrl: './shared-password-page.component.html',
  styleUrls: ['./shared-password-page.component.sass']
})
export class SharedPasswordPageComponent implements OnInit {

  constructor(private activatedRoute: ActivatedRoute) { }

  ngOnInit(): void {
    this.activatedRoute.params.subscribe(link => {
      console.log(link);
  });
  }

}
