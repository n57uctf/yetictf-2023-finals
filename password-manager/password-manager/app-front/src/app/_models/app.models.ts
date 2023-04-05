/* Api data models */

export interface ICredentialModel {
    username: string
    password: string
}

export interface IUserModel {
    user_id: number
    username: string
    password: string
    masterpass: string
}

export interface IAccessTokenModel {
    token: string
}

export interface IStorageModel {
    record_id: number
    password: string
    owner_username: string
    title: string
}

export interface ICreateStorageModel {
    password: string
    title: string
}

export interface IShareLinkModel {
    link: string
}

export interface IExportLinkModel {
    link: string
}

export interface IRegisteredUsersModel {
    username: string
}