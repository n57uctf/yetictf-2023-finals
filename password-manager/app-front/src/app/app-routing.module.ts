import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BackupPageComponent } from './_components/backup-page/backup-page.component';
import { LoginPageComponent } from './_components/login-page/login-page.component';
import { RegisterPageComponent } from './_components/register-page/register-page.component';
import { StoragePageComponent } from './_components/storage-page/storage-page.component';

const routes: Routes = [
  {path: 'login', component: LoginPageComponent},
  {path: 'register', component: RegisterPageComponent},
  {path: 'storage', component: StoragePageComponent},
  {path: 'backup', component: BackupPageComponent},
  {path: '**', component: LoginPageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
