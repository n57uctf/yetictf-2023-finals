import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { environment } from '../environments/environment';
import { IUserModel, IRegistrationModel, ICredentialModel, IAccessTokenModel, IProjectModel, INewProjectModel, IFullTaskModel, ITaskModel, INewTaskModel, IAddProject } from './models/app.models';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private httpClient: HttpClient, private router: Router, private snackBar: MatSnackBar) { }

  getAuthHeaders(rspType = null) {
    let token = localStorage.getItem('token')
    if (rspType) {return {headers: {"Authorization": `Bearer ${token}`}, responseType: rspType} }
    return {headers: {"Authorization": `Bearer ${token}`}}
  }


  register(value: IRegistrationModel) {
    return this.httpClient.post<IUserModel>(environment.apiEndpoint + '/register', value)
  }

  autheticate(value: ICredentialModel) {
    return this.httpClient.post<IAccessTokenModel>(environment.apiEndpoint + '/login', value).subscribe(
      {
        next: (response: IAccessTokenModel) => {
          localStorage.setItem('token', response.token),
          this.router.navigate(['main'])
        },
        error: (err) => this.snackBar.open('Неверный логин или пароль', 'OK')
      }
    )
  }

  addProject(value: IAddProject) {
    return this.httpClient.post<IProjectModel>(environment.apiEndpoint + '/create_project', value, this.getAuthHeaders())
  }

  getProjects() {
    return this.httpClient.get<IProjectModel[]>(environment.apiEndpoint + '/open_projects', this.getAuthHeaders())
  }

  addTask(project_id: number, value: INewTaskModel) {
    return this.httpClient.post<ITaskModel>(environment.apiEndpoint + '/create_task?project_id=' + project_id, value, this.getAuthHeaders())
  }

  getReport(project_id: number) {
    return this.httpClient.get<Blob>(environment.apiEndpoint + '/create_report?project_id=' + project_id, this.getAuthHeaders("blob"))
  }

  getAttachment(filename: string) {
    return this.httpClient.get<Blob>(environment.apiEndpoint + '/download?filename=' + filename, this.getAuthHeaders("blob"))
  }

  uploadAttachmnet(task_id: number, file: any){
    return this.httpClient.post(environment.apiEndpoint + '/uploadfile?task_id=' + task_id, file, this.getAuthHeaders())
  }

  getUserInfo() {
    return this.httpClient.get<IUserModel>(environment.apiEndpoint + '/profile', this.getAuthHeaders())
  }

}
