namespace Vulnogramm.Models;
using Microsoft.EntityFrameworkCore;
[Index(nameof(Id), nameof(Owner), IsUnique = true)]

public class Post
{
    public string Owner { get; set; }
    public Int64 Id { get; set; }
    public string Subscript { get; set; }
    public string PhotoForAll { get; set; }
}
