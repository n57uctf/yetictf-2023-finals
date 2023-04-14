import { Component, OnInit } from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {CreateTaskDialogComponent} from "../create-task-dialog/create-task-dialog.component";
import { MatSnackBar } from '@angular/material/snack-bar';
import { Route, Router, RouterLink, Routes } from '@angular/router';
import { IRegistrationModel, IUserModel, IProjectModel, INewProjectModel, ITaskModel, INewTaskModel, IAddProject } from 'src/app/models/app.models';
import { ApiService } from 'src/app/api.service';
import { InvokeFunctionExpr } from '@angular/compiler';
import { ListKeyManager } from '@angular/cdk/a11y';


@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.sass']
})
export class MainPageComponent implements OnInit {

  constructor(public dialog: MatDialog, private apiService: ApiService, private snackBar: MatSnackBar, private router: Router) {}


  projects_data: IProjectModel[] = [];
  fileName = '';
  user: IUserModel = null;


  ngOnInit(): void {
    this.getProjects()
    this.apiService.getUserInfo().subscribe(
      {
        next: (value: IUserModel) => this.user = value,
        error: (err) => this.snackBar.open('Произошла ошибка', 'Закрыть')
      }
    )
  }

  getProjects() {
    this.apiService.getProjects().subscribe(
      {
        next: (value: IProjectModel[]) => {this.projects_data=value}
      }
    )
  }

  addProject(users: string[], project_name: string, project_desc: string) {
    this.apiService.addProject(
      {
        users: users,
        new_project_data: {
          name: project_name,
          description: project_desc
        }
      }
    ).subscribe(
      {
        next: (value: IProjectModel) =>{ this.getProjects(); this.snackBar.open('Новый проект добавлен', 'Закрыть')},
        error: (err) => this.snackBar.open('Произошла ошибка', 'Закрыть')
      }
    )
  }

  openDialog(project_id: number) {
    this.dialog.open(CreateTaskDialogComponent, {data: { projectId: project_id}});
  }


  downloadFile(data: any) {
    const blob = new Blob([data], { type: 'text/text' });
    const url= window.URL.createObjectURL(blob);
    window.open(url);
  }

  getFile(project_id: number) {
    this.apiService.getReport(project_id).subscribe({next: (value) => this.downloadFile(value)} )

  }

  getAttach(text: string) {
    this.apiService.getAttachment(text).subscribe({next: (value) => this.downloadFile(value)} )

  }

  onFileSelected(task_id, event) {
    const file:File = event.target.files[0];
    if (file) {
        this.fileName = file.name;
        const formData = new FormData();
        formData.append("file", file);
        this.apiService.uploadAttachmnet(task_id, formData).subscribe({ next: () => {} })
    }
}


}


