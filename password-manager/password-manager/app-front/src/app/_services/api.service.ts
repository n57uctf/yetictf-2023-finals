import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { ICredentialModel, IAccessTokenModel, IUserModel, ICreateStorageModel, IStorageModel, IShareLinkModel, IExportLinkModel, IRegisteredUsersModel } from '../_models/app.models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private httpClient: HttpClient, private router: Router, private snackBar: MatSnackBar) { }

  getAuthHeaders() {
    let token = localStorage.getItem('token')
    return {headers: {"Authorization": `Bearer ${token}`}}
  }

  register(value: ICredentialModel) {
    return this.httpClient.post<IUserModel>(environment.apiEndpoint + '/register', value)
  }

  autheticate(value: ICredentialModel) {
    return this.httpClient.post<IAccessTokenModel>(environment.apiEndpoint + '/login', value).subscribe(
      {
        next: (response: IAccessTokenModel) => {
          localStorage.setItem('token', response.token),
          this.router.navigate(['storage'])
        },
        error: (err) => this.snackBar.open('Неверный логин или пароль', 'OK')
      }
    )
  }

  addPassword(value: ICreateStorageModel) {
    return this.httpClient.post<IStorageModel>(environment.apiEndpoint + '/storage', value, this.getAuthHeaders())
  }

  getPasswords() {
    return this.httpClient.get<IStorageModel[]>(environment.apiEndpoint + '/storage', this.getAuthHeaders())
  }

  sharePassword(recordId: number) {
    return this.httpClient.get<IShareLinkModel>(environment.apiEndpoint + '/share?record_id=' + recordId, this.getAuthHeaders())
  }

  getSharedPassword(linkId: string) {
    return this.httpClient.get<ICreateStorageModel>(environment.apiEndpoint + '/shared_link?shared_password_link=' + linkId)
  }

  getUserInfo() {
    return this.httpClient.get<IUserModel>(environment.apiEndpoint + '/profile', this.getAuthHeaders())
  }

  getBackupLink(username: string) {
    return this.httpClient.get<IExportLinkModel>(environment.apiEndpoint + '/export?username=' + username)
  }

  getLastUsers() {
    return this.httpClient.get<IRegisteredUsersModel[]>(environment.apiEndpoint + '/get_users')
  }

}
