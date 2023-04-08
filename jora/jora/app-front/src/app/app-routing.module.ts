import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {LoginPageComponent} from "./login-page/login-page.component";
import {RegisterPageComponent} from "./register-page/register-page.component";
import {MainPageComponent} from "./main-page/main-page.component";
import {ProjectPageComponent} from "./project-page/project-page.component";


const routes: Routes = [
  {path: "login", component: LoginPageComponent},
  {path: "register", component: RegisterPageComponent},
  {path: "main", component: MainPageComponent},
  {path: "project", component: ProjectPageComponent},
  {path: "**", component: LoginPageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
