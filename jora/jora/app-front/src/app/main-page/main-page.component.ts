import { Component } from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {CreateTaskDialogComponent} from "../create-task-dialog/create-task-dialog.component";
import {SearchTaskComponent} from "../search-task/search-task.component";

export interface Tile {
  color: string;
  cols: number;
  rows: number;
  text: string;
}


@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.sass']
})
export class MainPageComponent {

  tiles: Tile[] = [
    {text: '#', cols: 1, rows: 1, color: '#7c84ff'},
    {text: 'Name', cols: 3, rows: 1, color: '#7c84ff'},
    {text: 'Description', cols: 4, rows: 1, color: '#7c84ff'},
    {text: 'Attachments', cols: 3, rows: 1, color: '#7c84ff'},
    {text: 'Responsible', cols: 2, rows: 1, color: '#7c84ff'},
    {text: '1', cols: 1, rows: 1, color: '#d1ccff'},
    {text: 'First Task', cols: 3, rows: 1, color: '#d1ccff'},
    {text: 'My first task is', cols: 4, rows: 1, color: '#d1ccff'},
    {text: '-', cols: 3, rows: 1, color: '#d1ccff'},
    {text: 'diana', cols: 2, rows: 1, color: '#d1ccff'},
  ];

  constructor(public dialog: MatDialog) {
  }

  openDialog() {
    this.dialog.open(CreateTaskDialogComponent);
  }


}


