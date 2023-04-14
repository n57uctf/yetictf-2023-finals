

//token = token.substring(token.indexOf(':')+1, token.indexOf(','));
async function validateToken(credentials) {
    return fetch(`${window.location.origin}/backend/validate`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    })
        .then(data => data.json());
}
export default async function Validate() {
    let token = localStorage.getItem('jwt');
    token = JSON.parse(token);
    token = token.access_token;
    const isValid = await validateToken({
        token: token
    });
    if (isValid)
    {
        console.log("Validation success");
    }
    return isValid;
}