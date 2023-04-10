import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Route, Router, RouterLink, Routes } from '@angular/router';
import { IAddProject, IRegistrationModel, IUserModel } from 'src/app/models/app.models';
import { ApiService } from 'src/app/api.service';
import { InvokeFunctionExpr } from '@angular/compiler';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.sass']
})
export class LoginPageComponent {
  constructor(private apiService: ApiService, private snackBar: MatSnackBar, private router: Router) { }

  ngOnInit(): void {
  }

  login(username: string, password: string) {
    this.apiService.autheticate(
      {
        username: username,
        password: password
      }
    )
  }
}
