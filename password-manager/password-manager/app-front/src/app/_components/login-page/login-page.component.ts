import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/_services/api.service';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.sass']
})
export class LoginPageComponent implements OnInit {

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
