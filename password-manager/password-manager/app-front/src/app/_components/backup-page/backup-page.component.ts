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

  decrypted: string = null;

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

  decryptBackup(masertPassword: string, backup: File) {
    let reader = new FileReader();
    reader.readAsText(backup);
    reader.onload = () => { 
      console.log(reader.result)
      this.apiService.decryptBackup(masertPassword, reader.result as string).subscribe(
        {
          next: (value) => { this.decrypted = value.data }
        }
      )
     }
    
  }

}
