namespace Vulnogramm.Models;
using Microsoft.EntityFrameworkCore;

[Index(nameof(Id), nameof(Login), IsUnique = true)]

public class User
{
    public uint Id { get; set; }
    public string Login { get; set; }
    public string Password { get; set; }
}