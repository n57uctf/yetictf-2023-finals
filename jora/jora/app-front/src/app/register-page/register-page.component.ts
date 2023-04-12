import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Route, Router, RouterLink, Routes } from '@angular/router';
import { IRegistrationModel, IUserModel } from 'src/app/models/app.models';
import { ApiService } from 'src/app/api.service';
import { InvokeFunctionExpr } from '@angular/compiler';

@Component({
  selector: 'app-register-page',
  templateUrl: './register-page.component.html',
  styleUrls: ['./register-page.component.sass']
})
export class RegisterPageComponent {

  constructor(private apiService: ApiService, private snackBar: MatSnackBar, private router: Router) { }


  register(username: string, password1: string, password2: string, info: string) {
    if (password1 != password2) {
      return
    }
    this.apiService.register(
      {
        username: username,
        password: password1,
        info: info,
      }
    ).subscribe(
      {
        next: (value: IUserModel) => {
          this.router.navigate(['login'])
        },
        error: (err) => {
          this.snackBar.open('Произошла ошибка', 'Закрыть')
        }
      }
    )
  }
}
