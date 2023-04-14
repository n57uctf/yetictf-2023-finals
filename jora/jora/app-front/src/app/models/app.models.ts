/* Api data models */

export interface IUserModel {
  user_id: number
  username: string
  password: string
  info: string
}

export interface IRegistrationModel {
  username: string
  password: string
  info: string
}

export interface ICredentialModel {
  username: string
  password: string
}

export interface IAccessTokenModel {
  token: string
}

export interface IProjectModel {
  project_id: number
  name: string
  description: string
  creator: boolean
  tasks: {
      task_id: number
      name: string
      description: string
      attachments: string[]
      responsible: string
    }[]
  type: string
}

export interface INewProjectModel {
  usernames: string[]
  name: string
  description: string
}

export interface IAddProject {
  users: string[]
  new_project_data: {
    name: string,
    description: string
  }
}

export interface IFullTaskModel {
  task_id: number
  name: string
  description: string
  attachments: string[]
  responsible: string
}

export interface ITaskModel {
  task_id: number
  name: string
  description: string
  responsible: string
}

export interface INewTaskModel {
  name: string
  description: string
  responsible: string
}
