import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { IShareLinkModel, IStorageModel, IUserModel } from 'src/app/_models/app.models';
import { ApiService } from 'src/app/_services/api.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-storage-page',
  templateUrl: './storage-page.component.html',
  styleUrls: ['./storage-page.component.sass']
})
export class StoragePageComponent implements OnInit {

  constructor(private apiService: ApiService, private snackBar: MatSnackBar, private router: Router) { }

  ngOnInit(): void {
    this.getStorageData()
    this.apiService.getUserInfo().subscribe(
      {
        next: (value: IUserModel) => this.user = value,
        error: (err) => this.snackBar.open('Произошла ошибка', 'Закрыть')
      }
    )
  }

  storage: IStorageModel[] = null;
  user: IUserModel = null;

  getStorageData() {
    this.apiService.getPasswords().subscribe(
      {
        next: (value: IStorageModel[]) => {
          this.storage = value
        },
        error: (err) => this.snackBar.open('Произошла ошибка', 'Закрыть')
      }
    )
  }

  logout() {
    localStorage.removeItem('token')
    this.router.navigate(['login'])
  }

  addNewPassword(title: string, password: string) {
    this.apiService.addPassword(
      {
        password: password,
        title: title
      }
    ).subscribe(
      {
        next: (value: IStorageModel) => this.storage.push(value),
        error: (err) => this.snackBar.open('Произошла ошибка', 'Закрыть')
      }
    )
  }

  sharePassword(recordId) {
    this.apiService.sharePassword(recordId).subscribe(
      {
        next: (value: IShareLinkModel) => this.snackBar.open(`Ссылка: ${environment.origin}/shared/${value.link}`, 'Закрыть'),
        error: (err) => this.snackBar.open('Произошла ошибка', 'Закрыть')
      }
    )
  }

}
