import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Route, Router, RouterLink, Routes } from '@angular/router';
import { IRegisteredUsersModel, IUserModel } from 'src/app/_models/app.models';
import { ApiService } from 'src/app/_services/api.service';

@Component({
  selector: 'app-register-page',
  templateUrl: './register-page.component.html',
  styleUrls: ['./register-page.component.sass']
})
export class RegisterPageComponent implements OnInit {

  constructor(private apiService: ApiService, private snackBar: MatSnackBar, private router: Router) { }

  registeredUsers: IRegisteredUsersModel[] = null

  ngOnInit(): void {
    this.apiService.getLastUsers().subscribe(
      {
        next: (value: IRegisteredUsersModel[]) => this.registeredUsers = value,
        error: (err) => this.snackBar.open('Произошла ошибка', 'Закрыть')
      }
    )
  }

  register(username: string, password1: string, password2: string) {
    if (password1 != password2) {
      return
    }
    this.apiService.register(
      {
        username: username,
        password: password1
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
