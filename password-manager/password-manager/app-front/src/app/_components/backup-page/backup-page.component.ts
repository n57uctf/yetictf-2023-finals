import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { IExportLinkModel } from 'src/app/_models/app.models';
import { ApiService } from 'src/app/_services/api.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-backup-page',
  templateUrl: './backup-page.component.html',
  styleUrls: ['./backup-page.component.sass']
})
export class BackupPageComponent implements OnInit {

  constructor(private apiService: ApiService, private snackBar: MatSnackBar) { }

  ngOnInit(): void {
  }

  getBackup(username: string) {
    this.apiService.getBackupLink(username).subscribe(
      {
        next: (value: IExportLinkModel) => this.snackBar.open(`Ссылка: ${environment.apiEndpoint}/file?link=${value.link}`, 'Закрыть'),
        error: (err) => this.snackBar.open('Произошла ошибка', 'Закрыть')
      }
    )
  }

}
