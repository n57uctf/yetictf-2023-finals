import { Component, OnInit } from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Route, Router, RouterLink, Routes } from '@angular/router';
import { IRegistrationModel, IUserModel, IProjectModel, INewProjectModel, ITaskModel, INewTaskModel, IAddProject } from 'src/app/models/app.models';
import { ApiService } from 'src/app/api.service';
import { InvokeFunctionExpr } from '@angular/compiler';
import { ListKeyManager } from '@angular/cdk/a11y';
import {MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Inject } from '@angular/core';

@Component({
  selector: 'app-create-task-dialog',
  templateUrl: './create-task-dialog.component.html',
  styleUrls: ['./create-task-dialog.component.sass']
})

export class CreateTaskDialogComponent {
  
  private projectId: number;

  constructor(@Inject(MAT_DIALOG_DATA) data: { projectId: number }, 
  public dialog: MatDialog, 
  private apiService: ApiService, 
  private snackBar: MatSnackBar, 
  private router: Router) 
  {
    this.projectId = data.projectId
  }


  addTask(name: string, description: string, responsible: string) {
    this.apiService.addTask(this.projectId,
      {
        name: name,
        description: description,
        responsible: responsible
      }).subscribe(
      {
        next: () => this.snackBar.open('Новый таск добавлен', 'Закрыть'),
        error: (err) => this.snackBar.open('Произошла ошибка', 'Закрыть')
      }
      )
  }
}
