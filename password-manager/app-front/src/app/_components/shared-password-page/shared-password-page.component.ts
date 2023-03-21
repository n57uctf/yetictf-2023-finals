import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute } from '@angular/router';
import { ICreateStorageModel } from 'src/app/_models/app.models';
import { ApiService } from 'src/app/_services/api.service';

@Component({
  selector: 'app-shared-password-page',
  templateUrl: './shared-password-page.component.html',
  styleUrls: ['./shared-password-page.component.sass']
})
export class SharedPasswordPageComponent implements OnInit {

  constructor(private activatedRoute: ActivatedRoute, private apiService: ApiService, private snackBar: MatSnackBar) { }

  sharedPassword: ICreateStorageModel = null

  ngOnInit(): void {
    this.activatedRoute.params.subscribe(
      {
        next: (value) => {
          console.log(value)
          this.apiService.getSharedPassword(value["link"]).subscribe(
            {
              next: (value: ICreateStorageModel) => this.sharedPassword = value,
              error: (err) => this.snackBar.open('Произошла ошибка', 'Закрыть')
            }
          )
        }
      }
  );
  }

}
